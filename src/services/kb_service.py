from datetime import datetime  # Dùng datetime thay vì date
import uuid
from models.document_model import DocumentModel


class KBService:
    def __init__(self):
        from repositories.document_repository import DocumentRepository
        self.document_repository = DocumentRepository()

    def upload_document(self, file_path: str, course_code: str, title: str) -> dict:
        try:
            doc_id = str(uuid.uuid4())
            new_doc = DocumentModel(
                id=doc_id,
                docType="regulation",
                title=title,
                ownerType="course",
                ownerId=course_code,
                storagePath=file_path,
                language="vi",
                createdAt=datetime.now(), 
                isActive=True
            )

            result_id = self.document_repository.create_document(new_doc)

            if result_id:
                return {"documentId": result_id, "status": "success"}
            else:
                return {"status": "error", "message": "Failed to save to Firebase. Check console logs."}
        except Exception as e:
            return {"status": "error", "message": str(e)}