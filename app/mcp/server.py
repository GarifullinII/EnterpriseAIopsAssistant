from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "enterprise-aiops-assistant",
    json_response=True,
    stateless_http=True,
)


from app.mcp import ask_documents as _ask_documents
from app.mcp import get_document_chunks as _get_document_chunks
from app.mcp import prompt_template as _prompt_template
from app.mcp import resource as _resource
from app.mcp import search_documents as _search_documents


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
