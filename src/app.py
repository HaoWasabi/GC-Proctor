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
import os
import warnings
# Tắt các cảnh báo lặt vặt của transformers
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Bỏ qua các FutureWarning do Streamlit quét trúng
warnings.filterwarnings("ignore", module="transformers")


kb_service = KBService()
chat_service = ChatOrchestrationService()
exam_service = ExamScheduleService()
# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO STATE
# ==========================================
st.set_page_config(page_title="GC-Proctor Portal", page_icon="🛡️", layout="wide")

# ==========================================
# KHỞI TẠO SERVICES
# ==========================================
@st.cache_resource
def get_services():
    """Khởi tạo services dùng chung (singleton)"""
    return {
        "regulation_service": RegulationService(),
        "exam_service": ExamService(),
        "safety_service": SafetyService()
    }

services = get_services()
reg_service = services["regulation_service"]
exam_service = services["exam_service"]

# Khởi tạo các biến trạng thái (Session State) để lưu lịch sử và điều hướng
if "page" not in st.session_state:
    st.session_state.page = "home" # Các trang: home, student_home, chat_quyche, chat_lichthi, chat_ontap, admin_home
if "role" not in st.session_state:
    st.session_state.role = None # "student" hoặc "admin"

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
    
    # Nút về Trang chủ luôn hiện
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
        if st.button("⚙️ Quản lý Hệ thống", use_container_width=True): navigate_to("admin_home")


# ----------------------------------------
# TRANG CHAT (HÀM DÙNG CHUNG ĐỂ RENDER UI CHAT)
# ----------------------------------------
def render_chat_ui(chat_history_key, title, subtitle, is_rag=False, is_exam_lookup=False):
    st.header(title)
    st.caption(subtitle)
    
    # Hiển thị lịch sử tin nhắn
    for message in st.session_state[chat_history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Hiển thị trích dẫn nếu có
            if "links" in message:
                for link in message["links"]:
                    st.caption(f"🔗 [Nguồn: {link['title']}]({link['url']})")

    # Ô nhập liệu chat
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Thêm tin nhắn user vào lịch sử
        st.session_state[chat_history_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Xử lý phản hồi
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            if is_rag:
                # GỌI BACKEND THẬT CHO QUY CHẾ
                with st.spinner("Đang tra cứu quy chế..."):
                    ai_response = reg_service.answer_regulation_question(prompt)
                
                # Hiệu ứng gõ chữ
                full_response = ""
                for chunk in ai_response.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # Lấy link tài liệu từ Repository (lấy tài liệu đầu tiên làm ví dụ trích dẫn)
                relevant_links = []
                regs = reg_service.get_all_regulations()
                if regs:
                    relevant_links = [{"title": regs[0].get_title(), "url": regs[0].get_sourceUrl()}]
                
                # Lưu vào history
                st.session_state[chat_history_key].append({
                    "role": "assistant", 
                    "content": full_response,
                    "links": relevant_links
                })
                
                # Hiển thị link trích dẫn
                for link in relevant_links:
                    st.caption(f"🔗 [Nguồn: {link['title']}]({link['url']})")

            elif is_exam_lookup:
                # GỌI BACKEND THẬT CHO LỊCH THI
                student_id = st.session_state.get("student_id")
                if not student_id:
                    st.error("⚠️ Vui lòng nhập Mã số sinh viên ở phía trên trước khi hỏi về lịch thi.")
                    return
                
                with st.spinner("Đang tra cứu lịch thi..."):
                    ai_response = exam_service.answer_exam_question(student_id, prompt)

                # Hiệu ứng gõ chữ
                full_response = ""
                for chunk in ai_response.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                st.session_state[chat_history_key].append({
                    "role": "assistant",
                    "content": full_response
                })
            
            else:
                # Giả lập cho các luồng khác chưa tích hợp RAG
                full_response = ""
                simulated_response = f"Đây là câu trả lời giả lập cho luồng '{title}'. Bạn vừa hỏi: '{prompt}'. Sau này thay bằng API gọi xuống Backend nhé!"
                for chunk in simulated_response.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state[chat_history_key].append({"role": "assistant", "content": full_response})


# ==========================================
# 3. RENDER CÁC TRANG DỰA TRÊN ĐIỀU HƯỚNG
# ==========================================

# ----------------------------------------
# TRANG CHỦ: CHỌN VAI TRÒ
# ----------------------------------------
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Chào mừng đến với hệ thống GC-Proctor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vui lòng chọn cổng đăng nhập của bạn</p><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        st.info("### 👨‍🎓 Dành cho Sinh viên\nTra cứu quy chế, xem lịch thi cá nhân và ôn tập cùng AI.")
        if st.button("Truy cập Cổng Sinh viên", use_container_width=True, type="primary"):
            navigate_to("student_home", "student")
            st.rerun()
            
    with col3:
        st.error("### 👨‍💻 Dành cho Admin\nQuản lý dữ liệu lịch thi, cấu hình quy chế và upload tài liệu RAG.")
        if st.button("Truy cập Cổng Quản trị", use_container_width=True, type="primary"):
            navigate_to("admin_home", "admin")
            st.rerun()

# ----------------------------------------
# TRANG SINH VIÊN: DASHBOARD
# ----------------------------------------
elif st.session_state.page == "student_home":
    st.header("👋 Xin chào Sinh viên!")
    st.markdown("Hôm nay bạn muốn tôi hỗ trợ tính năng gì?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("#### 💬 Hỏi đáp Quy chế\nChat với AI về nội quy, điểm số, vắng thi.")
        if st.button("Vào Chat Quy chế", use_container_width=True):
            navigate_to("chat_quyche")
            st.rerun()

    with col2:
        st.warning("#### 📅 Lịch thi & Trợ lý\nXem bảng lịch thi và hỏi đáp các thắc mắc liên quan.")
        if st.button("Xem & Hỏi đáp Lịch thi", use_container_width=True):
            navigate_to("chat_lichthi")
            st.rerun()

    with col3:
        st.success("#### 📚 Ôn tập kiến thức\nLuyện tập với AI dựa trên tài liệu bài giảng của bạn.")
        if st.button("Vào Ôn tập", use_container_width=True):
            navigate_to("chat_ontap")
            st.rerun()

# ----------------------------------------
# 3 LUỒNG CHAT CỦA SINH VIÊN
# ----------------------------------------
elif st.session_state.page == "chat_quyche":
    render_chat_ui("chat_quyche", "💬 Trợ lý Quy chế", "Hỏi đáp mọi thứ về Sổ tay sinh viên và Quy chế thi.", is_rag=True)

elif st.session_state.page == "chat_lichthi":
    st.header("📅 Lịch thi & Trợ lý Khảo thí")
    
    # Input student_id
    st.info("ℹ️ Vui lòng nhập Mã số sinh viên của bạn để tra cứu lịch thi cá nhân:")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_student_id = st.text_input(
            "Mã số sinh viên (VD: SE160001, SV001)",
            value=st.session_state.get("student_id", ""),
            placeholder="Nhập mã SV của bạn",
            key="student_id_input"
        )
        if new_student_id and new_student_id != st.session_state.get("student_id"):
            st.session_state.student_id = new_student_id
    
    with col2:
        if st.button("🔄 Cập nhật", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Tạm hiển thị bảng dữ liệu mẫu
    st.markdown("##### Bảng lịch thi sắp tới:")
    df_exams = pd.DataFrame([
        {"Môn thi": "PRM392", "Ngày thi": "15/05/2026", "Giờ thi": "07:30 AM", "Phòng": "P.202 Alpha", "Hình thức": "Thực hành (PE)"},
        {"Môn thi": "SWE201", "Ngày thi": "18/05/2026", "Giờ thi": "09:45 AM", "Phòng": "P.101 Beta", "Hình thức": "Lý thuyết (FE)"},
    ])
    st.dataframe(df_exams, use_container_width=True, hide_index=True)
    st.divider()
    
    render_chat_ui(
        "chat_lichthi",
        "🤖 Hỏi đáp lịch thi",
        "Bạn có thắc mắc gì về danh sách môn thi ở trên không?",
        is_exam_lookup=True,
    )

elif st.session_state.page == "chat_ontap":
    st.header("📚 Cổng Ôn tập Thông minh")
    
    # Khởi tạo Service
    from services.study_service import StudyService
    svc = StudyService()

    t1, t2, t3 = st.tabs(["💬 Chat với Tài liệu", "🗂️ Flashcards AI", "📖 Tài liệu đề xuất"])

    with t1:
        # Chat RAG sử dụng KBService
        render_chat_ui("chat_ontap", "Hỏi đáp kiến thức", "Hỏi về slide, bài giảng...")

    with t2:
        st.subheader("Tạo bộ thẻ ghi nhớ")
        topic = st.text_input("Chủ đề ôn tập", key="fc_topic")
        if st.button("🚀 Tạo ngay"):
            res = svc.generate_flashcards("ALL", topic) # Gọi Service thật
            if res["status"] == "success":
                for card in res["flashcards"]:
                    with st.expander(card["question"]):
                        st.write(card["answer"])
            else:
                st.error(res["message"])

    with t3:
        st.subheader("Tài liệu khuyên dùng")
        # Gọi Service lấy dữ liệu từ Firebase
        mats = svc.get_recommendations("PRM392") 
        if mats:
            for m in mats:
                st.markdown(f"- **[{m['title']}]({m['url']})**")
        else:
            st.info("Chưa có tài liệu đề xuất cho môn này trên Firebase.")
# ----------------------------------------
# TRANG ADMIN: QUẢN LÝ DỮ LIỆU
# ----------------------------------------
elif st.session_state.page == "admin_home":
    st.header("⚙️ Quản trị Hệ thống GC-Proctor")

    tab1, tab2 = st.tabs(["📚 Upload Quy chế (Knowledge Base)", "📅 Quản lý Lịch thi"])

    with tab1:
        st.subheader("Upload Tài liệu Quy chế")

        uploaded_doc = st.file_uploader("Chọn file PDF hoặc DOCX", type=["pdf", "docx"])
        doc_title = st.text_input("Tên tài liệu", placeholder="VD: Quy chế thi cử 2024")

        # BỔ SUNG: Thêm ô nhập Course Code vì KBService yêu cầu
        course_code = st.text_input("Mã môn học (Course Code)", placeholder="VD: ALL (nếu dùng chung) hoặc PRM392")

        if st.button("🚀 Upload lên Vector DB", type="primary"):
            if uploaded_doc and doc_title and course_code:
                with st.spinner("Đang xử lý qua KBService..."):
                    try:
                        # 1. Mã hóa file sang Base64
                        file_bytes = uploaded_doc.getvalue()
                        encoded_file = base64.b64encode(file_bytes).decode('utf-8')

                        # 2. GỌI TRỰC TIẾP SERVICE VỚI ĐỦ 3 THAM SỐ
                        data = kb_service.upload_document(
                            file_path=encoded_file,
                            course_code=course_code,
                            title=doc_title
                        )

                        st.success(f"✅ Đã gửi yêu cầu xử lý tài liệu: {doc_title}")
                        st.json(data)  # Hiển thị kết quả trả về từ service

                    except Exception as e:
                        st.error(f"⚠️ Lỗi xử lý Service: {e}")
            else:
                st.warning("Vui lòng điền đầy đủ: File, Tên tài liệu và Mã môn học.")