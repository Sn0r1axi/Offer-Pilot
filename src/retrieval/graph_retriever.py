import os
import logging
from dotenv import load_dotenv
from llama_index.core import PropertyGraphIndex, Settings
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.gemini import Gemini
import nest_asyncio

# Apply nest_asyncio to help with async event loops in scripts/notebooks
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found. Gemini LLM may fail.")

def get_query_engine():
    """
    Reconstructs the PropertyGraphIndex from Neo4j and returns a query engine.
    """
    
    # 1. Setup LLM & Embedding (Must match ingestion settings for consistency)
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=GOOGLE_API_KEY)

    # 2. Connect to Neo4j Graph Store
    try:
        graph_store = Neo4jPropertyGraphStore(
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            url=NEO4J_URI,
        )
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
        raise e

    # 3. Load Index from existing Graph Store
    # We use PropertyGraphIndex.from_existing to load the index structure
    # that is already present in Neo4j.
    logger.info("Loading PropertyGraphIndex from Neo4j...")
    
    index = PropertyGraphIndex.from_existing(
        property_graph_store=graph_store,
        llm=Settings.llm,
        embed_model=Settings.embed_model
    )
    
    # 4. Create Query Engine
    # Using the higher-level 'as_query_engine' which abstracts the retrieval
    # and answer generation.
    query_engine = index.as_query_engine(
        include_text=True, # Include text from nodes in the context
        similarity_top_k=5 # How many nodes to retrieve
    )
    
    logger.info("Query Engine created.")
    return query_engine
