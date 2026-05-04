from fastapi import FastAPI
from app.api.routes.document_search import router as document_search_router
from app.api.routes.documents import router as documents_router
from app.api.routes.search import router as search_router
from app.api.routes.ask import router as ask_router
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
        "database_host": settings.resolved_postgres_host,
    }


app.include_router(documents_router)
app.include_router(search_router)
app.include_router(document_search_router)
app.include_router(ask_router)
