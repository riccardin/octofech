from typing import Dict

def normalize(item: Dict) -> Dict:
    return {
        "source": item.get("source", ""),
        "id": str(item.get("id", "")),
        "title": item.get("title", "") or "",
        "body": item.get("body", "") or "",
        "tags": item.get("tags", []) or [],
        "created_at": item.get("created_at", "")
    }
