from services.nlp_service import NLPService
from services.study_service import StudyService
from services.user_service import UserService
from services.exam_service import ExamService
from services.exam_schedule_service import ExamScheduleService
from services.help_request_service import HelpRequestService
from services.regulation_service import RegulationService
from services.kb_service import KBService
import json

class ChatOrchestrationService:
    """SIMPLIFIED - Routes user queries to appropriate service"""

    def __init__(self):
        self.nlp_service = NLPService()
        self.study_service = StudyService()
        self.user_service = UserService()
        self.exam_service = ExamService()
        self.exam_schedule_service = ExamScheduleService()
        self.regulation_service = RegulationService()
        self.help_request_service = HelpRequestService()
        self.kb_service = KBService()

    def ask(self, payload: dict, authorization: str = None) -> dict:
        """Handle user question and route to appropriate service"""

        question = payload.get("question", "")
        user_id = payload.get("userId", "default_user")

        # Parse intent
        intent_result = self.nlp_service.parse_intent(question)
        intent = intent_result.get("intent")

        # Route to appropriate service
        if intent == "help_request":
            # Route to help request service
            result = self.help_request_service.create_help_session(user_id, question)
            return {
                "intent": "help_request",
                "sessionId": result.get("sessionId"),
                "channel": result.get("channel"),
                "botResponse": result.get("botResponse"),
                "timestamp": result.get("timestamp")
            }

        elif intent == "exam_schedule":
            answer = self.exam_service.answer_exam_question(user_id, question)
            return {
                "intent": "exam_schedule",
                "answer": {"text": answer},
                "citations": [],
            }

        elif intent == "regulation":
            answer = self.regulation_service.answer_regulation_question(question)
            return {
                "intent": "regulation",
                "answer": {"text": answer},
                "citations": [],
            }
        
        elif intent == "study_support":
            # Get user context
            try:
                user_info = self.user_service.get_user(user_id)
                upcoming_exams = self.exam_schedule_service.get_upcoming_exams(user_id)
            except:
                user_info = {}
                upcoming_exams = []

            # Process with study service
            result = self.study_service.process_study_workflow(question, user_info, upcoming_exams)

            return {
                "intent": "study_support",
                "answer": result.get("answer"),
                "citations": result.get("citations"),
                "metadata": result.get("metadata")
            }
        
        else:
            return {
                "intent": intent,
                "answer": {"text": "Câu hỏi này không được hỗ trợ. Vui lòng hỏi về ôn tập hoặc yêu cầu trợ giúp."},
                "citations": []
            }
        
    def process_chat(self, role: str, prompt: str, context: dict) -> dict:
        """
        Nhận input từ Streamlit, suy luận ngữ cảnh (Context) và trả về kết quả
        """
        result = {
            "answer": "",
            "context": context  # Trả về context để UI cập nhật
        }

        try:
            if role == "student":
                # 1. TRÍCH XUẤT THỰC THỂ & INTENT BẰNG AI
                sys_router = f"""
                Bạn là AI Router. Phân tích câu hỏi của sinh viên và trả về DUY NHẤT một chuỗi JSON:
                {{
                    "intent": "QUY_CHE" | "LICH_THI" | "ON_TAP" | "GIAO_TIEP",
                    "student_id": "Mã sinh viên nếu có (vd: u004), hoặc null",
                    "course_code": "Mã môn học nếu có (vd: PRM392), hoặc null"
                }}
                Ngữ cảnh hiện tại: {context}
                Câu hỏi: "{prompt}"
                """
                
                # SỬ DỤNG ĐÚNG BIẾN self.study_service của bạn
                router_response = self.study_service.model.generate_content(sys_router).text.strip()
                router_response = router_response.replace("```json", "").replace("```", "").strip()
                
                try:
                    router_data = json.loads(router_response)
                except json.JSONDecodeError:
                    router_data = {"intent": "GIAO_TIEP"}

                intent = router_data.get("intent", "GIAO_TIEP")
                
                # Cập nhật bộ nhớ ngữ cảnh (Context)
                if router_data.get("student_id"): result["context"]["student_id"] = router_data["student_id"]
                if router_data.get("course_code"): result["context"]["course_code"] = router_data["course_code"].upper()

                c_student_id = result["context"].get("student_id")
                c_course_code = result["context"].get("course_code")

                # 2. ĐIỀU HƯỚNG TÁC VỤ VÀO CÁC SERVICES GỐC CỦA BẠN
                if intent == "LICH_THI":
                    if not c_student_id:
                        result["answer"] = "Để tra cứu lịch thi, bạn vui lòng cho mình biết **Mã số sinh viên** nhé (Ví dụ: u004)!"
                    else:
                        result["answer"] = self.exam_service.answer_exam_question(c_student_id, prompt)

                elif intent == "QUY_CHE":
                    result["answer"] = self.regulation_service.answer_regulation_question(prompt)

                elif intent == "ON_TAP":
                    if not c_course_code:
                        result["answer"] = "Bạn muốn ôn tập môn nào nhỉ? (Gõ mã môn, ví dụ: PRM392)"
                    else:
                        # Tìm trong VectorDB
                        chunks = self.kb_service.retrieve_relevant_chunks(prompt, c_course_code)
                        if chunks and len(chunks) > 0:
                            context_str = "\n\n".join([c.get("content", "") for c in chunks])
                            sys_study = f"Tài liệu môn {c_course_code}:\n{context_str}\n\nHãy trả lời câu hỏi: {prompt}"
                            result["answer"] = self.study_service.model.generate_content(sys_study).text.strip()
                        else:
                            recs = self.study_service.get_recommendations(c_course_code)
                            ans = f"⚠️ Hệ thống chưa có dữ liệu bài giảng phần này cho môn **{c_course_code}**.\n\n"
                            if recs:
                                ans += "Bạn tham khảo link tài liệu sau:\n" + "\n".join([f"- [{m['title']}]({m['url']})" for m in recs])
                            ans += "\n\n💡 Hoặc bạn có thể **mở mục 📎 Đính kèm phía trên** để tải file PDF/DOCX của môn học này lên nhé!"
                            result["answer"] = ans

                else:
                    result["answer"] = self.study_service.model.generate_content(f"Trả lời thân thiện: {prompt}").text.strip()

            elif role == "admin":
                if "thêm" in prompt.lower() and "lịch" in prompt.lower():
                    result["answer"] = "Đang kết nối Firebase Service để thêm lịch thi..."
                else:
                    result["answer"] = "Đã nhận lệnh Quản trị viên."

        except Exception as e:
            result["answer"] = f"❌ Lỗi xử lý AI (Backend): {str(e)}"

        return result