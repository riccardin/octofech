import pytest
from unittest.mock import patch, MagicMock
from core.normalizer import normalize
from core.loader import load_connector_classes
from connectors.base_connector import BaseConnector

def test_normalize():
    """Test the normalize function correctly formats items."""
    # Test with complete data
    item = {
        "source": "test",
        "id": 123,
        "title": "Test Title",
        "body": "Test Body",
        "tags": ["test", "unit-test"],
        "created_at": "2023-01-01T00:00:00.000Z"
    }
    
    result = normalize(item)
    
    assert result["source"] == "test"
    assert result["id"] == "123"  # Should be converted to string
    assert result["title"] == "Test Title"
    assert result["body"] == "Test Body"
    assert result["tags"] == ["test", "unit-test"]
    assert result["created_at"] == "2023-01-01T00:00:00.000Z"
    
    # Test with missing data
    item = {
        "source": "test",
        "id": 123
    }
    
    result = normalize(item)
    
    assert result["source"] == "test"
    assert result["id"] == "123"
    assert result["title"] == ""
    assert result["body"] == ""
    assert result["tags"] == []
    assert result["created_at"] == ""
    
    # Test with None values
    item = {
        "source": "test",
        "id": 123,
        "title": None,
        "body": None,
        "tags": None,
        "created_at": None
    }
    
    result = normalize(item)
    
    assert result["source"] == "test"
    assert result["id"] == "123"
    assert result["title"] == ""
    assert result["body"] == ""
    assert result["tags"] == []
    assert result["created_at"] == ""

# Create a mock connector class for testing
class MockConnector(BaseConnector):
    def name(self):
        return "mock"
    
    async def fetch(self, **kwargs):
        return []

def test_load_connector_classes():
    """Test the load_connector_classes function finds connector classes."""
    # Mock the pkgutil.iter_modules function to return our test modules
    mock_modules = [(None, "mock_connector", False), (None, "base_connector", False)]
    
    # Mock the importlib.import_module function to return a module with our mock connector
    mock_module = MagicMock()
    mock_module.__name__ = "connectors.mock_connector"
    
    # Add our MockConnector class to the module
    mock_module.MockConnector = MockConnector
    
    with patch('pkgutil.iter_modules', return_value=mock_modules), \
         patch('importlib.import_module', return_value=mock_module):
        
        # Call the function
        result = load_connector_classes()
        
        # Verify the result
        assert len(result) == 1
        assert result[0] == MockConnector