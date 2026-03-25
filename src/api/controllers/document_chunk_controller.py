from api.controllers.base_entity_controller import BaseEntityController
from models.document_chunk_model import DocumentChunkModel
from services.document_chunk_service import DocumentChunkService


class DocumentChunkController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=DocumentChunkService(),
            model_cls=DocumentChunkModel,
            entity_name="document_chunk",
            get_one_method="get_document_chunk",
            get_all_method="get_all_document_chunks",
            create_method="create_document_chunk",
            update_method="update_document_chunk",
            delete_method="delete_document_chunk",
            block_method="block_document_chunk",
            unblock_method="unblock_document_chunk",
        )