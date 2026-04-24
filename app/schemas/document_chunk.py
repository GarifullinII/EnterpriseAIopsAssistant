from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: str
    chunk_index: int
    content: str
    char_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
