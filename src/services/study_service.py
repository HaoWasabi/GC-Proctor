import json
from services.kb_service import KBService
from services.nlp_service import NLPService


class StudyService:
    """CLEAN Study Service - handles RAG + LLM for study support"""

    def __init__(self):
        self.kb_service = KBService()
        self.nlp_service = NLPService()

    def process_study_workflow(self, question: str, user_info: dict, upcoming_exams: list) -> dict:
        """
        Main workflow:
        1. Infer course from question + schedule
        2. Retrieve relevant materials (RAG)
        3. Generate answer using LLM with context
        """

        # STEP 1: Infer which course to study
        schedule_text = json.dumps(upcoming_exams, ensure_ascii=False, indent=2)

        inference_prompt = f"""
        Câu hỏi: {question}
        Lịch thi sắp tới:
        {schedule_text}

        Suy luận môn học phù hợp. Trả về JSON: {{"courseCode": "ĐS101", "courseName": "Đại số tuyến tính"}}
        """

        course_data = self.nlp_service.generate_json(inference_prompt)
        course_code = course_data.get("courseCode", "")
        course_name = course_data.get("courseName", "")

        if not course_code:
            return {
                "answer": "Không thể xác định môn học bạn muốn ôn tập. Vui lòng nêu rõ tên môn.",
                "citations": []
            }

        # STEP 2: Retrieve materials from KB
        relevant_chunks = self.kb_service.retrieve_relevant_chunks(question, course_code)

        if not relevant_chunks:
            return {
                "answer": f"Hệ thống chưa có tài liệu cho môn {course_name}. Hãy upload tài liệu trước.",
                "citations": []
            }

        # STEP 3: Generate answer with LLM + context
        context_text = "\n".join([chunk.get("content", "") for chunk in relevant_chunks])

        if "flashcard" in question.lower():
            answer_prompt = f"""
            Dựa trên tài liệu dưới đây của môn {course_name}, tạo 5-10 flashcard (Câu hỏi - Đáp án) 
            để giúp sinh viên ôn tập hiệu quả:

            TÀI LIỆU:
            {context_text}
            """
        else:
            answer_prompt = f"""
            Trả lời câu hỏi: "{question}"

            Dựa trên tài liệu của môn {course_name}:
            {context_text}

            Trả lời đầy đủ, chi tiết và đưa ra những điểm trọng tâm cần ôn tập.
            """

        final_answer = self.nlp_service.generate_text(answer_prompt)

        # Create citations
        citations = [
            {
                "type": "internal_rag",
                "source": chunk.get("source", "Tài liệu nội bộ"),
                "course": course_code
            }
            for chunk in relevant_chunks
        ]

        return {
            "answer": final_answer,
            "citations": citations,
            "metadata": {
                "course_code": course_code,
                "course_name": course_name
            }
        }

    def generate_flashcards(self, course_code: str, topic: str, num_cards: int = 10) -> dict:
        """Standalone flashcard generator"""
        chunks = self.kb_service.retrieve_relevant_chunks(topic, course_code)

        if not chunks:
            return {"flashcards": [], "error": "No materials found"}

        context = "\n".join([c.get("content", "") for c in chunks])

        prompt = f"""
        Tạo {num_cards} flashcard về chủ đề: {topic}

        Dựa trên tài liệu:
        {context}

        Format: JSON array với các object có cấu trúc {{"question": "...", "answer": "..."}}
        """

        flashcards_data = self.nlp_service.generate_json(prompt)
        return {
            "flashcards": flashcards_data if isinstance(flashcards_data, list) else flashcards_data.get("flashcards",
                                                                                                        [])}

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
        Tóm tắt tài liệu của môn {course_code} trong {length_guide.get(length, length_guide['short'])}:

        {context}
        """

        summary = self.nlp_service.generate_text(prompt)
        return {"summary": summary, "length": length}

