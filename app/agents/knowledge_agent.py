from app.agents.types import QueryRoute
from app.services.retrieval import search_similar_chunks
from app.services.rag import answer_with_rag


def run_knowledge_agent(
    route: QueryRoute,
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> dict:
    if route == QueryRoute.SEARCH:
        results = search_similar_chunks(
            query=query,
            limit=limit,
            document_id=document_id,
        )
        return {
            "mode": "search",
            "results": results,
        }

    if route == QueryRoute.ASK:
        answer, sources = answer_with_rag(
            question=query,
            limit=limit,
        )
        return {
            "mode": "ask",
            "answer": answer,
            "sources": sources,
        }

    raise ValueError(f"Unsupported knowledge route: {route}")
