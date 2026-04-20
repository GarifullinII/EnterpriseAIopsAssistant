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
│   └── main.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

### Key files

- `app/main.py` - FastAPI application entrypoint
- `Dockerfile` - container image for the API service
- `compose.yaml` - local stack with API, PostgreSQL, Redis, and Qdrant
- `requirements.txt` - Python dependencies

## API

Current endpoints:

- `GET /` - returns a basic service message
- `GET /health` - returns service status, version, and configured infrastructure hosts

Example `/health` response:

```json
{
  "status": "ok",
  "service": "api",
  "version": "0.1.0",
  "postgres_host": "postgres",
  "redis_host": "redis",
  "qdrant_host": "qdrant"
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

## Environment variables

The API currently reads these variables:

- `APP_VERSION`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `REDIS_HOST`
- `QDRANT_HOST`

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

Day 1:

- base project structure created;
- FastAPI application started;
- `/health` endpoint implemented;
- Dockerfile added for API containerization;
- Docker Compose stack added for PostgreSQL, Redis, and Qdrant;
- `.gitignore` updated for local environments and generated artifacts.

## Roadmap

Next planned steps:

- split API routes and service logic into dedicated modules;
- add configuration management and settings layer;
- connect PostgreSQL models and persistence;
- add Redis-backed caching and job processing;
- create the first RAG ingestion and query flow;
- add MCP server capabilities;
- introduce observability, testing, and deployment automation.
