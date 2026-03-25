from api.controllers.document_chunk_controller import DocumentChunkController
from api.routers.router_factory import build_router


router = build_router(prefix="/document-chunks", tags=["Document Chunks"], controller=DocumentChunkController())