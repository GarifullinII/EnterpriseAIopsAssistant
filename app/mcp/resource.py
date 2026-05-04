from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.document_queries import list_documents_basic
from app.mcp.server import mcp


@mcp.resource(
    "documents://catalog",
    name="documents_catalog",
    title="Documents Catalog",
    description="Read-only catalog of known documents with ids, titles, sources, and statuses.",
)
def documents_catalog() -> str:
    """Render a plain-text catalog of documents for MCP clients."""
    db: Session = SessionLocal()
    try:
        documents = list_documents_basic(db)
        if not documents:
            return "No documents found."

        lines = []
        for doc in documents:
            lines.append(
                f"id={doc.id} | title={doc.title} | status={doc.status} | source={doc.source}"
            )
        return "\n".join(lines)
    finally:
        db.close()
