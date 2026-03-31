import streamlit as st
import time
import pandas as pd
import base64
from services.regulation_service import RegulationService
from services.exam_service import ExamService
from services.safety_service import SafetyService
from services.kb_service import KBService
from services.chat_orchestration_service import ChatOrchestrationService
from services.exam_schedule_service import ExamScheduleService
from services.study_service import StudyService
import os
import warnings

# Tắt các cảnh báo lặt vặt của transformers
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", module="transformers")


# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO STATE
# ==========================================
st.set_page_config(page_title="GC-Proctor Portal", page_icon="🛡️", layout="wide")

# ==========================================
# KHỞI TẠO SERVICES (CHỈ LOAD 1 LẦN)
# ==========================================
@st.cache_resource
def get_services():
    """Khởi tạo services dùng chung (singleton) - Gom tất cả vào đây để tối ưu tốc độ"""
    return {
        "regulation_service": RegulationService(),
        "exam_service": ExamService(),
        "safety_service": SafetyService(),
        "kb_service": KBService(),
        "chat_service": ChatOrchestrationService(),
        "exam_schedule_svc": ExamScheduleService(),
        "study_svc": StudyService()
    }

services = get_services()
reg_service = services["regulation_service"]
exam_service = services["exam_service"]
kb_service = services["kb_service"]
chat_service = services["chat_service"]
exam_schedule_svc = services["exam_schedule_svc"]
study_svc = services["study_svc"]

# Khởi tạo các biến trạng thái (Session State) để lưu lịch sử và điều hướng
if "page" not in st.session_state:
    st.session_state.page = "home" 
if "role" not in st.session_state:
    st.session_state.role = None 

# Khởi tạo lịch sử chat riêng cho 3 luồng
if "chat_quyche" not in st.session_state:
    st.session_state.chat_quyche = [{"role": "assistant", "content": "Chào bạn, tôi là chuyên gia về Quy chế Khảo thí. Bạn cần hỏi gì?"}]
if "chat_lichthi" not in st.session_state:
    st.session_state.chat_lichthi = [{"role": "assistant", "content": "Dưới đây là lịch thi của bạn. Bạn có thắc mắc gì về phòng máy, giờ thi hay môn thi không?"}]
if "chat_ontap" not in st.session_state:
    st.session_state.chat_ontap = [{"role": "assistant", "content": "Sẵn sàng ôn tập! Gửi cho tôi slide bài giảng hoặc chủ đề bạn muốn luyện tập."}]

# Khởi tạo student_id cho session (dùng cho tra cứu lịch thi)
if "student_id" not in st.session_state:
    st.session_state.student_id = None

# Hàm điều hướng trang
def navigate_to(page_name, role=None):
    st.session_state.page = page_name
    if role:
        st.session_state.role = role

# ==========================================
# 2. THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("🛡️ GC-Proctor")
    st.markdown("---")
    
    if st.button("🏠 Đổi vai trò (Trang chủ)", width="stretch"):
        navigate_to("home", None)
    
    st.markdown("---")
    
    # Menu cho Sinh viên
    if st.session_state.role == "student":
        st.caption("👨‍🎓 MENU SINH VIÊN")
        if st.button("📍 Dashboard Sinh viên", width="stretch"): navigate_to("student_home")
        if st.button("💬 Hỏi đáp Quy chế", width="stretch"): navigate_to("chat_quyche")
        if st.button("📅 Lịch thi của tôi", width="stretch"): navigate_to("chat_lichthi")
        if st.button("📚 Ôn tập kiến thức", width="stretch"): navigate_to("chat_ontap")
        
    # Menu cho Admin
    elif st.session_state.role == "admin":
        st.caption("👨‍💻 MENU ADMIN")
        if st.button("⚙️ Quản lý Hệ thống", width="stretch"): navigate_to("admin_home")


# ----------------------------------------
# TRANG CHAT (GIỮ NGUYÊN HÀM GỐC CỦA BẠN - CHỈ THÊM st.container)
# ----------------------------------------
def render_chat_ui(chat_history_key, title, subtitle, is_rag=False, is_exam_lookup=False, is_study_rag=False, course_code="ALL"):
    st.header(title)
    st.caption(subtitle)
    
    # Bọc tin nhắn vào container để fix lỗi UI trôi ô nhập
    chat_container = st.container() 
    
    with chat_container:
        for message in st.session_state[chat_history_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "links" in message:
                    for link in message["links"]:
                        st.caption(f"🔗 [Nguồn: {link['title']}]({link['url']})")

    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        st.session_state[chat_history_key].append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                if is_rag:
                    # GỌI BACKEND THẬT CHO QUY CHẾ
                    with st.spinner("Đang tra cứu quy chế..."):
                        ai_response = reg_service.answer_regulation_question(prompt)
                    
                    full_response = ""
                    for chunk in ai_response.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    
                    relevant_links = []
                    regs = reg_service.get_all_regulations()
                    if regs:
                        relevant_links = [{"title": regs[0].get_title(), "url": regs[0].get_sourceUrl()}]
                    
                    st.session_state[chat_history_key].append({"role": "assistant", "content": full_response, "links": relevant_links})
                    for link in relevant_links:
                        st.caption(f"🔗 [Nguồn: {link['title']}]({link['url']})")

                elif is_exam_lookup:
                    # GỌI BACKEND THẬT CHO LỊCH THI
                    student_id = st.session_state.get("student_id")
                    if not student_id:
                        st.error("⚠️ Vui lòng nhập Mã số sinh viên ở phía trên trước khi hỏi về lịch thi.")
                        st.stop()
                    
                    with st.spinner("Đang tra cứu lịch thi..."):
                        ai_response = exam_schedule_svc.answer_exam_question(student_id, prompt)

                    full_response = ""
                    for chunk in ai_response.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                    st.session_state[chat_history_key].append({"role": "assistant", "content": full_response})
                
                elif is_study_rag:
                    # GỌI BACKEND THẬT CHO CHAT ÔN TẬP
                    with st.spinner("Đang lục tìm trong tài liệu bài giảng..."):
                        chunks = kb_service.retrieve_relevant_chunks(prompt, course_code)
                        if not chunks:
                            ai_response = f"⚠️ Không tìm thấy nội dung liên quan trong tài liệu môn **{course_code}**."
                        else:
                            context = "\n\n".join([c.get("content", "") for c in chunks])
                            sys_prompt = f"Dựa trên tài liệu bài giảng sau, hãy trả lời câu hỏi của sinh viên:\n\nTÀI LIỆU:\n{context}\n\nCÂU HỎI: {prompt}"
                            try:
                                response = study_svc.model.generate_content(sys_prompt)
                                ai_response = response.text
                            except Exception as e:
                                ai_response = f"Lỗi khi gọi AI: {e}"
                                
                    full_response = ""
                    for chunk in ai_response.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state[chat_history_key].append({"role": "assistant", "content": full_response})

# ==========================================
# 3. RENDER CÁC TRANG DỰA TRÊN ĐIỀU HƯỚNG
# ==========================================

if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Chào mừng đến với hệ thống GC-Proctor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vui lòng chọn cổng đăng nhập của bạn</p><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        st.info("### 👨‍🎓 Dành cho Sinh viên\nTra cứu quy chế, xem lịch thi cá nhân và ôn tập cùng AI.")
        if st.button("Truy cập Cổng Sinh viên", width="stretch", type="primary"):
            navigate_to("student_home", "student")
            st.rerun()
            
    with col3:
        st.error("### 👨‍💻 Dành cho Admin\nQuản lý dữ liệu lịch thi, cấu hình quy chế và upload tài liệu RAG.")
        if st.button("Truy cập Cổng Quản trị", width="stretch", type="primary"):
            navigate_to("admin_home", "admin")
            st.rerun()

elif st.session_state.page == "student_home":
    st.header("👋 Xin chào Sinh viên!")
    st.markdown("Hôm nay bạn muốn tôi hỗ trợ tính năng gì?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("#### 💬 Hỏi đáp Quy chế")
        if st.button("Vào Chat Quy chế", width="stretch"):
            navigate_to("chat_quyche")
            st.rerun()

    with col2:
        st.warning("#### 📅 Lịch thi & Trợ lý")
        if st.button("Xem & Hỏi đáp Lịch thi", width="stretch"):
            navigate_to("chat_lichthi")
            st.rerun()

    with col3:
        st.success("#### 📚 Ôn tập kiến thức")
        if st.button("Vào Ôn tập", width="stretch"):
            navigate_to("chat_ontap")
            st.rerun()

elif st.session_state.page == "chat_quyche":
    render_chat_ui("chat_quyche", "💬 Trợ lý Quy chế", "Hỏi đáp mọi thứ về Sổ tay sinh viên và Quy chế thi.", is_rag=True)

elif st.session_state.page == "chat_lichthi":
    st.header("📅 Lịch thi & Trợ lý Khảo thí")
    
    st.info("ℹ️ Vui lòng nhập Mã số sinh viên của bạn để tra cứu lịch thi cá nhân:")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_student_id = st.text_input(
            "Mã số sinh viên (VD: u004)",
            value=st.session_state.get("student_id", ""),
            key="student_id_input"
        )
        if new_student_id and new_student_id != st.session_state.get("student_id"):
            st.session_state.student_id = new_student_id
    
    with col2:
        if st.button("🔄 Cập nhật", width="stretch"):
            st.rerun()
    
    st.divider()
    
    st.markdown("##### Bảng lịch thi sắp tới:")
    df_exams = pd.DataFrame([
        {"Môn thi": "PRM392", "Ngày thi": "15/05/2026", "Giờ thi": "07:30 AM", "Phòng": "P.202 Alpha", "Hình thức": "Thực hành (PE)"},
        {"Môn thi": "SWE201", "Ngày thi": "18/05/2026", "Giờ thi": "09:45 AM", "Phòng": "P.101 Beta", "Hình thức": "Lý thuyết (FE)"},
    ])
    st.dataframe(df_exams, hide_index=True) 
    st.divider()
    
    render_chat_ui("chat_lichthi", "🤖 Hỏi đáp lịch thi", "Bạn có thắc mắc gì về danh sách môn thi ở trên không?", is_exam_lookup=True)

elif st.session_state.page == "chat_ontap":
    st.header("📚 Cổng Ôn tập Thông minh")

    t1, t2, t3 = st.tabs(["💬 Chat với Tài liệu", "🗂️ Flashcards AI", "📖 Tài liệu đề xuất"])

    with t1:
        st.markdown("Hỏi đáp với kho tài liệu dùng chung, hoặc **tự tải lên bài giảng của bạn** để AI hỗ trợ ôn tập.")
        
        # Phần Upload tài liệu an toàn (Chỉ dùng kb_service gốc)
        with st.expander("📁 Thêm tài liệu ôn tập cá nhân (PDF, DOCX)"):
            st.info("Tài liệu tải lên ở đây sẽ được AI phân tích để tạo Flashcard và hỗ trợ trả lời câu hỏi.")
            col_file, col_course = st.columns([2, 1])
            with col_file:
                uploaded_study_doc = st.file_uploader("Chọn slide/bài giảng", type=["pdf", "docx"], key="student_upload")
            with col_course:
                study_course_code = st.text_input("Mã môn học", placeholder="VD: PRM392", key="student_course")
            
            if st.button("🚀 Bắt đầu học tài liệu này"):
                if uploaded_study_doc and study_course_code:
                    with st.spinner("Đang lưu tài liệu vào hệ thống..."):
                        try:
                            file_bytes = uploaded_study_doc.getvalue()
                            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
                            data = kb_service.upload_document(
                                file_path=encoded_file,
                                course_code=study_course_code.upper(),
                                title=uploaded_study_doc.name
                            )
                            # Thông báo chat thành công
                            st.session_state.chat_ontap.append({"role": "assistant", "content": f"✅ Đã tải và học xong tài liệu **{uploaded_study_doc.name}** (Môn {study_course_code.upper()}). Hãy đặt câu hỏi hoặc sang tab Flashcard để ôn tập nhé!"})
                            st.success("Tải tài liệu thành công!")
                        except Exception as e:
                            st.error(f"⚠️ Có lỗi xảy ra: {e}")
                else:
                    st.warning("Vui lòng tải file và nhập mã môn học.")
        
        st.divider()
        
        
        render_chat_ui("chat_ontap", "Hỏi đáp kiến thức", "Hỏi về slide, bài giảng...", is_study_rag=True, course_code=study_course_code if 'study_course_code' in locals() else "ALL")

    with t2:
        st.subheader("Tạo bộ thẻ ghi nhớ")
        fc_course = st.text_input("Mã môn học (VD: PRM392, hoặc ALL)", value="ALL", key="fc_course_input")
        topic = st.text_input("Chủ đề ôn tập", key="fc_topic")
        
        if st.button("🚀 Tạo ngay"):
            with st.spinner("Đang tạo thẻ..."):
                res = study_svc.generate_flashcards(fc_course, topic) 
                # Đã fix lỗi KeyError "status"
                if "flashcards" in res and len(res["flashcards"]) > 0:
                    for card in res["flashcards"]:
                        with st.expander(card.get("question", "Câu hỏi")):
                            st.write(card.get("answer", "Trả lời"))
                else:
                    st.error(res.get("message", "Không thể tạo bộ thẻ hoặc môn học chưa có dữ liệu."))

    with t3:
        st.subheader("Tài liệu khuyên dùng")
        mats = study_svc.get_recommendations("PRM392") 
        if mats:
            for m in mats:
                st.markdown(f"- **[{m['title']}]({m['url']})**")
        else:
            st.info("Chưa có tài liệu đề xuất cho môn này trên Firebase.")
            
elif st.session_state.page == "admin_home":
    st.header("⚙️ Quản trị Hệ thống GC-Proctor")

    tab1, tab2 = st.tabs(["📚 Upload Quy chế", "📅 Quản lý Lịch thi"])

    with tab1:
        st.subheader("Upload Tài liệu Quy chế")

        uploaded_doc = st.file_uploader("Chọn file PDF hoặc DOCX", type=["pdf", "docx"])
        doc_title = st.text_input("Tên tài liệu", placeholder="VD: Quy chế thi cử 2024")
        course_code = st.text_input("Mã môn học (Course Code)", placeholder="VD: ALL hoặc PRM392")

        if st.button("🚀 Upload lên Vector DB", type="primary"):
            if uploaded_doc and doc_title and course_code:
                with st.spinner("Đang xử lý qua KBService..."):
                    try:
                        file_bytes = uploaded_doc.getvalue()
                        encoded_file = base64.b64encode(file_bytes).decode('utf-8')

                        data = kb_service.upload_document(
                            file_path=encoded_file,
                            course_code=course_code,
                            title=doc_title
                        )

                        st.success(f"✅ Đã gửi yêu cầu xử lý tài liệu: {doc_title}")
                        st.json(data)

                    except Exception as e:
                        st.error(f"⚠️ Lỗi xử lý Service: {e}")
            else:
                st.warning("Vui lòng điền đầy đủ: File, Tên tài liệu và Mã môn học.")