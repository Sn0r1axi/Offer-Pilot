import os
import logging
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def verify_neo4j_content():
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        driver.verify_connectivity()
        logger.info(f"Connected to Neo4j at {NEO4J_URI}")
        
        with driver.session() as session:
            # 1. Count Total Nodes
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]
            logger.info(f"Total Nodes: {total_nodes}")

            # 2. Count Relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            total_rels = result.single()["count"]
            logger.info(f"Total Relationships: {total_rels}")

            # 3. Check for specific Labels (LlamaIndex usually creates specific labels)
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            logger.info(f"Labels found: {labels}")

            if total_nodes == 0:
                logger.warning("The database is empty. The ingestion script may have failed silently or no data was found.")
            else:
                logger.info("Content verification successful: Data is present in the graph.")

    except Exception as e:
        logger.error(f"Verification failed: {e}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    verify_neo4j_content()
