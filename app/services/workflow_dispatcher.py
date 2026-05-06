from app.integrations.n8n_client import trigger_n8n_workflow


SUPPORTED_WORKFLOWS = {
    "ingestion_reindex",
    "document_processing",
    "notification_sync",
}


def dispatch_workflow(
    workflow_name: str,
    document_id: str | None = None,
    payload: dict | None = None,
) -> dict:
    if workflow_name not in SUPPORTED_WORKFLOWS:
        raise ValueError(f"Unsupported workflow: {workflow_name}")

    final_payload = dict(payload or {})

    if document_id is not None:
        final_payload["document_id"] = document_id

    upstream_response = trigger_n8n_workflow(
        workflow_name=workflow_name,
        payload=final_payload,
    )

    return {
        "workflow_name": workflow_name,
        "status": "triggered",
        "message": f"Workflow '{workflow_name}' triggered successfully.",
        "upstream_response": upstream_response,
    }
