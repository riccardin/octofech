# OctoFetch

OctoFetch is an async pluggable content extractor API that supports fetching content from various sources including Jira and Confluence.

## Features

- Async API endpoints using FastAPI
- Pluggable connector system
- Support for multiple data sources
- Normalized response format
- Configurable through environment variables

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Python-dotenv
- Atlassian Python API

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt

## Configuration
Create a .env file in the root directory with the following variables (adjust according to your sources):

JIRA_URL=https://your-jira-instance.com
JIRA_TOKEN=your-jira-token
JIRA_USER=your-username

CONFLUENCE_URL=https://your-confluence-instance.com
CONFLUENCE_TOKEN=your-confluence-token
CONFLUENCE_USER=your-username

## Running the Application
Debug Mode
uvicorn main:app --reload --port 8000

Production Mode

uvicorn main:app --port 8000

## API EndPoints

- GET / : Health check endpoint
- GET /sources : List available data sources
- GET /fetch/{source} : Fetch data from specified source
- Query Parameters:
  - q : Query string (JQL for Jira, space key for Confluence)
  - limit : Maximum number of items to return (default: 100, max: 1000)

## API Documentation
Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc