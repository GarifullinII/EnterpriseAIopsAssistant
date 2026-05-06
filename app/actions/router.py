from app.actions.types import ActionType


LIST_DOCUMENTS_KEYWORDS = {
    "list documents",
    "show documents",
    "show all documents",
    "список документов",
    "покажи документы",
    "покажи все документы",
}

GET_DOCUMENT_STATUS_KEYWORDS = {
    "document status",
    "get status",
    "check status",
    "статус документа",
    "проверь статус",
    "какой статус",
}

TRIGGER_INGESTION_KEYWORDS = {
    "trigger ingestion",
    "run ingestion",
    "start ingestion",
    "process document",
    "ingest document",
    "запусти ingestion",
    "запусти обработку",
    "обработай документ",
}


def normalize_action_query(text: str) -> str:
    return text.strip().lower()


def detect_action_type(query: str) -> ActionType:
    normalized = normalize_action_query(query)

    if any(keyword in normalized for keyword in LIST_DOCUMENTS_KEYWORDS):
        return ActionType.LIST_DOCUMENTS

    if any(keyword in normalized for keyword in GET_DOCUMENT_STATUS_KEYWORDS):
        return ActionType.GET_DOCUMENT_STATUS

    if any(keyword in normalized for keyword in TRIGGER_INGESTION_KEYWORDS):
        return ActionType.TRIGGER_INGESTION_STEP

    raise ValueError(f"Unsupported action query: {query}")
