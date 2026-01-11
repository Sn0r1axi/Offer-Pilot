import os
import logging
from neo4j import GraphDatabase
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def verify_neo4j_content():
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        driver.verify_connectivity()
        logger.info(f"Connected to Neo4j at {NEO4J_URI}")
        
        with driver.session() as session:
            # Check database names
            try:
                result = session.run("SHOW DATABASES")
                dbs = [record["name"] for record in result]
                logger.info(f"Databases: {dbs}")
            except Exception as e:
                logger.warning(f"Could not list databases: {e}")

            # Check counts for each standard label
            labels = ["Entity", "Document", "TextNode", "Chunk", "_Node"]
            for label in labels:
                try:
                    res = session.run(f"MATCH (n:`{label}`) RETURN count(n) as c")
                    count = res.single()["c"]
                    logger.info(f"Nodes with label '{label}': {count}")
                except Exception as e:
                    logger.warning(f"Error counting label {label}: {e}")

            # Total count again
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]
            logger.info(f"Total Nodes (All labels): {total_nodes}")

    except Exception as e:
        logger.error(f"Verification failed: {e}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    verify_neo4j_content()
