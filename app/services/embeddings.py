from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


_embeddings_client: OpenAIEmbeddings | None = None


def get_embeddings_client() -> OpenAIEmbeddings:
    global _embeddings_client

    if _embeddings_client is None:
        _embeddings_client = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )

    return _embeddings_client


def embed_chunk_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    embeddings_client = get_embeddings_client()
    return embeddings_client.embed_documents(texts)


def embed_search_query(query: str) -> list[float]:
    embeddings_client = get_embeddings_client()
    return embeddings_client.embed_query(query)
