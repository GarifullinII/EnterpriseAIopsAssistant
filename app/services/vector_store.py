from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from app.core.config import settings
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        host=settings.resolved_qdrant_host,
        port=settings.qdrant_port,
    )


def ensure_collection_exists(vector_size: int) -> None:
    client = get_qdrant_client()
    collection_name = settings.qdrant_collection_name

    if client.collection_exists(collection_name):
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def build_points(
    document: Document,
    chunks: list[DocumentChunk],
    vectors: list[list[float]],
) -> list[PointStruct]:
    points: list[PointStruct] = []

    if len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors count mismatch")

    for chunk, vector in zip(chunks, vectors):
        payload = {
            "document_id": document.id,
            "chunk_id": chunk.id,
            "chunk_index": chunk.chunk_index,
            "title": document.title,
            "source": document.source,
            "content": chunk.content,
        }

        points.append(
            PointStruct(
                id=chunk.id,
                vector=vector,
                payload=payload,
            )
        )

    return points


def upsert_chunks_to_qdrant(
    document: Document,
    chunks: list[DocumentChunk],
    vectors: list[list[float]],
) -> None:
    if not vectors:
        raise ValueError("No vectors to upsert")
    
    if len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors count mismatch")

    vector_size = len(vectors[0])

    if any(len(vector) != vector_size for vector in vectors):
        raise ValueError("All vectors must have the same size")

    ensure_collection_exists(vector_size=vector_size)

    client = get_qdrant_client()
    points = build_points(document=document, chunks=chunks, vectors=vectors)

    client.upsert(
        collection_name=settings.qdrant_collection_name,
        points=points,
    )
