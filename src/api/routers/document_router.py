from api.controllers.document_controller import DocumentController
from api.routers.router_factory import build_router


router = build_router(prefix="/documents", tags=["Documents"], controller=DocumentController())