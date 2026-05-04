from pydantic import BaseModel, Field
from app.services.rag import answer_with_rag
from app.mcp.server import mcp


class AskDocumentsOutput(BaseModel):
    question: str
    answer: str
    sources: list[dict]


@mcp.tool(
    title="Ask Documents",
    description=(
        "Answer a user question with RAG over indexed documents and return the "
        "grounded sources used for the answer."
    ),
)
def ask_documents(
    question: str = Field(description="Question to answer from indexed documents"),
    limit: int = Field(default=5, description="How many chunks to use"),
) -> AskDocumentsOutput:
    """Generate a grounded answer from indexed documents."""
    answer, sources = answer_with_rag(question=question, limit=limit)
    return AskDocumentsOutput(
        question=question,
        answer=answer,
        sources=sources,
    )
