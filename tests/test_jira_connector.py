import pytest
from unittest.mock import patch, MagicMock
from connectors.jira_connector import JiraConnector
import os

@pytest.fixture
def mock_jira_client():
    """Mock the Jira client from atlassian library."""
    with patch('connectors.jira_connector.Jira') as mock_jira:
        mock_instance = MagicMock()
        mock_jira.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def jira_connector():
    """Create a JiraConnector instance with mock config."""
    with patch.dict(os.environ, {
        "JIRA_URL": "https://test-jira.example.com",
        "JIRA_USERNAME": "test_user",
        "JIRA_API_TOKEN": "test_token"
    }):
        connector = JiraConnector({})
        yield connector

def test_name(jira_connector):
    """Test the name method returns 'jira'."""
    assert jira_connector.name() == "jira"

def test_get_client(jira_connector):
    """Test the _get_client method creates a Jira client with correct parameters."""
    with patch('connectors.jira_connector.Jira') as mock_jira:
        jira_connector._get_client()
        mock_jira.assert_called_once_with(
            url="https://test-jira.example.com",
            username="test_user",
            password="test_token",
            verify_ssl=False
        )

def test_fetch(jira_connector, mock_jira_client):
    """Test the fetch method returns normalized issues."""
    # Mock the jql method to return test data
    mock_jira_client.jql.return_value = {
        "issues": [
            {
                "key": "TEST-123",
                "fields": {
                    "summary": "Test Issue",
                    "description": "Test Description",
                    "labels": ["test", "unit-test"],
                    "created": "2023-01-01T00:00:00.000Z"
                }
            }
        ]
    }
    
    # Call the fetch method
    with patch('connectors.jira_connector.JiraConnector._get_client', return_value=mock_jira_client):
        results = jira_connector.fetch(jql="project = TEST", limit=10)
    
    # Verify the results
    assert len(results) == 1
    assert results[0]["source"] == "jira"
    assert results[0]["id"] == "TEST-123"
    assert results[0]["title"] == "Test Issue"
    assert results[0]["body"] == "Test Description"
    assert results[0]["tags"] == ["test", "unit-test"]
    assert results[0]["created_at"] == "2023-01-01T00:00:00.000Z"
    
    # Verify the mock was called with the right parameters
    mock_jira_client.jql.assert_called_once_with("project = TEST", limit=10)

@pytest.mark.asyncio
async def test_fetch_async(jira_connector):
    """Test the fetch_async method calls fetch with the same parameters."""
    with patch('connectors.jira_connector.JiraConnector.fetch') as mock_fetch:
        mock_fetch.return_value = [{"id": "TEST-123"}]
        results = await jira_connector.fetch_async(jql="project = TEST", limit=10)
    
    # Verify the results
    assert results == [{"id": "TEST-123"}]
    
    # Verify the mock was called with the right parameters
    mock_fetch.assert_called_once_with("project = TEST", 10)

@pytest.mark.asyncio
async def test_get_all_users(jira_connector, mock_jira_client):
    """Test the get_all_users method returns users from the Jira client."""
    # Mock the user_find_by_user_string method to return test data
    mock_jira_client.user_find_by_user_string.return_value = [
        {"accountId": "123", "displayName": "Test User", "emailAddress": "test@example.com"},
        {"accountId": "456", "displayName": "Another User", "emailAddress": "another@example.com"}
    ]
    
    # Call the get_all_users method
    with patch('connectors.jira_connector.JiraConnector._get_client', return_value=mock_jira_client):
        results = await jira_connector.get_all_users(query="test")
    
    # Verify the results
    assert len(results) == 2
    assert results[0]["accountId"] == "123"
    assert results[0]["displayName"] == "Test User"
    
    # Verify the mock was called with the right parameters
    mock_jira_client.user_find_by_user_string.assert_called_once_with("test")

def test_fetch_assigned(jira_connector):
    """Test the fetch_assigned method calls fetch with the correct JQL."""
    with patch('connectors.jira_connector.JiraConnector.fetch') as mock_fetch:
        mock_fetch.return_value = [{"id": "TEST-123"}]
        results = jira_connector.fetch_assigned(assignee="test@example.com", limit=10)
    
    # Verify the results
    assert results == [{"id": "TEST-123"}]
    
    # Verify the mock was called with the right parameters
    mock_fetch.assert_called_once_with(jql='assignee = "test@example.com" ORDER BY created DESC', limit=10)