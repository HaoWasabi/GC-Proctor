from types import NotImplementedType
from datetime import date

class ExamScheduleModel:
    def __init__(self, id: str, examId: str, studentId: str, examDate: date, startTime: date, room: str, status: str, updatedAt: date, isActive: bool = True):
        self.__id = id
        self.__examId = examId
        self.__studentId = studentId
        self.__examDate = examDate
        self.__startTime = startTime
        self.__room = room
        self.__status = status
        self.__updatedAt = updatedAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"ExamScheduleModel(id={self.__id}, examId={self.__examId}, studentId={self.__studentId}, examDate={self.__examDate}, startTime={self.__startTime}, room={self.__room}, status={self.__status}, updatedAt={self.__updatedAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExamScheduleModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_examId(self, examId: str) -> None:
        self.__examId = examId

    def set_studentId(self, studentId: str) -> None:
        self.__studentId = studentId

    def set_examDate(self, examDate: date) -> None:
        self.__examDate = examDate

    def set_startTime(self, startTime: date) -> None:
        self.__startTime = startTime

    def set_room(self, room: str) -> None:
        self.__room = room

    def set_status(self, status: str) -> None:
        self.__status = status

    def set_updatedAt(self, updatedAt: date) -> None:
        self.__updatedAt = updatedAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_examId(self) -> str:
        return self.__examId

    def get_studentId(self) -> str:
        return self.__studentId

    def get_examDate(self) -> date:
        return self.__examDate

    def get_startTime(self) -> date:
        return self.__startTime

    def get_room(self) -> str:
        return self.__room

    def get_status(self) -> str:
        return self.__status

    def get_updatedAt(self) -> date:
        return self.__updatedAt

    def get_state(self) -> bool:
        return self.__isActive
