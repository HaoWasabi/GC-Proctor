from types import NotImplementedType
from datetime import date

class UserModel:
    def __init__(self, id: str, userCode: str, role: str, fullName: str, email: str, authProvider: str, password: str, createdAt: date, updatedAt: date, isActive=True):
        self.__id = id
        self.__userCode = userCode
        self.__role = role
        self.__fullName = fullName
        self.__email = email
        self.__authProvider = authProvider
        self.__password = password
        self.__createdAt = createdAt
        self.__updatedAt = updatedAt
        self.__isActive = isActive
        
    def __str__(self) -> str:
        return f"UserModel(id={self.__id}, userCode={self.__userCode}, role={self.__role}, fullName={self.__fullName}, email={self.__email}, authProvider={self.__authProvider}, password={self.__password}, createdAt={self.__createdAt}, updatedAt={self.__updatedAt}, isActive={self.__isActive})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserModel):
            return NotImplementedType
        return self.__id == other.__id
    
    def set_id(self, id: str) -> None:
        self.__id = id

    def set_userCode(self, userCode: str) -> None:
        self.__userCode = userCode

    def set_role(self, role: str) -> None:
        self.__role = role

    def set_fullName(self, fullName: str) -> None:
        self.__fullName = fullName

    def set_email(self, email: str) -> None:
        self.__email = email

    def set_authProvider(self, authProvider: str) -> None:
        self.__authProvider = authProvider

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_createdAt(self, createdAt: date) -> None:
        self.__createdAt = createdAt

    def set_updatedAt(self, updatedAt: date) -> None:
        self.__updatedAt = updatedAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_userCode(self) -> str:
        return self.__userCode

    def get_role(self) -> str:
        return self.__role

    def get_fullName(self) -> str:
        return self.__fullName

    def get_email(self) -> str:
        return self.__email

    def get_authProvider(self) -> str:
        return self.__authProvider

    def get_password(self) -> str:
        return self.__password

    def get_createdAt(self) -> date:
        return self.__createdAt

    def get_updatedAt(self) -> date:
        return self.__updatedAt

    def get_state(self) -> bool:
        return self.__isActive
        