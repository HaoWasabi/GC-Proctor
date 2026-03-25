from types import NotImplementedType
from datetime import date

class AuditLogModel:
    def __init__(self, id: str, actorUserId: str, actionType: str, targetCollection: str, targetId: str, metadata: dict, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__actorUserId = actorUserId
        self.__actionType = actionType
        self.__targetCollection = targetCollection
        self.__targetId = targetId
        self.__metadata = metadata
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"AuditLogModel(id={self.__id}, actorUserId={self.__actorUserId}, actionType={self.__actionType}, targetCollection={self.__targetCollection}, targetId={self.__targetId}, metadata={self.__metadata}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AuditLogModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_actorUserId(self, actorUserId: str) -> None:
        self.__actorUserId = actorUserId

    def set_actionType(self, actionType: str) -> None:
        self.__actionType = actionType

    def set_targetCollection(self, targetCollection: str) -> None:
        self.__targetCollection = targetCollection

    def set_targetId(self, targetId: str) -> None:
        self.__targetId = targetId

    def set_metadata(self, metadata: dict) -> None:
        self.__metadata = metadata

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_actorUserId(self) -> str:
        return self.__actorUserId

    def get_actionType(self) -> str:
        return self.__actionType

    def get_targetCollection(self) -> str:
        return self.__targetCollection

    def get_targetId(self) -> str:
        return self.__targetId

    def get_metadata(self) -> dict:
        return self.__metadata

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
