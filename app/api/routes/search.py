from fastapi import APIRouter, HTTPException
from app.schemas.search import SearchRequest, SearchResponse, SearchResultItem
from app.services.retrieval import search_similar_chunks


router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
def semantic_search(payload: SearchRequest) -> SearchResponse:
    try:
        results = search_similar_chunks(
            query=payload.query,
            limit=payload.limit,
        )

        return SearchResponse(
            query=payload.query,
            results=[SearchResultItem(**item) for item in results],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
