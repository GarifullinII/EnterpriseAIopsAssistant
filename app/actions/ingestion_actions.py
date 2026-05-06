from sqlalchemy.orm import Session
from app.models.document import Document
from app.services.extraction import extract_text_from_file


def trigger_ingestion_step_action(db: Session, document_id: str) -> dict:
    document = db.get(Document, document_id)

    if document is None:
        raise ValueError(f"Document not found: {document_id}")

    if not document.file_path:
        raise ValueError("Document has no file path")

    extracted_text = extract_text_from_file(document.file_path)

    document.extracted_text = extracted_text
    document.status = "processed"

    db.commit()
    db.refresh(document)

    return {
        "action": "trigger_ingestion_step",
        "document": {
            "id": document.id,
            "title": document.title,
            "status": document.status,
        },
    }
