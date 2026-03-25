from typing import Any

from fastapi import APIRouter
from fastapi import Body
from fastapi import status


def build_router(prefix: str, tags: list[str], controller: Any) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("/")
    def get_all():
        return controller.get_all()

    @router.get("/{entity_id}")
    def get_one(entity_id: str):
        return controller.get_one(entity_id)

    @router.post("/", status_code=status.HTTP_201_CREATED)
    def create(payload: dict = Body(...)):
        return controller.create(payload)

    @router.put("/")
    def update(payload: dict = Body(...)):
        return controller.update(payload)

    @router.delete("/{entity_id}")
    def delete(entity_id: str):
        return controller.delete(entity_id)

    @router.patch("/{entity_id}/block")
    def block(entity_id: str):
        return controller.block(entity_id)

    @router.patch("/{entity_id}/unblock")
    def unblock(entity_id: str):
        return controller.unblock(entity_id)

    return router