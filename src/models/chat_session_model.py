from types import NotImplementedType
from datetime import date

class ChatSessionModel:
    def __init__(self, id: str, userId: str, channel: str, persona: str, sessionStatus: str, startedAt: date, endedAt: date, isActive: bool = True):
        self.__id = id
        self.__userId = userId
        self.__channel = channel
        self.__persona = persona
        self.__sessionStatus = sessionStatus
        self.__startedAt = startedAt
        self.__endedAt = endedAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"ChatSessionModel(id={self.__id}, userId={self.__userId}, channel={self.__channel}, persona={self.__persona}, sessionStatus={self.__sessionStatus}, startedAt={self.__startedAt}, endedAt={self.__endedAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChatSessionModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_userId(self, userId: str) -> None:
        self.__userId = userId

    def set_channel(self, channel: str) -> None:
        self.__channel = channel

    def set_persona(self, persona: str) -> None:
        self.__persona = persona

    def set_sessionStatus(self, sessionStatus: str) -> None:
        self.__sessionStatus = sessionStatus

    def set_startedAt(self, startedAt: date) -> None:
        self.__startedAt = startedAt

    def set_endedAt(self, endedAt: date) -> None:
        self.__endedAt = endedAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_userId(self) -> str:
        return self.__userId

    def get_channel(self) -> str:
        return self.__channel

    def get_persona(self) -> str:
        return self.__persona

    def get_sessionStatus(self) -> str:
        return self.__sessionStatus

    def get_startedAt(self) -> date:
        return self.__startedAt

    def get_endedAt(self) -> date:
        return self.__endedAt

    def get_state(self) -> bool:
        return self.__isActive
