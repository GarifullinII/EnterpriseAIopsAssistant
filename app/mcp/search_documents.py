from pydantic import BaseModel, Field
from app.services.retrieval import search_similar_chunks
from app.mcp.server import mcp


class SearchDocumentsOutput(BaseModel):
    query: str
    results: list[dict]


@mcp.tool(
    title="Search Documents",
    description=(
        "Run semantic search across indexed document chunks and optionally limit "
        "the search to a single document."
    ),
)
def search_documents(
    query: str = Field(description="Semantic search query"),
    limit: int = Field(default=5, description="Maximum number of chunks to return"),
    document_id: str | None = Field(default=None, description="Optional document scope"),
) -> SearchDocumentsOutput:
    """Return the most relevant indexed chunks for a user query."""
    results = search_similar_chunks(
        query=query,
        limit=limit,
        document_id=document_id,
    )
    return SearchDocumentsOutput(query=query, results=results)
