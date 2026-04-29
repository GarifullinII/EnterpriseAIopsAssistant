from fastapi import APIRouter, HTTPException
from app.schemas.ask import AskRequest, AskResponse, AskSourceItem
from app.services.rag import answer_with_rag


router = APIRouter(prefix="/ask", tags=["ask"])


@router.post("/", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    try:
        answer, sources = answer_with_rag(
            question=payload.question,
            limit=payload.limit,
        )

        return AskResponse(
            question=payload.question,
            answer=answer,
            sources=[AskSourceItem(**item) for item in sources],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG answer failed: {str(e)}")
