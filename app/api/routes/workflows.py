from fastapi import APIRouter, HTTPException

from app.schemas.workflow import TriggerWorkflowRequest, TriggerWorkflowResponse
from app.services.workflow_dispatcher import dispatch_workflow


router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.post("/trigger", response_model=TriggerWorkflowResponse)
def trigger_workflow(payload: TriggerWorkflowRequest) -> TriggerWorkflowResponse:
    try:
        result = dispatch_workflow(
            workflow_name=payload.workflow_name,
            document_id=payload.document_id,
            payload=payload.payload,
        )

        return TriggerWorkflowResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow trigger failed: {str(e)}",
        )
