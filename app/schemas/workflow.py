from pydantic import BaseModel, Field


class TriggerWorkflowRequest(BaseModel):
    workflow_name: str = Field(..., min_length=1)
    document_id: str | None = None
    payload: dict = Field(default_factory=dict)


class TriggerWorkflowResponse(BaseModel):
    workflow_name: str
    status: str
    message: str
    upstream_response: dict | None = None
