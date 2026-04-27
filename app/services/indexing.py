from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.embeddings import embed_chunk_texts
from app.services.vector_store import upsert_chunks_to_qdrant


def index_document_chunks(db: Session, document: Document) -> int:
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document.id)
        .order_by(DocumentChunk.chunk_index.asc())
        .all()
    )

    if not chunks:
        raise ValueError("Document has no chunks. Run /chunk first.")

    chunk_texts = [chunk.content for chunk in chunks]
    vectors = embed_chunk_texts(chunk_texts)

    if len(vectors) != len(chunks):
        raise ValueError("Embedding count does not match chunk count")

    upsert_chunks_to_qdrant(
        document=document,
        chunks=chunks,
        vectors=vectors,
    )

    document.status = "indexed"
    db.commit()
    db.refresh(document)

    return len(chunks)
