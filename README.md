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
```
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



## 🔑 Best Practices for Testing REST API Endpoints

When testing REST API endpoints, a lot of time can be wasted on trial-and-error with parameters and payloads.
This section outlines best practices to reduce guesswork and accelerate testing.

📖 1.  Use OpenAPI / Swagger Specs

  - Most modern APIs expose an OpenAPI specification (/openapi.json, /docs).

   - Use tools like Swagger UI or ReDoc to explore available endpoints and their required parameters.

   - In FastAPI, you automatically get:

      - /docs → Swagger UI

      - /redoc → ReDoc



💻 2. Prefer SDKs or API Clients

- Many APIs provide official SDKs (e.g., atlassian-python-api, stripe-python, boto3).

- SDKs enforce correct parameter structures and reduce common mistakes.

- When possible, use the SDK instead of raw REST calls.

🧪 3. Use API Playgrounds & Postman

- Interactive dashboards, Postman collections, or mock servers save time.

- Postman or Hoppscotch can act as living documentation with ready-to-use requests.

- Import your API’s OpenAPI spec into Postman → every endpoint is pre-configured.



🤖 7. Automate API Testing

Build automated tests with known-good requests.

Example tools:

- Python: pytest + httpx / requests

- Postman’s built-in test runner



## 🔗 Links 

[Atlassian Documentation](https://confluence.atlassian.com/alldoc/atlassian-documentation-32243719.html)

[Atlassian Postman Reference Library](https://www.postman.com/api-reference-library/atlassian-cloud)
