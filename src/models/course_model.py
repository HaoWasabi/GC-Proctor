from datetime import date
from types import NotImplementedType


class CourseModel:
    def __init__(self, id: str, courseCode: str, courseName: str, faculty: str, semester: str, createdAt: date, isActive: bool = True):
        self.__id = id
        self.__courseCode = courseCode
        self.__courseName = courseName
        self.__faculty = faculty
        self.__semester = semester
        self.__createdAt = createdAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"CourseModel(id={self.__id}, courseCode={self.__courseCode}, courseName={self.__courseName}, faculty={self.__faculty}, semester={self.__semester}, createdAt={self.__createdAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CourseModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_courseCode(self, courseCode: str) -> None:
        self.__courseCode = courseCode

    def set_courseName(self, courseName: str) -> None:
        self.__courseName = courseName

    def set_faculty(self, faculty: str) -> None:
        self.__faculty = faculty

    def set_semester(self, semester: str) -> None:
        self.__semester = semester

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_courseCode(self) -> str:
        return self.__courseCode

    def get_courseName(self) -> str:
        return self.__courseName

    def get_faculty(self) -> str:
        return self.__faculty

    def get_semester(self) -> str:
        return self.__semester

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_state(self) -> bool:
        return self.__isActive
