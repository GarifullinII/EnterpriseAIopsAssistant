# Enterprise AI Operations Assistant

Production-like backend for an enterprise AI assistant with document processing, RAG, MCP, agent workflows, and n8n automation.

## Русский

### Что Это За Проект

Production-like backend-платформа для enterprise AI assistant с акцентом на:

- загрузку документов и извлечение текста
- chunking и подготовку к RAG
- embeddings и индексацию документов
- хранение metadata в PostgreSQL
- инфраструктуру Redis и Qdrant
- интеграцию LangChain OpenAI embeddings
- MCP server layer
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
- `POST /documents/{document_id}/index`
- `POST /search`
- `POST /search/documents/{document_id}`
- `POST /ask`

### MCP Layer

- `search_documents` tool
- `ask_documents` tool
- `get_document_chunks` tool
- `documents://catalog` resource
- `document_qa_prompt` prompt template

### Что Уже Реализовано

- загрузка документов и сохранение файлов
- извлечение текста из `txt`, `md`, `pdf`, `docx`, `doc`, `xlsx`, `xls`
- создание chunks и сохранение chunks в PostgreSQL
- Alembic миграции для `documents` и `document_chunks`
- indexing pipeline через OpenAI embeddings и Qdrant upsert
- semantic search endpoint для поиска релевантных chunks в Qdrant
- document-level semantic search
- RAG answer endpoint with sources
- MCP server поверх существующих retrieval и RAG сервисов
- pipeline статусов документа: `uploaded -> stored -> processed -> chunked -> indexed`

### Текущий Flow

```text
upload -> store -> extract text -> chunk text -> index in Qdrant -> semantic search -> RAG answer
```

MCP flow:

```text
MCP client -> FastMCP server -> tools/resources/prompts -> existing app services
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

Запуск MCP server:

```bash
python scripts/run_mcp.py
```

Проверка MCP tools программно:

```bash
python scripts/check_mcp_tools.py
```

Пример вызова `search_documents` через MCP client:

```bash
python scripts/call_search_documents.py "your search query"
```


## English

### What This Project Is

Enterprise AI backend platform focused on:

- document upload and text extraction
- chunking and RAG preparation
- embeddings and document indexing
- PostgreSQL metadata storage
- Redis and Qdrant infrastructure
- LangChain OpenAI embeddings integration
- MCP server layer
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
- `POST /documents/{document_id}/index`
- `POST /search`
- `POST /search/documents/{document_id}`
- `POST /ask`

### MCP Layer

- `search_documents` tool
- `ask_documents` tool
- `get_document_chunks` tool
- `documents://catalog` resource
- `document_qa_prompt` prompt template

### What Is Implemented Now

- document upload and file storage
- text extraction for `txt`, `md`, `pdf`, `docx`, `doc`, `xlsx`, `xls`
- chunk creation and chunk storage in PostgreSQL
- Alembic migrations for `documents` and `document_chunks`
- document indexing flow with OpenAI embeddings and Qdrant upsert
- semantic search endpoint for retrieving relevant chunks from Qdrant
- document-level semantic search
- RAG answer endpoint with sources
- MCP server built on top of the existing retrieval and RAG services
- document status pipeline: `uploaded -> stored -> processed -> chunked -> indexed`

### Current Flow

```text
upload -> store -> extract text -> chunk text -> index in Qdrant -> semantic search -> RAG answer
```

MCP flow:

```text
MCP client -> FastMCP server -> tools/resources/prompts -> existing app services
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

Run MCP server:

```bash
python scripts/run_mcp.py
```

Check MCP tools programmatically:

```bash
python scripts/check_mcp_tools.py
```

Example `search_documents` call through an MCP client:

```bash
python scripts/call_search_documents.py "your search query"
```
