from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.agents.orchestrator import handle_agent_query


router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/query", response_model=AgentQueryResponse)
def agent_query(payload: AgentQueryRequest) -> AgentQueryResponse:
    try:
        route, agent_name, result = handle_agent_query(
            query=payload.query,
            limit=payload.limit,
            document_id=payload.document_id,
        )

        return AgentQueryResponse(
            query=payload.query,
            route=route,
            agent=agent_name,
            result=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent query failed: {str(e)}")
