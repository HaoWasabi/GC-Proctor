from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.document_chunk_model import DocumentChunkModel
from .base_repository import BaseRepository, logger


class DocumentChunkRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "document_chunks"

    def get_document_chunk(self, chunk_id: str) -> Optional[DocumentChunkModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(chunk_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return DocumentChunkModel(**doc_snapshot.to_dict())
            logger.warning(f"Document chunk with ID {chunk_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching document chunk {chunk_id}: {e}")
            return None

    def get_all_document_chunks(self) -> List[DocumentChunkModel]:
        try:
            chunks: List[DocumentChunkModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                chunks.append(DocumentChunkModel(**doc.to_dict()))
            return chunks
        except Exception as e:
            logger.error(f"Error fetching all document chunks: {e}")
            return []

    def create_document_chunk(self, chunk: DocumentChunkModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(chunk.get_id()).set(
                {
                    "id": chunk.get_id(),
                    "documentId": chunk.get_documentId(),
                    "chunkIndex": chunk.get_chunkIndex(),
                    "content": chunk.get_content(),
                    "embeddingId": chunk.get_embeddingId(),
                    "scoreThreshold": chunk.get_scoreThreshold(),
                    "createdAt": chunk.get_createdAt(),
                    "isActive": chunk.get_state(),
                }
            )
            logger.info(f"Document chunk {chunk.get_id()} created successfully.")
            return chunk.get_id()
        except Exception as e:
            logger.error(f"Error creating document chunk {chunk.get_id()}: {e}")
            return None

    def update_document_chunk(self, chunk: DocumentChunkModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(chunk.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "documentId": chunk.get_documentId(),
                        "chunkIndex": chunk.get_chunkIndex(),
                        "content": chunk.get_content(),
                        "embeddingId": chunk.get_embeddingId(),
                        "scoreThreshold": chunk.get_scoreThreshold(),
                        "createdAt": chunk.get_createdAt(),
                        "isActive": chunk.get_state(),
                    }
                )
                logger.info(f"Document chunk {chunk.get_id()} updated successfully.")
                return True
            logger.warning(f"Document chunk with ID {chunk.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating document chunk {chunk.get_id()}: {e}")
            return False

    def delete_document_chunk(self, chunk_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(chunk_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Document chunk {chunk_id} deleted successfully.")
                return True
            logger.warning(f"Document chunk with ID {chunk_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting document chunk {chunk_id}: {e}")
            return False

    def block_document_chunk(self, chunk_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(chunk_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Document chunk {chunk_id} blocked successfully.")
                return True
            logger.warning(f"Document chunk with ID {chunk_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking document chunk {chunk_id}: {e}")
            return False

    def unblock_document_chunk(self, chunk_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(chunk_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Document chunk {chunk_id} unblocked successfully.")
                return True
            logger.warning(f"Document chunk with ID {chunk_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking document chunk {chunk_id}: {e}")
            return False
