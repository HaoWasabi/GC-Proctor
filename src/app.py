import streamlit as st
import time
import pandas as pd

# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO STATE
# ==========================================
st.set_page_config(page_title="GC-Proctor Portal", page_icon="🛡️", layout="wide")

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
    if st.button("🏠 Đổi vai trò (Trang chủ)", use_container_width=True):
        navigate_to("home", None)
    
    st.markdown("---")
    
    # Menu cho Sinh viên
    if st.session_state.role == "student":
        st.caption("👨‍🎓 MENU SINH VIÊN")
        if st.button("📍 Dashboard Sinh viên", use_container_width=True): navigate_to("student_home")
        if st.button("💬 Hỏi đáp Quy chế", use_container_width=True): navigate_to("chat_quyche")
        if st.button("📅 Lịch thi của tôi", use_container_width=True): navigate_to("chat_lichthi")
        if st.button("📚 Ôn tập kiến thức", use_container_width=True): navigate_to("chat_ontap")
        
    # Menu cho Admin
    elif st.session_state.role == "admin":
        st.caption("👨‍💻 MENU ADMIN")
        if st.button("⚙️ Quản lý Hệ thống", use_container_width=True): navigate_to("admin_home")


# ----------------------------------------
# TRANG CHAT (HÀM DÙNG CHUNG ĐỂ RENDER UI CHAT)
# ----------------------------------------
def render_chat_ui(chat_history_key, title, subtitle):
    st.header(title)
    st.caption(subtitle)
    
    # Hiển thị lịch sử tin nhắn
    for message in st.session_state[chat_history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ô nhập liệu chat
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Thêm tin nhắn user vào lịch sử
        st.session_state[chat_history_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Mô phỏng AI trả lời
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            simulated_response = f"Đây là câu trả lời giả lập cho luồng '{title}'. Bạn vừa hỏi: '{prompt}'. Sau này thay bằng API gọi xuống Backend nhé!"
            for chunk in simulated_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
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
    render_chat_ui("chat_quyche", "💬 Trợ lý Quy chế", "Hỏi đáp mọi thứ về Sổ tay sinh viên và Quy chế thi.")

elif st.session_state.page == "chat_lichthi":
    st.header("📅 Lịch thi & Trợ lý Khảo thí")
    
    # 1. KHU VỰC IN LỊCH THI
    st.markdown("##### Bảng lịch thi sắp tới của bạn:")
    df_exams = pd.DataFrame([
        {"Môn thi": "PRM392", "Ngày thi": "15/05/2026", "Giờ thi": "07:30 AM", "Phòng": "P.202 Alpha", "Hình thức": "Thực hành (PE)"},
        {"Môn thi": "SWE201", "Ngày thi": "18/05/2026", "Giờ thi": "09:45 AM", "Phòng": "P.101 Beta", "Hình thức": "Lý thuyết (FE)"},
    ])
    st.dataframe(df_exams, use_container_width=True, hide_index=True)
    st.divider()
    
    # 2. KHU VỰC CHATBOT BÊN DƯỚI
    render_chat_ui("chat_lichthi", "🤖 Hỏi đáp lịch thi", "Bạn có thắc mắc gì về danh sách môn thi ở trên không?")

elif st.session_state.page == "chat_ontap":
    render_chat_ui("chat_ontap", "📚 Trợ lý Ôn tập", "Tóm tắt slide, tạo flashcard hoặc yêu cầu tôi tạo bài thi thử nghiệm.")

# ----------------------------------------
# TRANG ADMIN: QUẢN LÝ DỮ LIỆU
# ----------------------------------------
elif st.session_state.page == "admin_home":
    st.header("⚙️ Quản trị Hệ thống GC-Proctor")
    st.markdown("Quản lý nguồn dữ liệu (Knowledge Base) cho AI RAG và cơ sở dữ liệu hệ thống.")
    
    # Tạo các Tab để chia chức năng dễ nhìn
    tab1, tab2, tab3 = st.tabs(["📤 Import Dữ liệu (Upload)", "📖 Quản lý Quy chế (Tài liệu)", "📅 Quản lý Lịch thi"])
    
    with tab1:
        st.subheader("Import file Quy chế / Lịch thi")
        uploaded_file = st.file_uploader("Chọn file PDF, DOCX hoặc CSV", type=["pdf", "docx", "csv"])
        if uploaded_file is not None:
            doc_type = st.radio("Loại tài liệu này là gì?", ["Quy chế / Hướng dẫn", "Danh sách Lịch thi sinh viên"])
            if st.button("🚀 Upload và Xử lý (Embedding)"):
                with st.spinner("Đang đẩy file xuống backend xử lý Vector DB..."):
                    time.sleep(2) # Giả lập chờ API
                st.success(f"Đã import thành công file: {uploaded_file.name} vào hệ thống!")

    with tab2:
        st.subheader("Danh sách Tài liệu / Quy chế hiện có")
        # Giả lập data Editor (cho phép sửa xóa trực tiếp trên bảng)
        df_docs = pd.DataFrame([
            {"ID": "DOC_01", "Tên tài liệu": "Quy chế thi 2024.pdf", "Trạng thái": "Active", "Ngày upload": "10/01/2026"},
            {"ID": "DOC_02", "Tên tài liệu": "Sổ tay Sinh viên V3.pdf", "Trạng thái": "Active", "Ngày upload": "15/02/2026"},
        ])
        # data_editor cho phép user tích chọn và sửa text ngay trên UI
        edited_df = st.data_editor(df_docs, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Lưu thay đổi Tài liệu"):
            st.toast("Đã lưu cập nhật quy chế xuống Database!", icon="✅")

    with tab3:
        st.subheader("Cơ sở dữ liệu Lịch thi toàn trường")
        st.caption("Admin có thể xem, thêm, sửa, xóa các ca thi tại đây.")
        df_schedules = pd.DataFrame([
            {"Mã SV": "SE160001", "Môn": "PRM392", "Ngày": "15/05", "Giờ": "07:30", "Phòng": "202 Alpha"},
            {"Mã SV": "SE160001", "Môn": "SWE201", "Ngày": "18/05", "Giờ": "09:45", "Phòng": "101 Beta"},
            {"Mã SV": "SS170022", "Môn": "MKT101", "Ngày": "15/05", "Giờ": "13:30", "Phòng": "305 Gamma"},
        ])
        edited_schedules = st.data_editor(df_schedules, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Lưu thay đổi Lịch thi"):
            st.toast("Đã cập nhật lịch thi thành công!", icon="✅")