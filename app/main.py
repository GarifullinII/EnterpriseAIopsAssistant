from fastapi import FastAPI
from app.api.routes.documents import router as documents_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-style AI assistant with RAG, MCP, agents and workflows.",
)


@app.get("/")
async def root() -> dict:
    return {"message": "Enterprise AI Operations Assistant API is running"}


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "api",
        "version": settings.app_version,
        "database_host": settings.postgres_host,
    }


app.include_router(documents_router)
