from types import NotImplementedType
from datetime import date

class FeedbackModel:
    def __init__(self, id: str, userId: str, messageId: str, rating: int, comment: str, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__userId = userId
        self.__messageId = messageId
        self.__rating = rating
        self.__comment = comment
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"FeedbackModel(id={self.__id}, userId={self.__userId}, messageId={self.__messageId}, rating={self.__rating}, comment={self.__comment}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FeedbackModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_userId(self, userId: str) -> None:
        self.__userId = userId

    def set_messageId(self, messageId: str) -> None:
        self.__messageId = messageId

    def set_rating(self, rating: int) -> None:
        self.__rating = rating

    def set_comment(self, comment: str) -> None:
        self.__comment = comment

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_userId(self) -> str:
        return self.__userId

    def get_messageId(self) -> str:
        return self.__messageId

    def get_rating(self) -> int:
        return self.__rating

    def get_comment(self) -> str:
        return self.__comment

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
