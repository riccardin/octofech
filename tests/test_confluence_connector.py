import pytest
from unittest.mock import patch, MagicMock
from connectors.confluence_connector import ConfluenceConnector
import os

@pytest.fixture
def mock_confluence_client():
    """Mock the Confluence client from atlassian library."""
    with patch('connectors.confluence_connector.Confluence') as mock_confluence:
        mock_instance = MagicMock()
        mock_confluence.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def confluence_connector():
    """Create a ConfluenceConnector instance with mock config."""
    with patch.dict(os.environ, {
        "CONFLUENCE_URL": "https://test-confluence.example.com",
        "JIRA_USERNAME": "test_user",
        "CONFLUENCE_TOKEN": "test_token"
    }):
        connector = ConfluenceConnector({})
        yield connector

def test_name(confluence_connector):
    """Test the name method returns 'confluence'."""
    assert confluence_connector.name() == "confluence"

def test_get_client(confluence_connector):
    """Test the _get_client method creates a Confluence client with correct parameters."""
    with patch('connectors.confluence_connector.Confluence') as mock_confluence:
        confluence_connector._get_client()
        mock_confluence.assert_called_once_with(
            url="https://test-confluence.example.com",
            username="test_user",
            password="test_token",
            verify_ssl=False
        )

def test_fetch(confluence_connector, mock_confluence_client):
    """Test the fetch method returns normalized pages."""
    # Mock the cql method to return test data
    mock_confluence_client.cql.return_value = {
        "results": [
            {"id": "12345"}
        ]
    }
    
    # Mock the get_page_by_id method to return test data
    mock_confluence_client.get_page_by_id.return_value = {
        "id": "12345",
        "title": "Test Page",
        "body": {"storage": {"value": "<p>Test Content</p>"}},
        "metadata": {"labels": [{"name": "documentation"}]},
        "history": {"createdDate": "2023-01-01T00:00:00.000Z"}
    }
    
    # Call the fetch method
    with patch('connectors.confluence_connector.ConfluenceConnector._get_client', return_value=mock_confluence_client):
        results = confluence_connector.fetch(space_key="TEST", limit=10)
    
    # Verify the results
    assert len(results) == 1
    assert results[0]["source"] == "confluence"
    assert results[0]["id"] == "12345"
    assert results[0]["title"] == "Test Page"
    assert results[0]["body"] == "<p>Test Content</p>"
    assert results[0]["tags"] == ["documentation"]
    assert results[0]["created_at"] == "2023-01-01T00:00:00.000Z"
    
    # Verify the mock was called with the right parameters
    # Note: The current implementation uses a hardcoded CQL query
    mock_confluence_client.cql.assert_called_once_with('creator = "Rick.Magana" ORDER BY lastmodified DESC', limit=10)
    mock_confluence_client.get_page_by_id.assert_called_once_with("12345", expand="body.storage,version,history,metadata.labels")