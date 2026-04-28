from qdrant_client.models import FieldCondition, Filter, MatchValue
from app.core.config import settings
from app.services.embeddings import embed_search_query
from app.services.vector_store import get_qdrant_client


def search_similar_chunks(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> list[dict]:
    client = get_qdrant_client()

    query_vector = embed_search_query(query)
    query_filter = None

    if document_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        )

    result = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=limit,
        query_filter=query_filter,
        with_payload=True,
    )

    items: list[dict] = []

    for point in result.points:
        payload = point.payload or {}

        items.append(
            {
                "document_id": payload.get("document_id"),
                "chunk_id": payload.get("chunk_id"),
                "chunk_index": payload.get("chunk_index"),
                "title": payload.get("title"),
                "source": payload.get("source"),
                "content": payload.get("content"),
                "score": point.score,
            }
        )

    return items
