import os
import uuid
import base64
from datetime import datetime
from pathlib import Path
import fitz
import docx
from models.document_model import DocumentModel
from models.document_chunk_model import DocumentChunkModel
from repositories.document_repository import DocumentRepository
from repositories.document_chunk_repository import DocumentChunkRepository
from utils.vector_store_service import VectorStoreService


class KBService:
    def __init__(self):
        self.document_repository = DocumentRepository()
        self.chunk_repository = DocumentChunkRepository()
        self.vector_store = VectorStoreService()
        self.vector_store.load_faiss_index()

    def _extract_text(self, file_path: str, filename: str) -> str:
        """Đọc chữ từ file PDF hoặc DOCX bằng PyMuPDF (Mạnh hơn PyPDF2 rất nhiều)"""
        text = ""
        try:
            if filename.lower().endswith('.pdf'):
                # Sử dụng fitz (PyMuPDF) để đọc PDF
                with fitz.open(file_path) as doc:
                    for page in doc:
                        extracted = page.get_text() # Lấy text chuẩn xác hơn
                        if extracted:
                            text += extracted + "\n"
            elif filename.lower().endswith('.docx'):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
        except Exception as e:
            print(f"Lỗi khi đọc text từ file: {e}")
        return text

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
        """Cắt chữ thành nhiều đoạn nhỏ"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def retrieve_relevant_chunks(self, query: str, course_code: str) -> list:
        """Thực hiện Vector Search thật sự với FAISS"""
        try:
            if self.vector_store.index is None:
                self.vector_store.load_faiss_index()
                
            # Lấy danh sách Document ID hợp lệ theo môn học
            valid_doc_ids = set()
            docs = self.document_repository.get_all_documents()
            for d in docs:
                if d.get_ownerId() == course_code.upper():
                    valid_doc_ids.add(d.get_id())
            
            # Vector Search (Lấy ra 15 kết quả giống nhất đề phòng bị lọc)
            raw_results = self.vector_store.search_with_citations(query, k=15)
            
            chunks = []
            for res in raw_results:
                doc_id = res['citation'].get('documentId')
                
                # Bỏ qua nếu document không thuộc môn học này
                # (Chỉ lọc nếu valid_doc_ids có dữ liệu, tránh trường hợp DB lỗi làm mất hết kết quả)
                if course_code != "ALL" and len(valid_doc_ids) > 0 and doc_id not in valid_doc_ids:
                    continue
                    
                chunks.append({
                    "content": res['text'],
                    "metadata": res['citation']
                })
                
                if len(chunks) >= 5:
                    break
                    
            return chunks
            
        except Exception as e:
            print(f"Error in KB Retrieval: {e}")
            return []


    def upload_document(self, file_path: str, course_code: str, title: str) -> dict:
        try:
            doc_id = str(uuid.uuid4())
            
            tmp_dir = Path("tmp/uploads")
            tmp_dir.mkdir(parents=True, exist_ok=True)
            
            ext = ".pdf" if ".pdf" in title.lower() else ".docx" if ".docx" in title.lower() else ".pdf"
            temp_file_path = tmp_dir / f"{doc_id}{ext}"
            
            file_bytes = base64.b64decode(file_path)
            with open(temp_file_path, "wb") as f:
                f.write(file_bytes)

            extracted_text = self._chunk_text(self._extract_text(str(temp_file_path), title), 1000, 200)
            
            if not extracted_text:
                return {"status": "error", "message": "Không thể trích xuất chữ. File bị rỗng hoặc là ảnh scan."}

            # Lưu Document Model
            new_doc = DocumentModel(
                id=doc_id,
                docType="study_material",
                title=title,
                ownerType="course",
                ownerId=course_code.upper(),
                storagePath=str(temp_file_path),
                language="vi",
                createdAt=datetime.now(), 
                isActive=True
            )
            self.document_repository.create_document(new_doc)

            # Lưu Document Chunk Model
            for i, chunk_text in enumerate(extracted_text):
                chunk_id = f"{doc_id}_chunk_{i}"
                
                # BỔ SUNG ĐẦY ĐỦ THAM SỐ CHO MODEL CỦA BẠN ĐỂ KHÔNG BỊ CRASH
                new_chunk = DocumentChunkModel(
                    id=chunk_id,
                    documentId=doc_id,
                    chunkIndex=i,
                    content=chunk_text,
                    embeddingId="faiss_auto",   # Bổ sung tham số bị thiếu
                    scoreThreshold=0.0,         # Bổ sung tham số bị thiếu
                    createdAt=datetime.now(),
                    isActive=True
                )
                self.chunk_repository.create_document_chunk(new_chunk)

            # Rebuild FAISS Index
            from utils.index_builder import rebuild_faiss_from_firestore
            success = rebuild_faiss_from_firestore()
            
            # Load lại FAISS vào RAM
            self.vector_store.load_faiss_index()

            if success:
                return {"documentId": doc_id, "status": "success", "message": f"Đã học xong! Tạo thành công {len(extracted_text)} chunks kiến thức."}
            else:
                return {"status": "error", "message": "Đã lưu text nhưng tạo FAISS Index thất bại."}
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}