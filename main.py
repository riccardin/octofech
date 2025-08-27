import os
import asyncio
from fastapi import FastAPI, HTTPException, Query
from core.loader import load_connector_classes
from core.normalizer import normalize
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="OctoFetch - Async Pluggable Content Extractor")

CONNECTOR_CLASSES = load_connector_classes()

def build_config(prefix: str):
    # prefix expected like 'JIRA' or 'CONFLUENCE'
    return {
        "base_url": os.getenv(f"{prefix}_URL"),
        "token": os.getenv(f"{prefix}_TOKEN"),
        "user": os.getenv(f"{prefix}_USER")
    }

@app.get("/")
async def root():
    return {"message": "OctoFetch API is running 🚀"}

@app.get("/sources")
async def list_sources():
    # instantiate each class with dummy config to call name()
    names = []
    for cls in CONNECTOR_CLASSES:
        try:
            inst = cls({})
            names.append(inst.name())
        except Exception:
            # if instantiation fails, fallback to class name heuristic
            names.append(cls.__name__.replace('Connector', '').lower())
    return names

class FetchResponse(BaseModel):
    items: List[dict]

@app.get("/fetch/{source}", response_model=FetchResponse)
async def fetch_source(source: str, q: str = Query(None), limit: int = Query(100, le=1000)):
    for cls in CONNECTOR_CLASSES:
        # Use the connector's name() method to get the correct prefix for env vars
        inst = cls(build_config(cls.__name__.split(".")[-1].upper()))
        if inst.name() == source:
            try:
                if source == "jira":
                    items =  inst.fetch(jql=q or "ORDER BY created DESC", limit=limit)
                 
                elif source == "confluence":
                    items =  inst.fetch(space_key=q, limit=limit)
                else:
                    items =  inst.fetch(query=q, limit=limit)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            return {"items": [normalize(i) for i in items]}
    raise HTTPException(status_code=404, detail="source not found")
