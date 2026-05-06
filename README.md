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
- `POST /agent/query`
- `POST /workflows/trigger`

### MCP Layer

- `search_documents` tool
- `ask_documents` tool
- `get_document_chunks` tool
- `documents://catalog` resource
- `document_qa_prompt` prompt template

### Agent Layer

- basic rule-based router
- `knowledge_agent`
- `action_agent`
- route types: `search / ask / action`
- endpoint: `POST /agent/query`

### Actions Layer

- `list_documents`
- `get_document_status`
- `trigger_ingestion_step`
- backend action dispatch through `action_agent`

### Workflow Layer

- `POST /workflows/trigger`
- `ingestion_reindex` webhook workflow in n8n
- `document_processing` webhook workflow in n8n
- `notification_sync` webhook workflow in n8n
- backend workflow dispatch through `app/services/workflow_dispatcher.py`

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
- базовый agent routing layer для `search / ask / action`
- knowledge agent поверх retrieval и RAG сервисов
- actions layer с `list_documents`, `get_document_status`, `trigger_ingestion_step`
- action agent с backend action dispatch
- workflow dispatch layer for n8n webhook orchestration
- n8n workflows for ingestion/reindex, document processing, and notification sync
- pipeline статусов документа: `uploaded -> stored -> processed -> chunked -> indexed`

### Текущий Flow

```text
upload -> store -> extract text -> chunk text -> index in Qdrant -> semantic search -> RAG answer
```

MCP flow:

```text
MCP client -> FastMCP server -> tools/resources/prompts -> existing app services
```

Agent flow:

```text
User query -> router -> knowledge_agent or action_agent -> existing app services
```

Action flow:

```text
User action query -> agent router -> action_agent -> actions layer -> database/services
```

Workflow flow:

```text
Client/API -> workflow dispatcher -> n8n webhook -> backend document endpoints -> workflow summary
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

По умолчанию MCP server поднимается на `http://127.0.0.1:8100/mcp`.

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
- `POST /agent/query`
- `POST /workflows/trigger`

### MCP Layer

- `search_documents` tool
- `ask_documents` tool
- `get_document_chunks` tool
- `documents://catalog` resource
- `document_qa_prompt` prompt template

### Agent Layer

- basic rule-based router
- `knowledge_agent`
- `action_agent`
- route types: `search / ask / action`
- endpoint: `POST /agent/query`

### Actions Layer

- `list_documents`
- `get_document_status`
- `trigger_ingestion_step`
- backend action dispatch through `action_agent`

### Workflow Layer

- `POST /workflows/trigger`
- `ingestion_reindex` webhook workflow in n8n
- `document_processing` webhook workflow in n8n
- `notification_sync` webhook workflow in n8n
- backend workflow dispatch through `app/services/workflow_dispatcher.py`

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
- basic agent routing layer for `search / ask / action`
- knowledge agent on top of retrieval and RAG services
- actions layer with `list_documents`, `get_document_status`, and `trigger_ingestion_step`
- action agent with backend action dispatch
- workflow dispatch layer for n8n webhook orchestration
- n8n workflows for ingestion/reindex, document processing, and notification sync
- document status pipeline: `uploaded -> stored -> processed -> chunked -> indexed`

### Current Flow

```text
upload -> store -> extract text -> chunk text -> index in Qdrant -> semantic search -> RAG answer
```

MCP flow:

```text
MCP client -> FastMCP server -> tools/resources/prompts -> existing app services
```

Agent flow:

```text
User query -> router -> knowledge_agent or action_agent -> existing app services
```

Action flow:

```text
User action query -> agent router -> action_agent -> actions layer -> database/services
```

Workflow flow:

```text
Client/API -> workflow dispatcher -> n8n webhook -> backend document endpoints -> workflow summary
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

By default the MCP server is exposed at `http://127.0.0.1:8100/mcp`.

Check MCP tools programmatically:

```bash
python scripts/check_mcp_tools.py
```

Example `search_documents` call through an MCP client:

```bash
python scripts/call_search_documents.py "your search query"
```
