# OfferPilot

Advanced Agentic RAG system for Overseas University Admissions using GraphRAG.

## Architecture

*   **Orchestration**: LlamaIndex (PropertyGraphIndex, Workflows)
*   **Database**: Neo4j (Graph) + Qdrant (Vector)
*   **Ingestion**: Crawl4AI
*   **Backend**: FastAPI
*   **Frontend**: Streamlit
*   **AI**: Ollama (Llama3) + Gemini/GPT-4o

## Directory Structure

*   `src/ingestion`: Data collection and graph construction.
*   `src/retrieval`: Advanced RAG retrieval strategies.
*   `src/api`: Backend API services.
*   `src/frontend`: User interface.

## Getting Started

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Setup environment variables (TBD).
3.  Run the application (TBD).
