import os
import json
import logging
from typing import List
from dotenv import load_dotenv
from llama_index.core import Document, PropertyGraphIndex, Settings
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.gemini import Gemini
import nest_asyncio

nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found in environment variables. Gemini LLM may fail.")

# Setup LLM & Embedding
# Using FastEmbed for embeddings
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Using Gemini 2.5 Flash for specific reasoning capabilities
Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=GOOGLE_API_KEY)

def load_documents_from_json(data_dir: str) -> List[Document]:
    """Loads university data from JSON files as LlamaIndex Documents."""
    documents = []
    if not os.path.exists(data_dir):
        logger.warning(f"Data directory not found: {data_dir}")
        return []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Main Page
                    if data.get("content"):
                        doc = Document(
                            text=data["content"],
                            metadata={
                                "url": data.get("url", ""),
                                "title": data.get("name", "Unknown"),
                                "type": "main_page",
                                "university": data.get("name", "Unknown")
                            }
                        )
                        documents.append(doc)
                    
                    # Sub Pages
                    for sub in data.get("sub_pages", []):
                        if sub.get("content"):
                            doc = Document(
                                text=sub["content"],
                                metadata={
                                    "url": sub.get("url", ""),
                                    "title": f"{data.get('name', 'Unknown')} - SubPage",
                                    "type": "sub_page",
                                    "university": data.get("name", "Unknown")
                                }
                            )
                            documents.append(doc)
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
                
    return documents

def build_graph():
    """Ingests documents into Neo4j Property Graph."""
    logger.info("Initializing Graph Builder...")
    
    # 1. Connect to Neo4j
    try:
        graph_store = Neo4jPropertyGraphStore(
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            url=NEO4J_URI,
        )
        logger.info("Connected to Neo4j.")
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
        return

    # 2. Load Documents
    data_path = os.path.join(os.getcwd(), "data", "raw")
    docs = load_documents_from_json(data_path)
    logger.info(f"Loaded {len(docs)} documents from {data_path}.")
    
    if not docs:
        logger.warning("No documents to ingest. Exiting.")
        return

    # 3. Create Index
    # PropertyGraphIndex will use the default extractor (ImplicitPathExtractor) if not specified,
    # or it uses the LLM to extract KG triplets.
    # Without an LLM configured in Settings, this might fail if it tries to use OpenAI by default and no key is present.
    # We will try to rely on the environment variables provided by the user.
    
    logger.info("Creating PropertyGraphIndex... (This may take time)")
    
    try:
        index = PropertyGraphIndex.from_documents(
            docs,
            property_graph_store=graph_store,
            show_progress=True,
            # We can specify kg_extractors here if we want to customize, e.g., SimpleLLMPathExtractor
        )
        logger.info("Graph ingestion complete! Nodes and relationships should be in Neo4j.")
    except Exception as e:
        logger.error(f"Error building index: {e}")

if __name__ == "__main__":
    build_graph()
