from enum import Enum

class StateEnum(Enum):
    START = "START"
    READY = "READY"
    WORKING = "WORKING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"
    END = "END"

    IS_SPORT_RELATED = "is_sport_related"

    MESSAGE = "messages"