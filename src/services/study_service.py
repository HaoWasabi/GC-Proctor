import json
from services.kb_service import KBService
from services.nlp_service import NLPService


class StudyService:
    def __init__(self):
        self.kb_service = KBService()
        self.nlp_service = NLPService()

    def process_study_workflow(self, question: str, user_info: dict, upcoming_exams: list) -> dict:
        # RAG đọc lịch thi -> Suy luận môn thi
        # Ép kiểu dữ liệu lịch thi thành text để đưa vào LLM suy luận (RAG on Data)
        schedule_text = json.dumps(upcoming_exams, ensure_ascii=False)

        prompt_infer_course = f"""
        Dựa vào câu hỏi của người dùng: '{question}'
        Và danh sách lịch thi sau: {schedule_text}
        Hãy suy luận xem sinh viên đang muốn ôn tập môn học nào? Trả về JSON chứa: {{"courseCode": "mã môn", "courseName": "tên môn"}}. 
        Nếu không rõ, trả về môn thi gần nhất.
        """
        # Gọi hàm generate_json (giả sử có sẵn trong NLPService) để lấy kết quả
        inferred_course_data = self.nlp_service.generate_json(prompt_infer_course)

        course_code = inferred_course_data.get("courseCode", "")
        course_name = inferred_course_data.get("courseName", "")

        if not course_code:
            return {"answer": "Mình không tìm thấy thông tin môn thi nào phù hợp để ôn tập.", "citations": []}

        # BƯỚC 1B: RAG tìm tài liệu môn học đó trong Knowledge Base
        # Sử dụng hàm tìm kiếm Vector có sẵn của KBService
        relevant_chunks = self.kb_service.retrieve_relevant_chunks(query=question, course_code=course_code)

        # Xử lý: Nếu KHÔNG CÓ TÀI LIỆU
        if not relevant_chunks:
            fallback_answer = (
                f"Hệ thống RAG hiện tại chưa có tài liệu nội bộ cho môn **{course_name} ({course_code})**.\n"
                f"Mình recommend bạn truy cập hệ thống Tailieuhust để tìm tài liệu phù hợp:\n"
                f"👉 [Tài liệu môn {course_code} trên Tailieuhust.com](https://tailieuhust.com/?s={course_code})"
            )
            return {
                "answer": fallback_answer,
                "citations": [{"type": "external_link", "source": "tailieuhust.com",
                               "ref": f"https://tailieuhust.com/?s={course_code}"}]
            }

        # BƯỚC 2: CÓ TÀI LIỆU -> RAG đọc tài liệu và sinh Flashcard / Trả lời
        context_text = "\n".join([chunk.get("content", "") for chunk in relevant_chunks])

        if "flashcard" in question.lower():
            # Yêu cầu LLM sinh Flashcard từ context vừa retrieve được
            prompt_study = f"""
            Dựa trên TÀI LIỆU RAG SAU của môn {course_name}:
            {context_text}

            Hãy đóng vai một gia sư, tạo một bộ Flashcard (Hỏi - Đáp) trọng tâm nhất để sinh viên luyện thi.
            """
        else:
            # Yêu cầu LLM recommend/giải thích lý thuyết thông thường
            prompt_study = f"""
            Dựa trên TÀI LIỆU RAG SAU của môn {course_name}:
            {context_text}

            Hãy trả lời câu hỏi của sinh viên: '{question}'. Khuyên họ nên tập trung ôn phần nào dựa trên tài liệu này.
            """

        # Gọi LLM (sẵn có) để sinh text cuối cùng
        final_answer = self.nlp_service.generate_text(prompt_study)

        # Gắn citation trỏ về nguồn tài liệu nội bộ đã RAG
        citations = [{"type": "internal_rag", "source": chunk.get("source", "Tài liệu nội bộ")} for chunk in
                     relevant_chunks]

        return {
            "answer": final_answer,
            "citations": citations
        }

