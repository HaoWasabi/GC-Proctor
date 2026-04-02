import streamlit as st
import uuid
import base64
from datetime import datetime
import os
import warnings
from services.chat_orchestration_service import ChatOrchestrationService
from services.kb_service import KBService

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", module="transformers")

st.set_page_config(page_title="GC-Proctor Portal", page_icon="🛡️", layout="wide")

@st.cache_resource
def get_services():
    return {
        "chat_service": ChatOrchestrationService(),
        "kb_service": KBService()
    }

services = get_services()
chat_service = services["chat_service"]
kb_service = services["kb_service"]

if "page" not in st.session_state: st.session_state.page = "home" 
if "role" not in st.session_state: st.session_state.role = None 
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {}
if "current_session_id" not in st.session_state: st.session_state.current_session_id = None

def navigate_to(page_name, role=None):
    st.session_state.page = page_name
    if role: st.session_state.role = role

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🛡️ GC-Proctor AI")
    if st.button("🏠 Về Trang chủ", use_container_width=True):
        st.session_state.current_session_id = None
        navigate_to("home", None)
        st.rerun()
    
    st.markdown("---")
    if st.session_state.role in ["student", "admin"]:
        if st.button("➕ Trò chuyện mới", type="primary", use_container_width=True):
            st.session_state.current_session_id = None
            st.rerun()

        st.markdown("<br><b>🕒 Lịch sử trò chuyện</b>", unsafe_allow_html=True)
        for sid, sdata in reversed(st.session_state.chat_sessions.items()):
            if sdata.get('role') == st.session_state.role:
                if st.button(f"💬 {sdata['title']}", key=f"btn_{sid}", use_container_width=True):
                    st.session_state.current_session_id = sid
                    st.rerun()

# ================= TRANG CHỦ =================
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>GC-Proctor AI Agent</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        st.info("### 👨‍🎓 Dành cho Sinh viên\nTra cứu quy chế, lịch thi, ôn tập.")
        if st.button("Truy cập AI Sinh viên", width="stretch", type="primary"):
            navigate_to("unified_workspace", "student")
            st.rerun()
    with col3:
        st.error("### 👨‍💻 Dành cho Admin\nQuản lý tài liệu, lịch thi.")
        if st.button("Truy cập AI Quản trị", width="stretch", type="primary"):
            navigate_to("unified_workspace", "admin")
            st.rerun()

# ================= WORKSPACE =================
elif st.session_state.page == "unified_workspace":
    role = st.session_state.role
    
    if st.session_state.current_session_id is None:
        new_sid = str(uuid.uuid4())[:8]
        # Đổi câu chào cho ấn tượng
        welcome_msg = "🛡️ Chào SGU-er! Giám thị AI GC-Proctor đã sẵn sàng. Bạn muốn kiểm tra lịch thi phòng nào, hay cần tra cứu điều luật quy chế để tránh rớt môn?" if role == "student" else "Hệ thống quản trị sẵn sàng."
        st.session_state.chat_sessions[new_sid] = {
            "title": f"Phiên {datetime.now().strftime('%H:%M')}",
            "role": role,
            "messages": [{"role": "assistant", "content": welcome_msg}],
            "context": {} 
        }
        st.session_state.current_session_id = new_sid
        st.rerun()

    session = st.session_state.chat_sessions[st.session_state.current_session_id]
    st.header(f"🤖 AI {'Sinh viên' if role == 'student' else 'Quản trị viên'}")

    with st.expander("📎 Đính kèm tài liệu vào AI (Cho tính năng Ôn tập)"):
        uploaded_file = st.file_uploader("Tải lên file (PDF/DOCX)")
        course_target = st.text_input("Nhập mã môn học (VD: PRM392):")
        if st.button("🚀 Xử lý tài liệu", use_container_width=True) and uploaded_file:
            with st.spinner("Đang đưa tài liệu vào VectorDB..."):
                c_code = course_target.strip().upper() if course_target else "ALL"
                kb_service.upload_document(base64.b64encode(uploaded_file.getvalue()).decode('utf-8'), c_code, uploaded_file.name)
                session["context"]["course_code"] = c_code
                st.success("✅ Đã nạp tài liệu thành công!")

    chat_container = st.container(height=500, border=True)
    with chat_container:
        for message in session["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Nhập yêu cầu của bạn..."):
        session["messages"].append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("AI đang xử lý (Function Calling)..."):
                    # TRUYỀN THÊM HISTORY ĐỂ BOT NHỚ NGỮ CẢNH
                    result = chat_service.process_chat(
                        role=role, 
                        prompt=prompt, 
                        context=session["context"],
                        history=session["messages"][:-1] # Loại bỏ câu user vừa nhập để tránh trùng lặp trong history
                    )
                    
                    ai_response = result["answer"]
                    session["context"] = result["context"]
                    
                st.markdown(ai_response)
                session["messages"].append({"role": "assistant", "content": ai_response})
                st.session_state.chat_sessions[st.session_state.current_session_id] = session