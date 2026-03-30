from typing import List
from typing import Optional

from models.regulation_model import RegulationModel
from repositories.regulation_repository import RegulationRepository
from repositories.document_chunk_repository import DocumentChunkRepository
from services.base_service import BaseService


class RegulationService(BaseService):
    def __init__(self):
        super().__init__()
        self.regulation_repository = RegulationRepository()
        self.chunk_repository = DocumentChunkRepository()

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
        Tìm kiếm các đoạn văn bản quy chế liên quan.
        Lưu ý: Ở bước này, thực tế bạn sẽ cần một Vector DB hoặc hàm tìm kiếm Similarity.
        Dưới đây là logic giả lập lấy các chunk từ Repository.
        """
        # Giả sử lấy toàn bộ chunk liên quan đến quy chế (trong thực tế sẽ dùng Vector Search)
        chunks = self.chunk_repository.get_all_document_chunks()
        
        # Filter hoặc tìm kiếm đơn giản (Đây là nơi bạn tích hợp Embedding/Vector Search)
        relevant_text = []
        for chunk in chunks:
            # Logic tạm thời: Nếu query có từ khóa xuất hiện trong chunk
            if any(word.lower() in chunk.get_content().lower() for word in query.split()):
                relevant_text.append(chunk.get_content())
        
        return "\n\n".join(relevant_text[:5]) # Lấy top 5 đoạn liên quan nhất

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
