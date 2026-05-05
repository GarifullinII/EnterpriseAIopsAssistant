from enum import Enum


class QueryRoute(str, Enum):
    SEARCH = "search"
    ASK = "ask"
    ACTION = "action"
