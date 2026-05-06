from sqlalchemy.orm import Session
from app.models.document import Document


def list_documents_action(db: Session, limit: int = 10) -> dict:
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "action": "list_documents",
        "documents": [
            {
                "id": doc.id,
                "title": doc.title,
                "status": doc.status,
                "source": doc.source,
                "created_at": doc.created_at.isoformat(),
            }
            for doc in documents
        ],
    }


def get_document_status_action(db: Session, document_id: str) -> dict:
    document = db.get(Document, document_id)

    if document is None:
        raise ValueError(f"Document not found: {document_id}")

    return {
        "action": "get_document_status",
        "document": {
            "id": document.id,
            "title": document.title,
            "status": document.status,
            "source": document.source,
            "created_at": document.created_at.isoformat(),
        },
    }
