# Second Brain API - The Note-taking Assistant - Local RAG System

A high-performance, fully local API for semantic note-taking and Retrieval-Augmented Generation (RAG). Built with FastAPI, this system allows users to store notes, perform vector-based semantic searches, and query an LLM that reasons exclusively over the user's saved knowledge base.

Designed with a clean, layered architecture (DDD principles) and MLOps best practices, including structured logging, latency tracking, and containerization.

## Features

*   **Full CRUD Operations:** Manage notes with MariaDB for relational metadata.
*   **Semantic Search:** Vectorize text using Hugging Face models and search via ChromaDB.
*   **Local RAG (Retrieval-Augmented Generation):** Ask questions to your knowledge base using a local LLM via Ollama, ensuring 100% data privacy.
*   **State Synchronization:** Automatic syncing between the relational database (MariaDB) and the vector database (ChromaDB) on updates and deletions.
*   **MLOps Ready:** Structured logging with Loguru to track request latency and LLM inference time.
*   **Containerized:** Dockerfile optimized for running locally with host network mapping and persistent volumes.

## Tech Stack

*   **Framework:** FastAPI
*   **Package Manager:** uv
*   **Relational Database:** MariaDB + Peewee ORM
*   **Vector Database:** ChromaDB
*   **Data Validation:** Pydantic
*   **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
*   **LLM Provider:** Ollama (`llama3.2`)
*   **Observability:** Loguru

## Prerequisites

*   Python 3.13+
*   [uv](https://github.com/astral-sh/uv) installed
*   MariaDB server running locally
*   [Ollama](https://ollama.com/) installed and running locally with the `llama3.2` model (`ollama pull llama3.2`)
*   Docker (if running via container)

## Environment Variables

Create a `.env` file in the root directory. An `.env.example` was provided with the necessary variables.

```sh
cp .env.example .env
```

## Bare Metal Setup (Development)

1. **Initialize the project and install dependencies:**
   ```bash
   uv sync
   ```

2. **Database Preparation:**
   Create a MariaDB database named `second_brain`.

3. **Download the Embedding Model:**
   Execute the script to cache the Hugging Face model locally (prevents re-downloading):
   ```bash
   uv run python download_model.py
   ```
   *(Ensure the script saves the model to the path specified in your `.env`)*

4. **Run the API:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

The API documentation will be available at `http://127.0.0.1:8000/docs`.

## Docker Setup (Production)

To run the application in an isolated container while maintaining access to your local MariaDB and Ollama instances:

1. **Build the image:**
   ```bash
   docker build -t note-taking-assistant .
   ```

2. **Run the container (Linux host):**
   ```bash
   docker run -d \
     --name note-taking-assistant \
     --network host \
     --env-file .env \
     -e MODEL_PATH=/model_cache \
     -v $(pwd)/chroma_data:/app/chroma_data \
     -v $(pwd)/app/core/dl_models/all-MiniLM-L6-v2:/model_cache \
     note-taking-assistant
   ```

3. **Monitor logs in real-time (MLOps tracking):**
   ```bash
   docker logs -f note-taking-assistant
   ```

## API Endpoints Overview

*   `GET /api/notes/` - List notes with pagination and title filtering.
*   `POST /api/notes/` - Create a new note (generates and stores vector embedding).
*   `GET /api/notes/{id}` - Retrieve a specific note.
*   `PUT /api/notes/{id}` - Update a note (recalculates vector embedding).
*   `DELETE /api/notes/{id}` - Delete a note (removes from MariaDB and ChromaDB).
*   `POST /api/notes/search` - Perform a semantic search based on a text query.
*   `POST /api/notes/ask` - Execute the RAG pipeline to generate an answer based on the knowledge base.

## Project Structure

```text
note-taking-assistant/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── notes.py        (FastAPI Routes)
│   ├── core/
│   │   ├── config.py           (Environment settings)
│   │   ├── database.py         (MariaDB & ChromaDB clients)
│   │   └── logger.py           (Loguru structured logging)
│   ├── models/
│   │   └── note.py             (Peewee ORM models)
│   ├── schemas/
│   │   └── note.py             (Pydantic DTOs for validation)
│   ├── services/
│   │   ├── llm_service.py      (Ollama API integration)
│   │   └── note_service.py     (Business logic & embedding sync)
│   └── main.py                 (Application entry point)
├── .env
├── docker_rebuild.sh           (Auxiliary bash script for development)
├── minhas_notas.db             (The SQLite file)
└── README.md
```
