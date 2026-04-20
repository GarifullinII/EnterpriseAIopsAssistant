import os
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Enterprise AI Operations Assistant",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    postgres_host: str
    redis_host: str
    qdrant_host: str


@app.get("/")
async def root() -> dict:
    return {"message": "Enterprise AI Operations Assistant API is running"}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="api",
        version=os.getenv("APP_VERSION", "0.1.0"),
        postgres_host=os.getenv("POSTGRES_HOST", "unknown"),
        redis_host=os.getenv("REDIS_HOST", "unknown"),
        qdrant_host=os.getenv("QDRANT_HOST", "unknown"),
    )
