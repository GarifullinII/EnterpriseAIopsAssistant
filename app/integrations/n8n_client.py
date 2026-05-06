import requests

from app.core.config import settings


def build_n8n_webhook_url(workflow_name: str) -> str:
    if workflow_name == "ingestion_reindex":
        return (
            f"{settings.resolved_n8n_base_url}"
            f"{settings.n8n_ingestion_webhook_path}"
        )

    if workflow_name == "document_processing":
        return (
            f"{settings.resolved_n8n_base_url}"
            f"{settings.n8n_document_processing_webhook_path}"
        )

    if workflow_name == "notification_sync":
        return (
            f"{settings.resolved_n8n_base_url}"
            f"{settings.n8n_notification_webhook_path}"
        )

    raise ValueError(f"Unsupported workflow: {workflow_name}")


def trigger_n8n_workflow(
    workflow_name: str,
    payload: dict,
    timeout_seconds: int = 30,
) -> dict:
    url = build_n8n_webhook_url(workflow_name)

    response = requests.post(
        url,
        json=payload,
        timeout=timeout_seconds,
    )
    response.raise_for_status()

    if response.content:
        return response.json()

    return {
        "status": "accepted",
        "status_code": response.status_code,
    }
