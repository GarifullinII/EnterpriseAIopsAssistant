from pydantic import BaseModel, Field
from app.agents.types import QueryRoute


class AgentQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query")
    limit: int = Field(default=5, ge=1, le=20)
    document_id: str | None = None


class AgentQueryResponse(BaseModel):
    query: str
    route: QueryRoute
    agent: str
    result: dict
