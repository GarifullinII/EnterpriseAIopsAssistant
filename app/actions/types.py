from enum import Enum


class ActionType(str, Enum):
    LIST_DOCUMENTS = "list_documents"
    GET_DOCUMENT_STATUS = "get_document_status"
    TRIGGER_INGESTION_STEP = "trigger_ingestion_step"
