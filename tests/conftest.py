import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def mock_jira_connector():
    """Mock the JiraConnector class for testing."""
    with patch('connectors.jira_connector.JiraConnector') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.name.return_value = "jira"
        yield mock_instance

@pytest.fixture
def mock_confluence_connector():
    """Mock the ConfluenceConnector class for testing."""
    with patch('connectors.confluence_connector.ConfluenceConnector') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.name.return_value = "confluence"
        yield mock_instance