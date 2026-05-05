def run_action_agent(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> dict:
    return {
        "mode": "action",
        "message": "Action routing is ready, but backend actions will be implemented on Day 12.",
        "query": query,
        "document_id": document_id,
    }
