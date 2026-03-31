from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.document_model import DocumentModel
from .base_repository import BaseRepository, logger

class DocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "documents"

    def get_document(self, document_id: str) -> Optional[DocumentModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                data = doc_snapshot.to_dict()
                data['id'] = data.get('id', doc_snapshot.id) # VÁ LỖI THIẾU ID
                return DocumentModel(**data)
            logger.warning(f"Document with ID {document_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching document {document_id}: {e}")
            return None

    def get_all_documents(self) -> List[DocumentModel]:
        try:
            documents: List[DocumentModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                data = doc.to_dict()
                data['id'] = data.get('id', doc.id) # VÁ LỖI THIẾU ID
                documents.append(DocumentModel(**data))
            return documents
        except Exception as e:
            logger.error(f"Error fetching all documents: {e}")
            return []

    def create_document(self, document: DocumentModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(document.get_id()).set(
                {
                    "id": document.get_id(),
                    "docType": document.get_docType(),
                    "title": document.get_title(),
                    "ownerType": document.get_ownerType(),
                    "ownerId": document.get_ownerId(),
                    "storagePath": document.get_storagePath(),
                    "language": document.get_language(),
                    "createdAt": document.get_createdAt(),
                    "isActive": document.get_state(),
                }
            )
            logger.info(f"Document {document.get_id()} created successfully.")
            return document.get_id()
        except Exception as e:
            logger.error(f"Error creating document {document.get_id()}: {e}")
            return None

    def update_document(self, document: DocumentModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(document.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "docType": document.get_docType(),
                        "title": document.get_title(),
                        "ownerType": document.get_ownerType(),
                        "ownerId": document.get_ownerId(),
                        "storagePath": document.get_storagePath(),
                        "language": document.get_language(),
                        "createdAt": document.get_createdAt(),
                        "isActive": document.get_state(),
                    }
                )
                logger.info(f"Document {document.get_id()} updated successfully.")
                return True
            logger.warning(f"Document with ID {document.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating document {document.get_id()}: {e}")
            return False

    def delete_document(self, document_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Document {document_id} deleted successfully.")
                return True
            logger.warning(f"Document with ID {document_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False

    def block_document(self, document_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Document {document_id} blocked successfully.")
                return True
            logger.warning(f"Document with ID {document_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking document {document_id}: {e}")
            return False

    def unblock_document(self, document_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Document {document_id} unblocked successfully.")
                return True
            logger.warning(f"Document with ID {document_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking document {document_id}: {e}")
            return False
