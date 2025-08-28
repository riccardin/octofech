import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

def test_root_endpoint(client):
    """Test the root endpoint returns the expected message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OctoFetch API is running 🚀"}

def test_list_sources(client):
    """Test the /sources endpoint returns a list of available sources."""
    with patch('main.CONNECTOR_CLASSES', [
        MagicMock(return_value=MagicMock(name=MagicMock(return_value="jira"))),
        MagicMock(return_value=MagicMock(name=MagicMock(return_value="confluence")))
    ]):
        response = client.get("/sources")
        assert response.status_code == 200
        assert "jira" in response.json()
        assert "confluence" in response.json()

def test_fetch_jira_source(client, mock_jira_connector):
    """Test the /fetch/jira endpoint returns normalized items."""
    # Mock the fetch method to return test data
    mock_jira_connector.fetch.return_value = [
        {
            "source": "jira",
            "id": "TEST-123",
            "title": "Test Issue",
            "body": "Test Description",
            "tags": ["test", "unit-test"],
            "created_at": "2023-01-01T00:00:00.000Z"
        }
    ]
    
    # Mock the load_connector_classes function to return our mock
    with patch('main.CONNECTOR_CLASSES', [MagicMock(return_value=mock_jira_connector)]):
        response = client.get("/fetch/jira?q=test&limit=10")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == "TEST-123"
        assert data["items"][0]["title"] == "Test Issue"
        
        # Verify the mock was called with the right parameters
        mock_jira_connector.fetch.assert_called_once_with(jql="test", limit=10)

def test_fetch_confluence_source(client, mock_confluence_connector):
    """Test the /fetch/confluence endpoint returns normalized items."""
    # Mock the fetch method to return test data
    mock_confluence_connector.fetch.return_value = [
        {
            "source": "confluence",
            "id": "12345",
            "title": "Test Page",
            "body": "<p>Test Content</p>",
            "tags": ["documentation"],
            "created_at": "2023-01-01T00:00:00.000Z"
        }
    ]
    
    # Mock the load_connector_classes function to return our mock
    with patch('main.CONNECTOR_CLASSES', [MagicMock(return_value=mock_confluence_connector)]):
        response = client.get("/fetch/confluence?q=TEST&limit=10")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == "12345"
        assert data["items"][0]["title"] == "Test Page"
        
        # Verify the mock was called with the right parameters
        mock_confluence_connector.fetch.assert_called_once_with(space_key="TEST", limit=10)

def test_fetch_source_not_found(client):
    """Test the /fetch/{source} endpoint returns 404 for unknown sources."""
    with patch('main.CONNECTOR_CLASSES', []):
        response = client.get("/fetch/unknown")
        assert response.status_code == 404
        assert response.json() == {"detail": "source not found"}

def test_get_jira_users(client, mock_jira_connector):
    """Test the /users/jira endpoint returns users."""
    # Mock the get_all_users method to return test data
    mock_jira_connector.get_all_users.return_value = [
        {"accountId": "123", "displayName": "Test User", "emailAddress": "test@example.com"},
        {"accountId": "456", "displayName": "Another User", "emailAddress": "another@example.com"}
    ]
    
    # Mock the load_connector_classes function to return our mock
    with patch('main.CONNECTOR_CLASSES', [MagicMock(return_value=mock_jira_connector)]):
        response = client.get("/users/jira?q=test")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["displayName"] == "Test User"
        
        # Verify the mock was called with the right parameters
        mock_jira_connector.get_all_users.assert_called_once_with(query="test")

def test_get_users_unsupported_source(client, mock_confluence_connector):
    """Test the /users/{source} endpoint returns 400 for unsupported sources."""
    with patch('main.CONNECTOR_CLASSES', [MagicMock(return_value=mock_confluence_connector)]):
        response = client.get("/users/confluence")
        assert response.status_code == 400
        assert response.json() == {"detail": "Getting users not supported for confluence"}

def test_get_users_source_not_found(client):
    """Test the /users/{source} endpoint returns 404 for unknown sources."""
    with patch('main.CONNECTOR_CLASSES', []):
        response = client.get("/users/unknown")
        assert response.status_code == 404
        assert response.json() == {"detail": "source not found"}