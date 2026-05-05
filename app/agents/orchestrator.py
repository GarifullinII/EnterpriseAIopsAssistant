from app.agents.router import detect_route
from app.agents.types import QueryRoute
from app.agents.knowledge_agent import run_knowledge_agent
from app.agents.action_agent import run_action_agent


def handle_agent_query(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> tuple[QueryRoute, str, dict]:
    route = detect_route(query)

    if route in {QueryRoute.SEARCH, QueryRoute.ASK}:
        result = run_knowledge_agent(
            route=route,
            query=query,
            limit=limit,
            document_id=document_id,
        )
        return route, "knowledge_agent", result

    if route == QueryRoute.ACTION:
        result = run_action_agent(
            query=query,
            limit=limit,
            document_id=document_id,
        )
        return route, "action_agent", result

    raise ValueError(f"Unsupported route: {route}")
