from app.agents.types import QueryRoute


SEARCH_KEYWORDS = {
    "find",
    "search",
    "look up",
    "найди",
    "найти",
    "поиск",
}

ACTION_KEYWORDS = {
    "run",
    "trigger",
    "start",
    "execute",
    "reindex",
    "process",
    "ingest",
    "update status",
    "запусти",
    "выполни",
    "переиндексируй",
    "обнови",
    "обработай",
    "show documents",
    "list documents",
    "show all documents",
    "покажи документы",
    "покажи все документы",
    "список документов",
    "document status",
    "get status",
    "check status",
    "статус документа",
    "проверь статус",
    "какой статус",
    "process document",
    "ingest document",
    "обработай документ",
}


def normalize_query(text: str) -> str:
    return text.strip().lower()


def detect_route(query: str) -> QueryRoute:
    normalized = normalize_query(query)

    if any(keyword in normalized for keyword in ACTION_KEYWORDS):
        return QueryRoute.ACTION

    if any(keyword in normalized for keyword in SEARCH_KEYWORDS):
        return QueryRoute.SEARCH

    return QueryRoute.ASK
