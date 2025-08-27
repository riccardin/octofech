
from typing import List, Dict, Optional
from .base_connector import BaseConnector
from atlassian import Confluence

class ConfluenceConnector(BaseConnector):
    def name(self) -> str:
        return "confluence"

    def _get_client(self):
        return Confluence(
            url=self.config.get("base_url"),
            username=self.config.get("user"),
            password=self.config.get("token"),
            cloud=True
        )

    def fetch(self, space_key: str = None, cql: str = None, limit: Optional[int] = 100) -> List[Dict]:
        if not cql and not space_key:
            raise ValueError("space_key or cql must be provided")
        client = self._get_client()
        query = cql or f'space = "{space_key}" ORDER BY lastmodified DESC'
        results = client.cql(query, limit=limit).get("results", [])
        final = []
        for item in results[:limit]:
            page = client.get_page_by_id(item["id"], expand="body.storage,version,history,metadata.labels")
            body = page.get("body", {}).get("storage", {}).get("value", "")
            labels = [l.get("name") for l in page.get("metadata", {}).get("labels", [])] if page.get("metadata") else []
            final.append({
                "source": "confluence",
                "id": page.get("id"),
                "title": page.get("title"),
                "body": body,
                "tags": labels,
                "created_at": page.get("history", {}).get("createdDate") or page.get("version", {}).get("when")
            })
        return final