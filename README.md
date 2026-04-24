# Enterprise AI Operations Assistant

Production-like backend for an enterprise AI assistant with document processing, RAG, MCP, agent workflows, and n8n automation.

## English

### What This Project Is

Enterprise AI backend platform focused on:

- document upload and text extraction
- chunking and RAG preparation
- PostgreSQL metadata storage
- Redis and Qdrant infrastructure
- upcoming MCP server layer
- upcoming agent routing and n8n workflows

This project is designed as a practical MVP for AI Backend / Applied AI / RAG Platform roles.

### Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Qdrant
- LangChain
- Docker Compose
- MCP
- n8n

### Current API

- `GET /`
- `GET /health`
- `POST /documents`
- `POST /documents/upload`
- `POST /documents/{document_id}/process`
- `POST /documents/{document_id}/chunk`
- `GET /documents/{document_id}/chunks`

### Current Flow

```text
upload -> store -> extract text -> chunk text -> prepare for embeddings
```

### Run

Local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./.venv/bin/python -m uvicorn app.main:app --reload
```

Docker:

```bash
docker compose up --build
```

Note:
the current `.env` is Docker-oriented. If you run the API directly from your machine, `POSTGRES_HOST=postgres` may need to be changed to `localhost`.

### Why It Looks Good for Vacancies

This repository shows:

- AI-ready backend architecture
- document ingestion pipeline design
- RAG-oriented data preparation
- infrastructure thinking with PostgreSQL, Redis, and Qdrant
- roadmap toward MCP, agents, and automation

## Русский

### Что Это За Проект

Production-like backend-платформа для enterprise AI assistant с акцентом на:

- загрузку документов и извлечение текста
- chunking и подготовку к RAG
- хранение metadata в PostgreSQL
- инфраструктуру Redis и Qdrant
- будущий MCP server layer
- будущие agent workflows и automation через n8n

Проект делается как практический MVP под направления:

- AI Backend Engineer
- Applied AI Engineer
- Python Backend Engineer
- RAG / LLM Platform Engineer

### Стек

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Qdrant
- LangChain
- Docker Compose
- MCP
- n8n

### Текущее API

- `GET /`
- `GET /health`
- `POST /documents`
- `POST /documents/upload`
- `POST /documents/{document_id}/process`
- `POST /documents/{document_id}/chunk`
- `GET /documents/{document_id}/chunks`

### Текущий Flow

```text
upload -> store -> extract text -> chunk text -> prepare for embeddings
```

### Запуск

Локально:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./.venv/bin/python -m uvicorn app.main:app --reload
```

Через Docker:

```bash
docker compose up --build
```

Важно:
текущий `.env` настроен под Docker Compose. Для локального запуска может понадобиться заменить `POSTGRES_HOST=postgres` на `localhost`.

### Почему Это Сильно Для Вакансий

Проект показывает:

- backend-подход к AI-продукту
- ingestion pipeline для документов
- подготовку данных под RAG
- работу с PostgreSQL, Redis и Qdrant
- понятный roadmap к MCP, agents и automation
