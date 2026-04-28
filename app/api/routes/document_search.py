from fastapi import APIRouter, HTTPException
from app.schemas.search import SearchRequest, SearchResponse, SearchResultItem
from app.services.retrieval import search_similar_chunks

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/documents/{document_id}", response_model=SearchResponse)
def semantic_search_in_document(
    document_id: str,
    payload: SearchRequest,
) -> SearchResponse:
    try:
        results = search_similar_chunks(
            query=payload.query,
            limit=payload.limit,
            document_id=document_id,
        )

        return SearchResponse(
            query=payload.query,
            results=[SearchResultItem(**item) for item in results],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document search failed: {str(e)}"
        )

