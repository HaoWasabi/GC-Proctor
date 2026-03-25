from types import NotImplementedType
from datetime import date


class RegulationModel:
    def __init__(self, id: str, regulationCode: str, title: str, version: str, effectiveDate: date, sourceUrl: str, updatedAt: date, isActive: bool = True):
        self.__id = id
        self.__regulationCode = regulationCode
        self.__title = title
        self.__version = version
        self.__effectiveDate = effectiveDate
        self.__sourceUrl = sourceUrl
        self.__updatedAt = updatedAt
        self.__isActive = isActive

    def __str__(self) -> str:
        return f"RegulationModel(id={self.__id}, regulationCode={self.__regulationCode}, title={self.__title}, version={self.__version}, effectiveDate={self.__effectiveDate}, sourceUrl={self.__sourceUrl}, updatedAt={self.__updatedAt}, isActive={self.__isActive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RegulationModel):
            return NotImplementedType
        return self.__id == other.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    def set_regulationCode(self, regulationCode: str) -> None:
        self.__regulationCode = regulationCode

    def set_title(self, title: str) -> None:
        self.__title = title

    def set_version(self, version: str) -> None:
        self.__version = version

    def set_effectiveDate(self, effectiveDate: date) -> None:
        self.__effectiveDate = effectiveDate

    def set_sourceUrl(self, sourceUrl: str) -> None:
        self.__sourceUrl = sourceUrl

    def set_updatedAt(self, updatedAt: date) -> None:
        self.__updatedAt = updatedAt

    def set_state(self, isActive: bool) -> None:
        self.__isActive = isActive

    def get_id(self) -> str:
        return self.__id

    def get_regulationCode(self) -> str:
        return self.__regulationCode

    def get_title(self) -> str:
        return self.__title

    def get_version(self) -> str:
        return self.__version

    def get_effectiveDate(self) -> date:
        return self.__effectiveDate

    def get_sourceUrl(self) -> str:
        return self.__sourceUrl

    def get_updatedAt(self) -> date:
        return self.__updatedAt

    def get_state(self) -> bool:
        return self.__isActive
