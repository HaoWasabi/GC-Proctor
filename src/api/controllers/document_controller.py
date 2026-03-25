from api.controllers.base_entity_controller import BaseEntityController
from models.document_model import DocumentModel
from services.document_service import DocumentService


class DocumentController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=DocumentService(),
            model_cls=DocumentModel,
            entity_name="document",
            get_one_method="get_document",
            get_all_method="get_all_documents",
            create_method="create_document",
            update_method="update_document",
            delete_method="delete_document",
            block_method="block_document",
            unblock_method="unblock_document",
        )