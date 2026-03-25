from datetime import date
from types import NotImplementedType


class ExamModel:
    def __init__(self, id: str, courseId: str, examType: str, durationMinutes: int, policyVersion: str, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__courseId = courseId
        self.__examType = examType
        self.__durationMinutes = durationMinutes
        self.__policyVersion = policyVersion
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"ExamModel(id={self.__id}, courseId={self.__courseId}, examType={self.__examType}, durationMinutes={self.__durationMinutes}, policyVersion={self.__policyVersion}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExamModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_courseId(self, courseId: str) -> None:
        self.__courseId = courseId

    def set_examType(self, examType: str) -> None:
        self.__examType = examType

    def set_durationMinutes(self, durationMinutes: int) -> None:
        self.__durationMinutes = durationMinutes

    def set_policyVersion(self, policyVersion: str) -> None:
        self.__policyVersion = policyVersion

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_courseId(self) -> str:
        return self.__courseId

    def get_examType(self) -> str:
        return self.__examType

    def get_durationMinutes(self) -> int:
        return self.__durationMinutes

    def get_policyVersion(self) -> str:
        return self.__policyVersion

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
