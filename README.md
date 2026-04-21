# Enterprise AI Operations Assistant

Production-style backend foundation for an enterprise AI assistant with a clear path toward RAG, MCP-based tooling, agent workflows, and operational monitoring.

The project starts with a small FastAPI service and a local infrastructure stack, so it can grow from a simple health-checked API into a real multi-service AI platform without rewriting the basics later.

## Goal

Build an enterprise AI assistant that can:

- answer questions over internal documents with RAG;
- expose tools, resources, and prompts through an MCP server;
- orchestrate multi-step agent workflows;
- integrate with automation platforms such as n8n;
- run in a containerized local and production-style environment.

## Current architecture

At the current stage, the project includes:

- `FastAPI` for the backend API;
- `PostgreSQL` for structured application data;
- `Redis` for caching and background workflow support;
- `Qdrant` for vector storage and semantic search;
- `Docker Compose` for local multi-service startup.

## Project structure

```text
.
├── app/
│   ├── api/routes/documents.py
│   ├── core/
│   ├── models/document.py
│   ├── schemas/document.py
│   └── main.py
├── Dockerfile
├── compose.yaml
├── uploads/
├── requirements.txt
└── README.md
```

### Key files

- `app/main.py` - FastAPI application entrypoint
- `app/api/routes/documents.py` - document creation and upload endpoints
- `app/models/document.py` - SQLAlchemy document model
- `app/schemas/document.py` - request and response schemas for documents
- `Dockerfile` - container image for the API service
- `compose.yaml` - local stack with API, PostgreSQL, Redis, and Qdrant, plus mounted uploads storage
- `requirements.txt` - Python dependencies

## API

Current endpoints:

- `GET /` - returns a basic service message
- `GET /health` - returns service status, version, and current database host
- `POST /documents` - creates a document record without a file
- `POST /documents/upload` - uploads a file, stores it in `uploads/`, and updates document metadata

Example `/health` response:

```json
{
  "status": "ok",
  "service": "api",
  "version": "0.1.0",
  "database_host": "postgres"
}
```

Example `/documents/upload` response:

```json
{
  "id": "d9c2b6ce-0817-4dfa-adf7-a8cb90397282",
  "title": "VPN policy",
  "source": "manual",
  "status": "stored",
  "original_filename": "vpn-policy.pdf",
  "file_path": "uploads/d9c2b6ce-0817-4dfa-adf7-a8cb90397282.pdf",
  "mime_type": "application/pdf",
  "created_at": "2026-04-21T13:21:06.032602"
}
```

## Requirements

- Python 3.11+
- Docker and Docker Compose for container-based startup

## Run locally

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API:

```bash
uvicorn app.main:app --reload
```

5. Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`

## Run with Docker Compose

Start the full local stack:

```bash
docker compose up --build
```

This starts:

- `api` on port `8000`
- `postgres` on port `5432`
- `redis` on port `6379`
- `qdrant` on ports `6333` and `6334`

The `uploads/` directory is mounted into the API container, so uploaded files are visible both:

- inside the container at `/app/uploads`
- locally in the project folder at `./uploads`

## Environment variables

The API currently reads these variables:

- `APP_VERSION`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `REDIS_HOST`
- `REDIS_PORT`
- `QDRANT_HOST`
- `QDRANT_PORT`

Example `.env`:

```env
APP_VERSION=0.1.0
POSTGRES_DB=aiops
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
REDIS_HOST=redis
QDRANT_HOST=qdrant
```

## Current status

Day 4:

- base FastAPI service is running;
- PostgreSQL, Redis, and Qdrant start via Docker Compose;
- `Document` model includes file metadata and processing status;
- `/documents` creates a document record;
- `/documents/upload` accepts multipart form data and saves files to `uploads/`;
- uploaded files are persisted through a Docker volume mount;
- document status changes from `uploaded` to `stored` after file save.

## Roadmap

Next planned steps:

- extract text from uploaded documents;
- add document processing states beyond `stored`;
- create the first ingestion pipeline for chunking;
- generate embeddings and save them to Qdrant;
- create the first RAG retrieval and answer flow;
- add MCP server capabilities;
- introduce observability, testing, and deployment automation.
