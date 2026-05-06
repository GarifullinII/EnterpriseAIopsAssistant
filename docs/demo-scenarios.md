# Demo Scenarios

## Russian

### 1. Document Pipeline
- Upload a document through `POST /documents/upload`
- Run `process`, `chunk`, and `index`
- Show the document status changing from `stored` to `indexed`

### 2. Search and RAG
- Call `POST /search`
- Call `POST /ask`
- Show grounded answers with retrieved sources

### 3. Agent Routing
- Show a search-like query
- Show an ask-like query
- Show an action-like query
- Explain how the router selects `knowledge_agent` or `action_agent`

### 4. Workflow Layer
- Trigger `notification_sync` or `ingestion_reindex`
- Open the `n8n` execution view
- Show the orchestration across backend endpoints

### 5. MCP Layer
- Start the MCP server
- Run `python scripts/check_mcp_tools.py`
- Run `python scripts/call_search_documents.py "query"`

## English

### 1. Document Pipeline
- Upload a document through `POST /documents/upload`
- Run `process`, `chunk`, and `index`
- Show the document status moving from `stored` to `indexed`

### 2. Search and RAG
- Call `POST /search`
- Call `POST /ask`
- Show grounded answers with retrieved sources

### 3. Agent Routing
- Show a search-like query
- Show an ask-like query
- Show an action-like query
- Explain how the router selects `knowledge_agent` or `action_agent`

### 4. Workflow Layer
- Trigger `notification_sync` or `ingestion_reindex`
- Open the `n8n` execution view
- Show backend orchestration through webhook workflows

### 5. MCP Layer
- Start the MCP server
- Run `python scripts/check_mcp_tools.py`
- Run `python scripts/call_search_documents.py "query"`
