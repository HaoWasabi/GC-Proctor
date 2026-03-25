from typing import List
from typing import Optional

from models.document_chunk_model import DocumentChunkModel
from repositories.document_chunk_repository import DocumentChunkRepository
from services.base_service import BaseService


class DocumentChunkService(BaseService):
    def __init__(self):
        super().__init__()
        self.document_chunk_repository = DocumentChunkRepository()

    def get_document_chunk(self, chunk_id: str) -> Optional[DocumentChunkModel]:
        return self.document_chunk_repository.get_document_chunk(chunk_id)

    def get_all_document_chunks(self) -> List[DocumentChunkModel]:
        return self.document_chunk_repository.get_all_document_chunks()

    def create_document_chunk(self, chunk: DocumentChunkModel) -> Optional[str]:
        return self.document_chunk_repository.create_document_chunk(chunk)

    def update_document_chunk(self, chunk: DocumentChunkModel) -> bool:
        return self.document_chunk_repository.update_document_chunk(chunk)

    def delete_document_chunk(self, chunk_id: str) -> bool:
        return self.document_chunk_repository.delete_document_chunk(chunk_id)

    def block_document_chunk(self, chunk_id: str) -> bool:
        return self.document_chunk_repository.block_document_chunk(chunk_id)

    def unblock_document_chunk(self, chunk_id: str) -> bool:
        return self.document_chunk_repository.unblock_document_chunk(chunk_id)