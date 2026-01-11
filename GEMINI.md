# UniGraph-RAG System Memory

This file contains the persistent system memory, coding standards, and tech stack definitions for the UniGraph-RAG project.

## 1. Tech Stack Definition

*   **Orchestration**: LlamaIndex (focus on PropertyGraphIndex and Workflow).
*   **Database**: Neo4j (Graph Store) + Qdrant (Vector Store).
*   **Data Acquisition**: Crawl4AI (Async/Web Scraping).
*   **Interface**: Streamlit (Frontend) + FastAPI (Backend API).
*   **LLM/Inference**: Ollama (Local Llama3 for indexing) + Gemini/GPT-4o (Cloud for reasoning).

## 2. Coding Standards (Strict Rules)

*   **Language**: Python 3.10+
*   **Paradigm**: AsyncIO first (always use `await` for I/O).
*   **Typing**: Strict Type Hints with Pydantic models for all data structures.
*   **Documentation**: Google-style docstrings for every function.
*   **Structure**: Modular design (separate `src/ingestion`, `src/retrieval`, `src/api`).

## 3. Project Structure

*   `src/ingestion`: Data acquisition and processing.
*   `src/retrieval`: RAG logic, graph traversal, and vector search.
*   `src/api`: FastAPI backend.
*   `src/frontend`: Streamlit interface.
