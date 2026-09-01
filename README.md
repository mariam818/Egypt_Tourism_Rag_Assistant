# RAG-Powered Egypt Tourism Assistant

An AI-powered travel assistant that answers questions about Egypt using the Lonely Planet travel guide. Built with RAG (Retrieval-Augmented Generation) technology to provide grounded, cited answers.

## Overview

This application allows users to ask questions about Egypt tourism and receives answers grounded in the Lonely Planet Egypt travel guide. The system uses semantic search to find relevant document sections and a local LLM to generate cited responses.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend       │────▶│   Ollama LLM    │
│   (Streamlit)   │◀────│   (FastAPI)     │◀────│   (llama3.2)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   ChromaDB      │
                        │   (Vector DB)   │
                        └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   Lonely Planet │
                        │   Egypt PDF     │
                        └─────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.10, FastAPI |
| Frontend | Streamlit |
| LLM | Ollama (llama3.2) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| Pipeline | Jupyter Notebook |

## Project Structure

```
rag_assitant_project/
├── rag_assitant_project/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py              # FastAPI app entry point
│   │   │   ├── api/routes/query.py  # /health and /query endpoints
│   │   │   ├── core/config.py       # Settings from .env
│   │   │   ├── schemas/query.py     # QueryRequest / QueryResponse
│   │   │   ├── services/
│   │   │   │   ├── retrieval.py     # Vector store retrieval
│   │   │   │   └── generation.py    # Ollama LLM calls
│   │   │   └── utils/logging_config.py
│   │   ├── data/
│   │   │   ├── documents/           # Source PDF documents
│   │   │   └── vector_store/        # Persisted ChromaDB
│   │   ├── tests/test_query.py      # API tests
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   └── Dockerfile
│   ├── frontend/
│   │   ├── app.py                   # Streamlit application
│   │   ├── api_client.py            # Backend API client
│   │   ├── .env
│   │   └── requirements.txt
│   └── phase2.ipynb                 # RAG pipeline notebook
├── .gitignore
└── README.md
```

## Domain & Data

- **Domain**: Egypt tourism
- **Source**: Lonely Planet Egypt travel guide (PDF)
- **Content**: Tourist attractions, transportation, food, practical information
- **Chunks**: ~900 words with 150-word overlap

## Setup Prerequisites

- Python 3.10+
- Ollama installed and running (https://ollama.com)

## Backend Setup

```bash
cd rag_assitant_project/backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Pull Ollama model
ollama pull llama3.2

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with Swagger docs at `/docs`.

## Frontend Setup

```bash
cd rag_assitant_project/frontend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The UI will open at `http://localhost:8501`.

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| OLLAMA_HOST | Ollama server URL | http://localhost:11434 |
| OLLAMA_MODEL | Model name | llama3.2 |
| FRONTEND_ORIGIN | Allowed CORS origin | http://localhost:8501 |
| API_HOST | Server host | 0.0.0.0 |
| API_PORT | Server port | 8000 |
| TOP_K | Number of chunks to retrieve | 5 |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| API_BASE_URL | Backend URL | http://localhost:8000 |

## API Reference

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Egypt Tourism RAG API",
  "retrieval": "ready",
  "generation": "ready"
}
```

### POST /query

Submit a question and get a grounded answer.

**Request:**
```json
{
  "question": "What are the main attractions in Luxor?"
}
```

**Response:**
```json
{
  "answer": "According to the guide, Luxor features... [1] [2]",
  "sources": [
    "[1] Lonely_Planet_Egypt.pdf (Page 123, Chunk xyz_page_123_chunk_0)"
  ]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main attractions in Luxor?"}'
```

## Evaluation Results

Tested with 10 questions covering attractions, transportation, food, and destinations:

| Question | Retrieved Source | Correct |
|----------|-----------------|---------|
| Main attractions in Cairo? | Lonely Planet Egypt (p. 45) | Yes |
| Attractions around Giza? | Lonely Planet Egypt (p. 52) | Yes |
| Historical sites in Luxor? | Lonely Planet Egypt (p. 123) | Yes |
| Things to do in Aswan? | Lonely Planet Egypt (p. 156) | Yes |
| Information about Alexandria? | Lonely Planet Egypt (p. 89) | Yes |
| Red Sea destinations? | Lonely Planet Egypt (p. 178) | Yes |
| Transportation options? | Lonely Planet Egypt (p. 12) | Yes |
| Practical tourist info? | Lonely Planet Egypt (p. 8) | Yes |
| Egyptian food and dining? | Lonely Planet Egypt (p. 34) | Yes |
| Sinai information? | Lonely Planet Egypt (p. 201) | Yes |

## Tests

```bash
cd rag_assitant_project/backend
pytest tests/test_query.py -v
```

## License

This project was developed as part of the ITI Level 2 Summer Training graduation project.
