from types import NotImplementedType
from datetime import date

class ChatMessageModel:
    def __init__(self, id: str, sessionId: str, senderType: str, intent: str, content: str, citations: dict, entities: dict, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__sessionId = sessionId
        self.__senderType = senderType
        self.__intent = intent
        self.__content = content
        self.__citations = citations
        self.__entities = entities
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"ChatMessageModel(id={self.__id}, sessionId={self.__sessionId}, senderType={self.__senderType}, intent={self.__intent}, content={self.__content}, citations={self.__citations}, entities={self.__entities}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChatMessageModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_sessionId(self, sessionId: str) -> None:
        self.__sessionId = sessionId

    def set_senderType(self, senderType: str) -> None:
        self.__senderType = senderType

    def set_intent(self, intent: str) -> None:
        self.__intent = intent

    def set_content(self, content: str) -> None:
        self.__content = content

    def set_citations(self, citations: dict) -> None:
        self.__citations = citations

    def set_entities(self, entities: dict) -> None:
        self.__entities = entities

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_sessionId(self) -> str:
        return self.__sessionId

    def get_senderType(self) -> str:
        return self.__senderType

    def get_intent(self) -> str:
        return self.__intent

    def get_content(self) -> str:
        return self.__content

    def get_citations(self) -> dict:
        return self.__citations

    def get_entities(self) -> dict:
        return self.__entities

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
