from datetime import date
from datetime import datetime
from typing import Any
from typing import Type

from fastapi import HTTPException


class BaseEntityController:
    def __init__(
        self,
        service: Any,
        model_cls: Type,
        entity_name: str,
        get_one_method: str,
        get_all_method: str,
        create_method: str,
        update_method: str,
        delete_method: str,
        block_method: str,
        unblock_method: str,
    ):
        self.service = service
        self.model_cls = model_cls
        self.entity_name = entity_name
        self.get_one_method = get_one_method
        self.get_all_method = get_all_method
        self.create_method = create_method
        self.update_method = update_method
        self.delete_method = delete_method
        self.block_method = block_method
        self.unblock_method = unblock_method

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value

    def _model_to_dict(self, model: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for attr_name in dir(model):
            if not attr_name.startswith("get_"):
                continue

            getter = getattr(model, attr_name)
            if not callable(getter):
                continue

            field_name = attr_name[4:]
            if field_name == "state":
                field_name = "isActive"

            result[field_name] = self._serialize_value(getter())
        return result

    def _build_model(self, payload: dict[str, Any]):
        try:
            return self.model_cls(**payload)
        except TypeError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid payload: {exc}") from exc

    def get_one(self, entity_id: str) -> dict[str, Any]:
        method = getattr(self.service, self.get_one_method)
        entity = method(entity_id)
        if entity is None:
            raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")
        return self._model_to_dict(entity)

    def get_all(self) -> list[dict[str, Any]]:
        method = getattr(self.service, self.get_all_method)
        entities = method()
        return [self._model_to_dict(entity) for entity in entities]

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        method = getattr(self.service, self.create_method)
        entity = self._build_model(payload)
        created_id = method(entity)
        if not created_id:
            raise HTTPException(status_code=400, detail=f"Cannot create {self.entity_name}")
        return {"id": created_id, "message": f"{self.entity_name} created successfully"}

    def update(self, payload: dict[str, Any]) -> dict[str, Any]:
        method = getattr(self.service, self.update_method)
        entity = self._build_model(payload)
        updated = method(entity)
        if not updated:
            raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")
        return {"message": f"{self.entity_name} updated successfully"}

    def delete(self, entity_id: str) -> dict[str, Any]:
        method = getattr(self.service, self.delete_method)
        deleted = method(entity_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")
        return {"message": f"{self.entity_name} deleted successfully"}

    def block(self, entity_id: str) -> dict[str, Any]:
        method = getattr(self.service, self.block_method)
        blocked = method(entity_id)
        if not blocked:
            raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")
        return {"message": f"{self.entity_name} blocked successfully"}

    def unblock(self, entity_id: str) -> dict[str, Any]:
        method = getattr(self.service, self.unblock_method)
        unblocked = method(entity_id)
        if not unblocked:
            raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")
        return {"message": f"{self.entity_name} unblocked successfully"}