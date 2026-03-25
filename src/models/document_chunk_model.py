from types import NotImplementedType
from datetime import date


class DocumentChunkModel:
    def __init__(self, id: str, documentId: str, chunkIndex: int, content: str, embeddingId: str, scoreThreshold: float, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__documentId = documentId
        self.__chunkIndex = chunkIndex
        self.__content = content
        self.__embeddingId = embeddingId
        self.__scoreThreshold = scoreThreshold
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"DocumentChunkModel(id={self.__id}, documentId={self.__documentId}, chunkIndex={self.__chunkIndex}, content={self.__content}, embeddingId={self.__embeddingId}, scoreThreshold={self.__scoreThreshold}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DocumentChunkModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_documentId(self, documentId: str) -> None:
        self.__documentId = documentId

    def set_chunkIndex(self, chunkIndex: int) -> None:
        self.__chunkIndex = chunkIndex

    def set_content(self, content: str) -> None:
        self.__content = content

    def set_embeddingId(self, embeddingId: str) -> None:
        self.__embeddingId = embeddingId

    def set_scoreThreshold(self, scoreThreshold: float) -> None:
        self.__scoreThreshold = scoreThreshold

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_documentId(self) -> str:
        return self.__documentId

    def get_chunkIndex(self) -> int:
        return self.__chunkIndex

    def get_content(self) -> str:
        return self.__content

    def get_embeddingId(self) -> str:
        return self.__embeddingId

    def get_scoreThreshold(self) -> float:
        return self.__scoreThreshold

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
