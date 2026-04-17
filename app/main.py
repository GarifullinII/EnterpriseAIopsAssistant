from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Enterprise AI Operations Assistant",
    version="0.1.0",
    description="Production-style AI assistant with RAG, MCP, agents and workflows.",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/")
async def root() -> dict:
    return {"message": "Enterprise AI Operations Assistant API is running"}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="api",
        version="0.1.0",
    )
