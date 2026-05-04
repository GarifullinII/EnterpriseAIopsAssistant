from app.mcp.server import mcp


@mcp.prompt(
    title="Document QA Prompt",
    description="Guide an MCP client to search documents first and answer only from retrieved evidence.",
)
def document_qa_prompt(user_question: str) -> str:
    """Template for grounded question answering over indexed documents."""
    return (
        "You are a document assistant.\n"
        "First, use search_documents to find relevant chunks.\n"
        "Then use ask_documents if a grounded answer is needed.\n"
        "If the information is missing, say it explicitly.\n\n"
        f"User question: {user_question}"
    )
