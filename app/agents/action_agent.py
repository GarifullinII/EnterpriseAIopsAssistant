from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.actions.router import detect_action_type
from app.actions.types import ActionType
from app.actions.document_actions import (
    list_documents_action,
    get_document_status_action,
)
from app.actions.ingestion_actions import trigger_ingestion_step_action


def extract_document_id_from_query(query: str) -> str | None:
    # MVP version: rely on explicit document_id from API when possible.
    return None


def run_action_agent(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> dict:
    action_type = detect_action_type(query)

    db: Session = SessionLocal()
    try:
        if action_type == ActionType.LIST_DOCUMENTS:
            return list_documents_action(db=db, limit=limit)

        if action_type == ActionType.GET_DOCUMENT_STATUS:
            if document_id is None:
                raise ValueError("document_id is required for get_document_status")
            return get_document_status_action(db=db, document_id=document_id)

        if action_type == ActionType.TRIGGER_INGESTION_STEP:
            if document_id is None:
                raise ValueError("document_id is required for trigger_ingestion_step")
            return trigger_ingestion_step_action(db=db, document_id=document_id)

        raise ValueError(f"Unsupported action type: {action_type}")
    finally:
        db.close()
