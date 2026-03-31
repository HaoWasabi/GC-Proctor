from datetime import datetime  # Dùng datetime thay vì date
import uuid
from models.document_model import DocumentModel


class KBService:
    def __init__(self):
        from repositories.document_repository import DocumentRepository
        self.document_repository = DocumentRepository()

    def retrieve_relevant_chunks(self, query: str, course_code: str) -> list:
        """
        Tìm kiếm các đoạn văn bản liên quan (Semantic Search).
        Trong đồ án, dùng FAISS hoặc ChromaDB tại đây.
        """
        try:
            # TODO: Triển khai logic Vector Search thật với LangChain & FAISS
            # Hiện tại: Lấy danh sách tài liệu từ Firestore để giả lập nội dung tìm thấy
            docs = self.document_repository.get_all_documents()
            # Lọc theo môn học
            relevant_docs = [d for d in docs if d.get_ownerId() == course_code or course_code == "ALL"]
            
            chunks = []
            for d in relevant_docs:
                chunks.append({
                    "content": f"Nội dung từ tài liệu '{d.get_title()}': ...", 
                    "metadata": {"source": d.get_title(), "id": d.get_id()}
                })
            return chunks
        except Exception as e:
            print(f"Error in KB Retrieval: {e}")
            return []


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