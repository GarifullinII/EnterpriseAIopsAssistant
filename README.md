# Enterprise AI Operations Assistant

Enterprise AI assistant backend for document processing, text extraction, RAG, and MCP-ready workflows.

## Stack

FastAPI, PostgreSQL, Redis, Qdrant, Docker Compose

## API

- `GET /`
- `GET /health`
- `POST /documents`
- `POST /documents/upload`
- `POST /documents/{document_id}/process`

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or:

```bash
docker compose up --build
```

Files are stored in `./uploads` and mounted to `/app/uploads` inside the container.

## Русский перевод

Backend для корпоративного AI-ассистента с обработкой документов, извлечением текста, RAG и MCP-ready workflow.

### Стек

FastAPI, PostgreSQL, Redis, Qdrant, Docker Compose

### API

- `GET /`
- `GET /health`
- `POST /documents`
- `POST /documents/upload`
- `POST /documents/{document_id}/process`

### Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Или:

```bash
docker compose up --build
```

Файлы сохраняются в `./uploads` и монтируются в контейнер по пути `/app/uploads`.
