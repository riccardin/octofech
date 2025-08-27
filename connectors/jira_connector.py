from typing import List, Dict, Optional
from .base_connector import BaseConnector
from atlassian import Jira
import os
import asyncio

class JiraConnector(BaseConnector):
    def name(self) -> str:
        return "jira"

    def _get_client(self):
        return Jira(
            url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_USERNAME"),
            password=os.getenv("JIRA_API_TOKEN"),
            verify_ssl=False
        )

    def fetch(self, jql: str = "ORDER BY created DESC", limit: Optional[int] = 200) -> List[Dict]:
        client = self._get_client()
        issues = client.jql(jql, limit=limit).get("issues", [])
        results = []
        for issue in issues:
            fields = issue.get("fields", {})
            results.append({
                "source": "jira",
                "id": issue.get("key"),
                "title": fields.get("summary"),
                "body": fields.get("description") or "",
                "tags": fields.get("labels") or [],
                "created_at": fields.get("created")
            })
        return results

    async def fetch_async(self, jql: str = "ORDER BY created DESC", limit: Optional[int] = 200) -> List[Dict]:
       
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.fetch, jql, limit)

    async def get_projects(self):
            return await asyncio.to_thread(self.client.get_all_projects)

    async def search_issues(self, jql):
        return await asyncio.to_thread(self.client.jql, jql)
    
    async def get_assigned_issues(self, assignee_email):
        jql = f'assignee = "{assignee_email}" ORDER BY created DESC'
        return await asyncio.to_thread(self.client.jql, jql)

    def fetch_assigned(self, assignee: str, limit: Optional[int] = 200) -> List[Dict]:
        jql = f'assignee = "{assignee}" ORDER BY created DESC'
        return self.fetch(jql=jql, limit=limit)