try:
    from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
    print("Neo4jPropertyGraphStore found!")
except ImportError:
    print("Neo4jPropertyGraphStore NOT found.")

try:
    from llama_index.graph_stores.neo4j import Neo4jGraphStore
    print("Neo4jGraphStore found!")
except ImportError:
    print("Neo4jGraphStore NOT found.")
