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
    
    def _rewrite_query(self, user_query: str) -> str:
        """Kỹ thuật Advanced RAG: Viết lại câu hỏi lóng thành từ khóa chuẩn hành chính"""
        prompt = f"""
        Nhiệm vụ: Chuyển đổi câu hỏi của sinh viên thành các từ khóa/câu văn chuẩn mực trong quy chế đào tạo đại học để tìm kiếm tài liệu (Vector Search).
        Ví dụ: "rớt môn" -> "học lại, điểm F, thi lại"
        Ví dụ: "bảo lưu" -> "nghỉ học tạm thời, bảo lưu kết quả"
        Ví dụ: "đk hp" -> "đăng ký học phần, tín chỉ"
        
        Câu hỏi gốc: "{user_query}"
        Chỉ trả về DUY NHẤT một chuỗi chứa từ khóa chuẩn đã làm mịn:
        """
        try:
            return self.model.generate_content(prompt).text.strip()
        except:
            return user_query 

    def _retrieve_relevant_chunks(self, query: str) -> str:
        # (GIỮ NGUYÊN CODE CHUẨN CỦA HÀM NÀY NHƯ BẠN ĐÃ VIẾT - KHÔNG SỬA GÌ Ở ĐÂY)
        import unicodedata
        def normalize_text(text: str) -> str:
            nfd = unicodedata.normalize("NFD", text)
            return "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        
        if self.vector_store_ready and self.vector_store.index and len(self.vector_store.metadata) > 0:
            try:
                results = self.vector_store.search(query, k=5)
                if results:
                    filtered_results = [text for text, score in results if score > 0.3]
                    if filtered_results: return "\n\n".join(filtered_results)
            except Exception: pass
            
        try:
            chunks = self.chunk_repository.get_document_chunks_by_owner_type("regulation")
            if not chunks: return ""
            relevant_text = []
            query_words = [normalize_text(w.lower().strip()) for w in query.split() if w.strip()]
            for chunk in chunks:
                content_lower = normalize_text(chunk.get_content().lower())
                match_count = sum(1 for word in query_words if word in content_lower)
                if match_count >= 1: relevant_text.append((chunk.get_content(), match_count))
            relevant_text.sort(key=lambda x: x[1], reverse=True)
            return "\n\n".join([text for text, _ in relevant_text[:5]])
        except Exception: return ""

    def answer_regulation_question(self, user_query: str):
        """Luồng RAG thông minh kết hợp Query Rewriting và Chain-of-Thought"""
        
        # 1. Làm mịn câu hỏi trước khi search
        smart_query = self._rewrite_query(user_query)
        print(f"[RAG Logger] Dịch câu hỏi: '{user_query}' -> '{smart_query}'")
        
        # 2. Retrieval
        context = self._retrieve_relevant_chunks(smart_query)
        
        if not context:
            return "🛡️ Rất tiếc, mình không tìm thấy quy định cụ thể về vấn đề này trong cơ sở dữ liệu hiện tại của trường."

        # 3. Chain-of-Thought (CoT) Prompting
        prompt = f"""
        Bạn là GC-Proctor chuyên gia tư vấn Quy chế Đào tạo tại SGU.
        Ngữ cảnh quy chế thu thập được:
        {context}

        Câu hỏi của sinh viên: "{user_query}"

        HÃY SUY LUẬN TỪNG BƯỚC (Chain of Thought):
        Bước 1: Kiểm tra xem câu hỏi có chứa yếu tố chống phá, hỏi vặn, hoặc giải bài tập hộ không? Nếu có, hãy từ chối.
        Bước 2: Đối chiếu câu hỏi với Ngữ cảnh. Có thông tin trả lời không?
        Bước 3: Lập luận và tổng hợp câu trả lời ngắn gọn, trích dẫn rõ tên Điều/Khoản nếu có.
        Bước 4: Bỏ qua mọi thông tin học thuật dư thừa (code, bài giảng) có lẫn trong ngữ cảnh.

        Chỉ xuất ra CÂU TRẢ LỜI CUỐI CÙNG (Không in ra các bước suy luận của bạn).
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Lỗi kết nối AI: {str(e)}"
            
    def import_from_excel_batch(self, file_path: str):
        return self.regulation_repository.import_from_excel_batch(file_path)
