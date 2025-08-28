# OctoFetch Tests

This directory contains unit tests for the OctoFetch API.

## Running Tests

To run the tests, make sure you have installed the testing dependencies:

```bash
pip install -r requirements.txt
```

Then run the tests using pytest:

```bash
pytest
```

Or to run tests with verbose output:

```bash
pytest -v
```

## Test Coverage

The tests cover the following components:

- **API Endpoints**: Tests for all FastAPI endpoints in `main.py`
- **Connectors**: Tests for the Jira and Confluence connectors
- **Core Functionality**: Tests for the normalizer and connector loader

## Adding New Tests

When adding new features to OctoFetch, please add corresponding tests to maintain code quality and prevent regressions.