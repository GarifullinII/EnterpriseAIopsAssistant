# Ingestion Reindex Workflow

Purpose:
Run the full document ingestion pipeline from a single webhook trigger.

Why this workflow exists:
- The backend already owns the document-processing logic.
- n8n should orchestrate the sequence, not duplicate chunking/indexing logic.
- Splitting `process -> chunk -> index` into separate steps makes failures visible.

Steps:
1. Receive `document_id` through `POST /webhook/ingestion-reindex`
2. Call `POST /documents/{document_id}/process`
3. Call `POST /documents/{document_id}/chunk`
4. Call `POST /documents/{document_id}/index`
5. Return a JSON summary through `Respond to Webhook`

Expected success response:
```json
{
  "status": "ok",
  "workflow": "ingestion-reindex",
  "document_id": "DOCUMENT_ID",
  "message": "Document processed, chunked, and indexed successfully"
}
```
