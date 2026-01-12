from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.retrieval.graph_retriever import get_query_engine

import nest_asyncio
nest_asyncio.apply()

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Global variables
query_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load the query engine on startup.
    """
    global query_engine
    logger.info("Startup: Loading Query Engine...")
    try:mm
        query_engine = get_query_engine()
        logger.info("Startup: Query Engine loaded successfully.")
    except Exception as e:
        logger.error(f"Startup: Failed to load Query Engine: {e}")
        # We might want to raise here or handle it gracefully depending on requirements
        # For now, we'll let it fail on first request if it's None.
    
    yield
    
    logger.info("Shutdown: Cleaning up...")

app = FastAPI(title="Offer-Pilot API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_graph(request: QueryRequest):
    global query_engine
    
    if not query_engine:
        raise HTTPException(status_code=503, detail="Query Engine is not ready.")
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query text is required.")

    try:
        logger.info(f"Processing query: {request.query}")
        response = await query_engine.aquery(request.query)
        return QueryResponse(answer=str(response))
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
