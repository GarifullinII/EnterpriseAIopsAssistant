from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
    limit: int = Field(default=5, ge=1, le=10)


class AskSourceItem(BaseModel):
    document_id: str
    chunk_id: int
    chunk_index: int
    title: str
    source: str
    content: str
    score: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[AskSourceItem]
