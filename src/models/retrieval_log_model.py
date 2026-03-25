from types import NotImplementedType
from datetime import date

class RetrievalLogModel:
    def __init__(self, id: str, messageId: str, chunkId: str, similarity: float, retrieverVersion: str, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__messageId = messageId
        self.__chunkId = chunkId
        self.__similarity = similarity
        self.__retrieverVersion = retrieverVersion
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"RetrievalLogModel(id={self.__id}, messageId={self.__messageId}, chunkId={self.__chunkId}, similarity={self.__similarity}, retrieverVersion={self.__retrieverVersion}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RetrievalLogModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_messageId(self, messageId: str) -> None:
        self.__messageId = messageId

    def set_chunkId(self, chunkId: str) -> None:
        self.__chunkId = chunkId

    def set_similarity(self, similarity: float) -> None:
        self.__similarity = similarity

    def set_retrieverVersion(self, retrieverVersion: str) -> None:
        self.__retrieverVersion = retrieverVersion

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_messageId(self) -> str:
        return self.__messageId

    def get_chunkId(self) -> str:
        return self.__chunkId

    def get_similarity(self) -> float:
        return self.__similarity

    def get_retrieverVersion(self) -> str:
        return self.__retrieverVersion

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
