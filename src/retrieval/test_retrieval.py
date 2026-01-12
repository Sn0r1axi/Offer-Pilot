import sys
import os

# Ensure the src directory is in the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.retrieval.graph_retriever import get_query_engine

def test_retrieval():
    print("Initializing Query Engine...")
    try:
        query_engine = get_query_engine()
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return

    question = "Which universities are in the database?"
    print(f"\nAsking: {question}")
    
    try:
        response = query_engine.query(question)
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"Query failed: {e}")

if __name__ == "__main__":
    test_retrieval()
