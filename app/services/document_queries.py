from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def get_document_by_id(db: Session, document_id: str) -> Document | None:
    return db.get(Document, document_id)


def get_chunks_for_document(db: Session, document_id: str) -> list[DocumentChunk]:
    document = db.get(Document, document_id)
    if document is None:
        return []
    return document.chunks


def list_documents_basic(db: Session) -> list[Document]:
    return db.query(Document).order_by(Document.created_at.desc()).all()
