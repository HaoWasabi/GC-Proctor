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
                parsed_chunk = self._parse_chunk(doc)
                if parsed_chunk:
                    chunks.append(parsed_chunk)
            return chunks
        except Exception as e:
            logger.error(f"Error fetching all document chunks: {e}")
            return []

    def get_document_chunks_by_owner_type(self, owner_type: str) -> List[DocumentChunkModel]:
        """
        Lấy chunks theo ownerType của document (ví dụ: 'regulation', 'course').
        """
        try:
            # Lấy danh sách document IDs theo ownerType trước.
            document_ids: List[str] = []
            documents_query = self.db.collection("documents").where("ownerType", "==", owner_type).stream()
            for document in documents_query:
                document_ids.append(document.id)

            if not document_ids:
                return []

            chunks: List[DocumentChunkModel] = []

            # Firestore giới hạn tối đa 10 phần tử cho toán tử 'in'.
            for i in range(0, len(document_ids), 10):
                batch_ids = document_ids[i:i + 10]
                chunk_docs = (
                    self.db.collection(self.collection_name)
                    .where("documentId", "in", batch_ids)
                    .stream()
                )

                for doc in chunk_docs:
                    parsed_chunk = self._parse_chunk(doc)
                    if parsed_chunk:
                        chunks.append(parsed_chunk)

            return chunks
        except Exception as e:
            logger.error(f"Error fetching document chunks by ownerType={owner_type}: {e}")
            return []

    def _parse_chunk(self, doc: DocumentSnapshot) -> Optional[DocumentChunkModel]:
        data = doc.to_dict() or {}

        # Support mixed schema and skip malformed docs instead of failing entire retrieval.
        normalized = {
            "id": data.get("id") or doc.id,
            "documentId": data.get("documentId") or data.get("document_id") or "",
            "chunkIndex": data.get("chunkIndex") if data.get("chunkIndex") is not None else data.get("chunk_index", 0),
            "content": data.get("content") or "",
            "embeddingId": data.get("embeddingId") or data.get("embedding_id") or "",
            "scoreThreshold": data.get("scoreThreshold") if data.get("scoreThreshold") is not None else data.get("score_threshold", 0.0),
            "createdAt": data.get("createdAt") or data.get("created_at"),
            "isActive": data.get("isActive", True),
        }

        # Minimum required fields to be useful for retrieval.
        if not normalized["documentId"] or not normalized["content"] or not normalized["createdAt"]:
            logger.warning(
                "Skip malformed chunk doc id=%s keys=%s",
                doc.id,
                sorted(list(data.keys())),
            )
            return None

        try:
            return DocumentChunkModel(**normalized)
        except Exception as parse_err:
            logger.warning(
                "Skip invalid chunk doc id=%s parse_error=%s",
                doc.id,
                parse_err,
            )
            return None

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
