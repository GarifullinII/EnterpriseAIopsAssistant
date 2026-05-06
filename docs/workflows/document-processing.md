# Document Processing Workflow

Purpose:
Run the extraction and chunking stages without indexing.

Why this workflow exists:
- Some scenarios need preprocessing only.
- Keeping this separate from reindexing makes the flow easier to debug.
- It demonstrates that n8n can orchestrate shorter backend pipelines too.

Steps:
1. Receive `document_id` through `POST /webhook/document-processing`
2. Call `POST /documents/{document_id}/process`
3. Call `POST /documents/{document_id}/chunk`
4. Return a JSON summary through `Respond to Webhook`

Expected success response:
```json
{
  "status": "ok",
  "workflow": "document-processing",
  "document_id": "DOCUMENT_ID",
  "message": "Document processed and chunked successfully"
}
```
