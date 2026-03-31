import json
from services.base_service import BaseService
from services.kb_service import KBService
from repositories.study_repository import StudyRepository # Bổ sung import

class StudyService(BaseService):
    """CLEAN Study Service - handles RAG + LLM for study support using Real API"""

    def __init__(self):
        super().__init__()
        self.kb_service = KBService()
        self.study_repo = StudyRepository() # Khởi tạo repository để dùng cho get_recommendations

    def process_study_workflow(self, question: str, user_info: dict, upcoming_exams: list) -> dict:
        # ... [Giữ nguyên nội dung hàm process_study_workflow tôi đã cung cấp ở câu trả lời trước] ...
        pass

    # ==========================================
    # KHÔI PHỤC LẠI CÁC HÀM BỊ THIẾU TỪ FILE GỐC
    # ==========================================

    def get_recommendations(self, course_code: str):
        """Lấy danh sách tài liệu từ Firebase"""
        return self.study_repo.get_materials_by_course(course_code)

    def generate_flashcards(self, course_code: str, topic: str, num_cards: int = 10) -> dict:
        """Standalone flashcard generator"""
        chunks = self.kb_service.retrieve_relevant_chunks(topic, course_code)

        if not chunks:
            # SỬA Ở ĐÂY: Thêm status và message
            return {"status": "error", "flashcards": [], "message": "Không tìm thấy tài liệu phù hợp để tạo flashcards."}

        context = "\n".join([c.get("content", "") for c in chunks])

        prompt = f"""
        Tạo {num_cards} flashcard về chủ đề: {topic}
        Dựa trên tài liệu:
        {context}
        Format: TRẢ VỀ CHỈ MỘT CHUỖI JSON HỢP LỆ với các object có cấu trúc {{"question": "...", "answer": "..."}}
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
            flashcards_data = json.loads(response_text)
            
            # Đảm bảo flashcards_data là một list
            final_cards = flashcards_data if isinstance(flashcards_data, list) else flashcards_data.get("flashcards", [])
            
            # SỬA Ở ĐÂY: Trả về trạng thái thành công
            return {
                "status": "success",
                "flashcards": final_cards
            }
            
        except Exception as e:
            print(f"[DEBUG] Error parsing flashcards JSON: {e}")
            # SỬA Ở ĐÂY: Trả về trạng thái lỗi nếu quá trình AI parse gặp sự cố
            return {
                "status": "error",
                "flashcards": [],
                "message": f"Lỗi trong quá trình tạo flashcards từ AI."
            }

    def summarize_material(self, course_code: str, length: str = "short") -> dict:
        """Generate course summary"""
        chunks = self.kb_service.retrieve_relevant_chunks(f"Tóm tắt {course_code}", course_code)
        context = "\n".join([c.get("content", "") for c in chunks])

        length_guide = {
            "short": "100-200 từ",
            "medium": "300-500 từ",
            "long": "800+ từ"
        }

        prompt = f"""
        Tóm tắt tài liệu của môn {course_code} trong khoảng {length_guide.get(length, length_guide['short'])}:
        TÀI LIỆU:
        {context}
        """

        response = self.model.generate_content(prompt)
        return {"summary": response.text, "length": length}

