from types import NotImplementedType
from datetime import date

class DocumentModel:
    def __init__(self, id: str, docType: str, title: str, ownerType: str, ownerId: str, storagePath: str, language: str, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__docType = docType
        self.__title = title
        self.__ownerType = ownerType
        self.__ownerId = ownerId
        self.__storagePath = storagePath
        self.__language = language
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"DocumentModel(id={self.__id}, docType={self.__docType}, title={self.__title}, ownerType={self.__ownerType}, ownerId={self.__ownerId}, storagePath={self.__storagePath}, language={self.__language}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DocumentModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_docType(self, docType: str) -> None:
        self.__docType = docType

    def set_title(self, title: str) -> None:
        self.__title = title

    def set_ownerType(self, ownerType: str) -> None:
        self.__ownerType = ownerType

    def set_ownerId(self, ownerId: str) -> None:
        self.__ownerId = ownerId

    def set_storagePath(self, storagePath: str) -> None:
        self.__storagePath = storagePath

    def set_language(self, language: str) -> None:
        self.__language = language

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_docType(self) -> str:
        return self.__docType

    def get_title(self) -> str:
        return self.__title

    def get_ownerType(self) -> str:
        return self.__ownerType

    def get_ownerId(self) -> str:
        return self.__ownerId

    def get_storagePath(self) -> str:
        return self.__storagePath

    def get_language(self) -> str:
        return self.__language

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
