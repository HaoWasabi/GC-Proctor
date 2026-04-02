import google.generativeai as genai
from services.study_service import StudyService
from services.exam_service import ExamService
from services.regulation_service import RegulationService
from services.kb_service import KBService

class ChatOrchestrationService:
    """MODERN AGENT - Sử dụng Native Function Calling của Gemini"""

    def __init__(self):
        self.study_service = StudyService()
        self.exam_service = ExamService()
        self.regulation_service = RegulationService()
        self.kb_service = KBService()

        # Xây dựng Persona cốt lõi
        self.system_instruction = """
        Bạn là GC-Proctor 🛡️ - Trợ lý AI Giám thị và Học vụ tận tâm của Đại học Sài Gòn (SGU).
        Đặc điểm:
        - Xưng hô "mình" và "bạn" (hoặc "SGU-er"). Luôn dùng icon 🛡️, 📚.
        - Trả lời ngắn gọn, đi thẳng vào vấn đề. Không dài dòng.
        
        Nguyên tắc cốt lõi (BẮT BUỘC):
        - Bạn được trang bị các CÔNG CỤ (Tools). Hãy ưu tiên tự động gọi các Công Cụ này khi người dùng hỏi về: Tra lịch thi (cần MSSV), Tra quy chế, hoặc Ôn tập bài giảng.
        - Nếu người dùng hỏi những thứ nằm ngoài giáo dục (Code bài tập hộ, Giải Toán/Lý/Hóa, Tin đồn, Giải trí), HÃY TỪ CHỐI một cách dí dỏm: "🛡️ Chà, GC-Proctor chỉ rành về học vụ và lịch trình SGU thôi. Vấn đề này ngoài chuyên môn của mình rồi SGU-er ơi!"
        """

        self.agent_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.system_instruction,
            tools=[self.tra_cuu_lich_thi, self.tra_cuu_quy_che, self.on_tap_mon_hoc]
        )

    # ================= CÁC CÔNG CỤ (TOOLS) CHO AI =================
    
    def tra_cuu_lich_thi(self, student_id: str, query: str) -> str:
        """Công cụ này dùng để lấy dữ liệu lịch thi từ database. Gọi khi sinh viên hỏi lịch thi.
        Args:
            student_id: Mã số sinh viên (Ví dụ: u004, 3120410...).
            query: Câu hỏi gốc của sinh viên (VD: "tuần sau thi môn gì")
        """
        if not student_id or student_id.lower() == "null":
            return "Hãy yêu cầu sinh viên cung cấp Mã số sinh viên (MSSV) để tra cứu."
        return self.exam_service.answer_exam_question(student_id, query)

    def tra_cuu_quy_che(self, query: str) -> str:
        """Công cụ dùng để tìm kiếm thông tin về quy chế đào tạo, luật lệ, tín chỉ, điểm số, rớt môn.
        Args:
            query: Câu hỏi gốc của sinh viên.
        """
        return self.regulation_service.answer_regulation_question(query)

    def on_tap_mon_hoc(self, course_code: str, query: str) -> str:
        """Công cụ dùng để tìm tài liệu bài giảng và giải đáp ôn tập môn học (RAG môn học).
        Args:
            course_code: Mã môn học (Ví dụ: PRM392). Nếu không có, hãy trả về 'NO_COURSE'
            query: Câu hỏi học thuật của sinh viên.
        """
        if course_code == "NO_COURSE" or not course_code:
             return "Hãy hỏi sinh viên xem họ muốn ôn tập mã môn học nào (VD: PRM392)."
        
        chunks = self.kb_service.retrieve_relevant_chunks(query, course_code.upper())
        if chunks and len(chunks) > 0:
            context_str = "\n\n".join([c.get("content", "") for c in chunks])
            sys_study = f"Tài liệu môn {course_code}:\n{context_str}\n\nTrả lời dựa trên tài liệu: {query}"
            return self.study_service.model.generate_content(sys_study).text.strip()
        else:
            return f"Hệ thống chưa có tài liệu cho môn {course_code}. Hãy hướng dẫn sinh viên dùng nút đính kèm để upload tài liệu."

    # ================= LUỒNG XỬ LÝ CHÍNH =================

    def process_chat(self, role: str, prompt: str, context: dict, history: list) -> dict:
        """Xử lý yêu cầu và duy trì trạng thái ngữ cảnh"""
        result = {
            "answer": "",
            "context": context  
        }

        try:
            if role == "student":
                # 1. Chuyển đổi định dạng Lịch sử Chat của Streamlit sang Gemini
                gemini_history = []
                for msg in history:
                    msg_role = "model" if msg["role"] == "assistant" else "user"
                    gemini_history.append({"role": msg_role, "parts": [msg["content"]]})

                # Cập nhật thông tin ẩn vào câu hỏi để Agent lấy tham số tự động
                hidden_context = f"[Ngữ cảnh ẩn - MSSV hiện tại: {context.get('student_id', 'Chưa có')}, Mã Môn: {context.get('course_code', 'Chưa có')}].\n Câu hỏi: "
                enriched_prompt = hidden_context + prompt

                # 2. Khởi động Agent với khả năng TỰ ĐỘNG GỌI HÀM (enable_automatic_function_calling)
                chat = self.agent_model.start_chat(
                    history=gemini_history,
                    enable_automatic_function_calling=True # Đây là tính năng xịn nhất, AI tự quyết định gọi tools
                )
                
                # 3. Gửi prompt. AI sẽ tự suy luận -> gọi Tool Python tương ứng -> Lấy kết quả -> Sinh câu trả lời cuối cùng
                response = chat.send_message(enriched_prompt)
                result["answer"] = response.text

                # 4. Trích xuất lại MSSV hoặc Mã môn từ prompt mới nếu người dùng cung cấp
                # Dùng một LLM flash siêu nhanh để trích xuất trạng thái nhẹ nhàng (chạy ngầm)
                extraction_prompt = f"""Trích xuất MSSV (VD: u004, 3120...) và Mã môn học (VD: PRM392) từ câu sau nếu có. 
                Trả về dạng CSV: MSSV,CourseCode. Nếu không có xuất ra: NONE,NONE. 
                Câu hỏi: {prompt}"""
                try:
                    ext = self.study_service.model.generate_content(extraction_prompt).text.strip().split(',')
                    if len(ext) == 2:
                        if ext[0].strip() != "NONE": result["context"]["student_id"] = ext[0].strip()
                        if ext[1].strip() != "NONE": result["context"]["course_code"] = ext[1].strip().upper()
                except: pass

            elif role == "admin":
                result["answer"] = "Đã nhận lệnh Quản trị viên."

        except Exception as e:
            result["answer"] = f"❌ Lỗi xử lý Agent AI: {str(e)}"

        return result