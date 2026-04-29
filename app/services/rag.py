from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.retrieval import search_similar_chunks


def get_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.chat_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )


def build_context_block(results: list[dict]) -> str:
    parts: list[str] = []

    for index, item in enumerate(results, start=1):
        parts.append(
            (
                f"[Source {index}]\n"
                f"Document ID: {item['document_id']}\n"
                f"Title: {item['title']}\n"
                f"Chunk Index: {item['chunk_index']}\n"
                f"Content:\n{item['content']}"
            )
        )

    return "\n\n".join(parts)


def answer_with_rag(question: str, limit: int = 5) -> tuple[str, list[dict]]:
    results = search_similar_chunks(
        query=question,
        limit=limit,
    )

    if not results:
        return (
            "I could not find relevant information in the indexed documents.",
            [],
        )

    context_block = build_context_block(results)

    system_prompt = (
        "You are an enterprise AI assistant."
        "Answer only from the provided context."
        "If the answer is not in the context, say that the information is not found."
        "Respond in the same language as the user's question."
        "Do not invent facts."
    )

    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context:\n{context_block}\n\n"
        "Provide a concise and helpful answer."
    )

    model = get_chat_model()

    response = model.invoke(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )

    return response.content, results
