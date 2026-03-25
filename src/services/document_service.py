from typing import List
from typing import Optional

from models.document_model import DocumentModel
from repositories.document_repository import DocumentRepository
from services.base_service import BaseService


class DocumentService(BaseService):
    def __init__(self):
        super().__init__()
        self.document_repository = DocumentRepository()

    def get_document(self, document_id: str) -> Optional[DocumentModel]:
        return self.document_repository.get_document(document_id)

    def get_all_documents(self) -> List[DocumentModel]:
        return self.document_repository.get_all_documents()

    def create_document(self, document: DocumentModel) -> Optional[str]:
        return self.document_repository.create_document(document)

    def update_document(self, document: DocumentModel) -> bool:
        return self.document_repository.update_document(document)

    def delete_document(self, document_id: str) -> bool:
        return self.document_repository.delete_document(document_id)

    def block_document(self, document_id: str) -> bool:
        return self.document_repository.block_document(document_id)

    def unblock_document(self, document_id: str) -> bool:
        return self.document_repository.unblock_document(document_id)