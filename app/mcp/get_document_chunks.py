from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.document_queries import get_chunks_for_document, get_document_by_id
from app.mcp.server import mcp


class ChunkItem(BaseModel):
    id: int
    document_id: str
    chunk_index: int
    content: str
    char_count: int

    model_config = ConfigDict(from_attributes=True)


class DocumentChunksOutput(BaseModel):
    document_id: str
    chunks: list[ChunkItem]


@mcp.tool(
    title="Get Document Chunks",
    description=(
        "Fetch stored chunks for a specific document directly from PostgreSQL in "
        "their original chunk order."
    ),
)
def get_document_chunks(
    document_id: str = Field(description="Document ID"),
) -> DocumentChunksOutput:
    """Return all persisted chunks for one document."""
    db: Session = SessionLocal()
    try:
        document = get_document_by_id(db, document_id)
        if document is None:
            raise ValueError(f"Document not found: {document_id}")

        chunks = get_chunks_for_document(db, document_id)
        return DocumentChunksOutput(
            document_id=document_id,
            chunks=[ChunkItem.model_validate(chunk) for chunk in chunks],
        )
    finally:
        db.close()
