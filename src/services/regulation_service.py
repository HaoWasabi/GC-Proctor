from typing import List
from typing import Optional

from models.regulation_model import RegulationModel
from repositories.regulation_repository import RegulationRepository
from repositories.document_chunk_repository import DocumentChunkRepository
from services.base_service import BaseService
from utils.vector_store_service import VectorStoreService


class RegulationService(BaseService):
    def __init__(self):
        super().__init__()
        self.regulation_repository = RegulationRepository()
        self.chunk_repository = DocumentChunkRepository()
        
        # Khởi tạo Vector Store Service cho RAG
        self.vector_store = VectorStoreService()
        self.vector_store_ready = self.vector_store.load_faiss_index()

    def get_regulation(self, regulation_id: str) -> Optional[RegulationModel]:
        return self.regulation_repository.get_regulation(regulation_id)

    def get_all_regulations(self) -> List[RegulationModel]:
        return self.regulation_repository.get_all_regulations()

    def create_regulation(self, regulation: RegulationModel) -> Optional[str]:
        return self.regulation_repository.create_regulation(regulation)

    def update_regulation(self, regulation: RegulationModel) -> bool:
        return self.regulation_repository.update_regulation(regulation)

    def delete_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.delete_regulation(regulation_id)

    def block_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.block_regulation(regulation_id)

    def unblock_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.unblock_regulation(regulation_id)
    
    def _retrieve_relevant_chunks(self, query: str) -> str:
        """
        Tìm kiếm các đoạn văn bản quy chế liên quan bằng Vector Search.
        
        Sử dụng FAISS + sentence-transformers để semantic search thay vì keyword matching.
        Nếu vector search không khả dụng, fallback sang keyword matching.
        
        Args:
            query: Câu hỏi từ user
            
        Returns:
            Chuỗi chứa top 5 chunks liên quan, ngăn cách bởi "\n\n"
        """
        import unicodedata

        def normalize_text(text: str) -> str:
            """Normalize Vietnamese text by removing diacritics."""
            nfd = unicodedata.normalize("NFD", text)
            return "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        
        # Ưu tiên dùng Vector Search nếu FAISS index sẵn sàng và có data
        if self.vector_store_ready and self.vector_store.index and len(self.vector_store.metadata) > 0:
            try:
                results = self.vector_store.search(query, k=5)
                
                if results:
                    # Filter kết quả có similarity > threshold
                    threshold = 0.3  # Có thể adjust threshold này
                    filtered_results = [text for text, score in results if score > threshold]
                    
                    if filtered_results:
                        context = "\n\n".join(filtered_results)
                        return context
                        
                # Nếu vector search không tìm thấy kết quả, fall through to keyword search
                print("⚠️  Vector search không tìm thấy kết quả, thử keyword search...")
                
            except Exception as e:
                print(f"⚠️  Lỗi Vector Search: {e}, fallback to keyword search")
        
        # Fallback: Dùng keyword matching nếu vector search không khả dụng hoặc không trả kết quả
        try:
            chunks = self.chunk_repository.get_all_document_chunks()
            
            if not chunks:
                return ""
            
            # Improved keyword matching: case-insensitive, normalize diacritics
            relevant_text = []
            query_words = [normalize_text(w.lower().strip()) for w in query.split() if w.strip()]
            
            for chunk in chunks:
                content_lower = normalize_text(chunk.get_content().lower())
                
                # Đếm số từ query xuất hiện trong chunk (substring match)
                match_count = sum(1 for word in query_words if word in content_lower)
                
                # Nếu match >= 1 từ query, thêm vào kết quả
                if match_count >= 1:
                    relevant_text.append((chunk.get_content(), match_count))
            
            # Sort by match count (descending), lấy top 5
            relevant_text.sort(key=lambda x: x[1], reverse=True)
            results = [text for text, _ in relevant_text[:5]]
            
            return "\n\n".join(results)
            
        except Exception as e:
            print(f"❌ Lỗi retrieval: {e}")
            return ""

    def answer_regulation_question(self, user_query: str):
        """Luồng RAG: Tra cứu quy chế và trả lời"""
        
        # 1. Retrieval: Tìm các đoạn quy chế liên quan
        context = self._retrieve_relevant_chunks(user_query)
        
        if not context:
            return ("Xin lỗi, mình không tìm thấy quy định cụ thể về vấn đề này trong tài liệu hiện có. "
                    "Bạn vui lòng xem thêm tại website của Phòng Đào tạo SGU nhé.")

        # 2. Augmentation & Generation
        prompt = f"""
        Bạn là chuyên gia về quy chế đào tạo tại Đại học Sài Gòn (SGU).
        Nhiệm vụ của bạn là giải đáp thắc mắc của sinh viên dựa trên các đoạn văn bản quy chế dưới đây.

        Ngữ cảnh quy chế:
        {context}

        Câu hỏi của sinh viên: "{user_query}"

        Yêu cầu:
        1. Trả lời chính xác, căn cứ vào nội dung được cung cấp.
        2. Trích dẫn rõ (ví dụ: "Theo Điều X...") nếu thông tin có sẵn trong ngữ cảnh.
        3. Nếu thông tin không có trong ngữ cảnh, hãy nói "Tôi không tìm thấy thông tin này trong quy chế hiện tại".
        4. Giọng điệu chuyên nghiệp, rõ ràng, dễ hiểu cho sinh viên.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Lỗi kết nối AI: {str(e)}"

    def import_from_excel_batch(self, file_path: str):
        return self.regulation_repository.import_from_excel_batch(file_path)