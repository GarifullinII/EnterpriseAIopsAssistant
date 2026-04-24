from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.schemas.document_chunk import DocumentChunkResponse


class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    source: str = Field(default="manual", max_length=100)


class DocumentResponse(BaseModel):
    id: str
    title: str
    source: str
    status: str

    original_filename: str | None = None
    file_path: str | None = None
    mime_type: str | None = None

    extracted_text: str | None = None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentWithChunksResponse(DocumentResponse):
    chunks: list[DocumentChunkResponse] = Field(default_factory=list)