from datetime import datetime
from uuid import uuid4
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
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
from services.help_request_service import HelpRequestService
from services.user_service import UserService
from services.chat_session_service import ChatSessionService
from services.chat_message_service import ChatMessageService
from models.chat_session_model import ChatSessionModel
from models.chat_message_model import ChatMessageModel
from utils.study_content_utils import generate_flashcards_markdown, generate_mindmap_payload
from utils.mindmap_builder import generate_mindmap_js
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
        "study_svc": StudyService(),
        "help_request_service": HelpRequestService(),
        "user_svc": UserService(),
        "chat_session_svc": ChatSessionService(),
        "chat_message_svc": ChatMessageService(),
    }

services = get_services()
reg_service = services["regulation_service"]
exam_service = services["exam_service"]
kb_service = services["kb_service"]
chat_service = services["chat_service"]
exam_schedule_svc = services["exam_schedule_svc"]
study_svc = services["study_svc"]
help_request_service = services["help_request_service"]
user_svc = services["user_svc"]
chat_session_svc = services["chat_session_svc"]
chat_message_svc = services["chat_message_svc"]

# Khởi tạo các biến trạng thái (Session State) để lưu lịch sử và điều hướng
if "page" not in st.session_state:
    st.session_state.page = "home" 
if "role" not in st.session_state:
    st.session_state.role = None 

# Khởi tạo lịch sử chat riêng cho 4 luồng
if "chat_quyche" not in st.session_state:
    st.session_state.chat_quyche = [{"role": "assistant", "content": "Chào bạn, tôi là chuyên gia về Quy chế Khảo thí. Bạn cần hỏi gì?"}]
if "chat_lichthi" not in st.session_state:
    st.session_state.chat_lichthi = [{"role": "assistant", "content": "Dưới đây là lịch thi của bạn. Bạn có thắc mắc gì về phòng máy, giờ thi hay môn thi không?"}]
if "chat_ontap" not in st.session_state:
    st.session_state.chat_ontap = [{"role": "assistant", "content"
                                    : "Sẵn sàng ôn tập! Gửi cho tôi slide bài giảng hoặc chủ đề bạn muốn luyện tập."}]
if "chat_bot_guidance" not in st.session_state:
    st.session_state.chat_bot_guidance = [
        {
            "role": "assistant",
            "content": "Xin chào, tôi là trợ lý vận hành. Bạn có thể hỏi cách sử dụng các chức năng phía sinh viên trong GC-Proctor.",
        }
    ]

# Khởi tạo student_id cho session (dùng cho tra cứu lịch thi)
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "user_code" not in st.session_state:
    st.session_state.user_code = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "full_name" not in st.session_state:
    st.session_state.full_name = None

if "student_chat_active_session_id" not in st.session_state:
    st.session_state.student_chat_active_session_id = None
if "student_chat_force_new" not in st.session_state:
    st.session_state.student_chat_force_new = False
if "admin_dashboard_view" not in st.session_state:
    st.session_state.admin_dashboard_view = "home"


# Khởi tạo state cho yêu cầu hỗ trợ
if "help_session_id" not in st.session_state:
    st.session_state.help_session_id = None
if "admin_help_last_count" not in st.session_state:
    st.session_state.admin_help_last_count = 0
if "support_creating_new" not in st.session_state:
    st.session_state.support_creating_new = False
if "admin_help_session_id" not in st.session_state:
    st.session_state.admin_help_session_id = None
if "bot_escalation_session_id" not in st.session_state:
    st.session_state.bot_escalation_session_id = None
if "admin_bot_session_id" not in st.session_state:
    st.session_state.admin_bot_session_id = None
if "bot_escalate_target_idx" not in st.session_state:
    st.session_state.bot_escalate_target_idx = None
if "inline_mindmap_payload" not in st.session_state:
    st.session_state.inline_mindmap_payload = None

# Hàm điều hướng trang
def navigate_to(page_name, role=None):
    st.session_state.page = page_name
    if role:
        st.session_state.role = role


def logout_portal_user():
    st.session_state.role = None
    st.session_state.page = "home"
    st.session_state.student_id = None
    st.session_state.user_code = None
    st.session_state.user_id = None
    st.session_state.full_name = None


def authenticate_portal_user(user_code: str, password: str, selected_role: str):
    normalized_user_code = _safe_str(user_code)
    normalized_role = _safe_str(selected_role).lower()

    if not normalized_user_code:
        return False, "Vui lòng nhập mã số.", None

    matched_user = None
    lookup_variants = [normalized_user_code, normalized_user_code.upper(), normalized_user_code.lower()]
    if hasattr(user_svc, "get_user_by_userCode"):
        for candidate in lookup_variants:
            if candidate:
                matched_user = user_svc.get_user_by_userCode(candidate)
                if matched_user:
                    break
    if not matched_user:
        for user in user_svc.get_all_users():
            if _safe_str(user.get_userCode()).lower() == normalized_user_code.lower():
                matched_user = user
                break

    if not matched_user:
        return False, "Không tìm thấy tài khoản với mã số này.", None

    if _safe_str(matched_user.get_role()).lower() != normalized_role:
        return False, "Role đã chọn không khớp với tài khoản.", None

    if not _as_bool(matched_user.get_state(), default=True):
        return False, "Tài khoản đang bị khóa.", None

    return (
        True,
        None,
        {
            "user_id": _safe_str(matched_user.get_id()),
            "user_code": _safe_str(matched_user.get_userCode()).upper(),
            "role": _safe_str(matched_user.get_role()).lower(),
            "full_name": _safe_str(matched_user.get_fullName()),
        },
    )

def _safe_str(value) -> str:
    if value is None:
        return ""
    return str(value).strip()

def _as_bool(value, default=True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return _safe_str(value).lower() in {"1", "true", "yes", "y", "active", "on"}


def _format_bot_transcript(messages, max_turns=12) -> str:
    recent_messages = messages[-max_turns:]
    lines = []
    for msg in recent_messages:
        role = "Sinh viên" if msg.get("role") == "user" else "Bot"
        content = _safe_str(msg.get("content"))
        if content:
            lines.append(f"- {role}: {content}")
    return "\n".join(lines)


def _get_open_help_request_count() -> int:
    try:
        result = help_request_service.get_help_sessions(include_closed=False, limit=500)
        return int(result.get("count", 0))
    except Exception:
        return 0


STUDENT_CHAT_CHANNEL = "student_chat"
STUDENT_CHAT_MODES = {
    "regulation": {
        "label": "Tra cuu quy che",
        "icon": "📘",
        "welcome": "Xin chào! Tôi là trợ lý Quy chế. Bạn muốn hỏi điều khoản nào?",
        "spinner": "Đang tra cứu quy chế...",
    },
    "exam": {
        "label": "Lich thi",
        "icon": "🗓️",
        "welcome": "Xin chào! Tôi là trợ lý Lịch thi. ạn cần kiểm tra lịch thi nào?",
        "spinner": "Đang tra cứu lịch thi...",
    },
    "study": {
        "label": "On tap",
        "icon": "📚",
        "welcome": "Xin chào! Tôi là trợ lý Ôn tập. Bạn đang cần ôn chủ đề gì?",
        "spinner": "Đang tìm nội dung ôn tập...",
    },
}


def _parse_datetime(value):
    if value is None:
        return datetime.min
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return datetime.min


def _format_datetime_short(value) -> str:
    dt = _parse_datetime(value)
    if dt == datetime.min:
        return ""
    return dt.strftime("%d/%m %H:%M")


def _mode_label(mode: str) -> str:
    mode_key = _safe_str(mode).lower()
    return STUDENT_CHAT_MODES.get(mode_key, {}).get("label", "Unknown")


def _mode_icon(mode: str) -> str:
    mode_key = _safe_str(mode).lower()
    return STUDENT_CHAT_MODES.get(mode_key, {}).get("icon", "💬")


def _mode_welcome(mode: str) -> str:
    mode_key = _safe_str(mode).lower()
    return STUDENT_CHAT_MODES.get(mode_key, {}).get("welcome", "Xin chao! Ban can ho tro gi?")


def _mode_spinner(mode: str) -> str:
    mode_key = _safe_str(mode).lower()
    return STUDENT_CHAT_MODES.get(mode_key, {}).get("spinner", "Dang xu ly...")


def _resolve_workspace_path(path_str: str) -> Path:
    normalized = _safe_str(path_str).replace("\\", "/")
    base_dir = Path(__file__).resolve().parent
    candidates = [
        Path(normalized),
        base_dir / normalized,
    ]

    if normalized.startswith("src/"):
        trimmed = normalized[len("src/"):]
        candidates.extend([Path(trimmed), base_dir / trimmed])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def _render_mindmap_inline(nodes: list, viewer_file: str) -> None:
    viewer_path = _resolve_workspace_path(viewer_file or "src/tmp/gc_mindmap.html")
    if not viewer_path.exists():
        st.error(f"❌ Không tìm thấy file viewer mindmap: {viewer_path}")
        return

    try:
        html_text = viewer_path.read_text(encoding="utf-8")
    except Exception as e:
        st.error(f"❌ Không thể đọc file viewer: {e}")
        return

    inline_data_script = f"<script>window.externalData = {json.dumps(nodes or [], ensure_ascii=False)};</script>"
    if '<script src="./data.js"></script>' in html_text:
        html_text = html_text.replace('<script src="./data.js"></script>', inline_data_script, 1)
    else:
        html_text = inline_data_script + "\n" + html_text

    st.markdown("### 🗺️ Sơ đồ tư duy")
    components.html(html_text, height=760, scrolling=True)


def _show_inline_mindmap_panel() -> None:
    payload = st.session_state.get("inline_mindmap_payload")
    if not isinstance(payload, dict):
        return

    nodes = payload.get("nodes", [])
    viewer = _safe_str(payload.get("viewer")) or "src/tmp/gc_mindmap.html"
    if not isinstance(nodes, list) or not nodes:
        return

    col_open, col_close = st.columns([5, 1])
    with col_close:
        if st.button("✖ Đóng", key="close_inline_mindmap", use_container_width=True):
            st.session_state.inline_mindmap_payload = None
            st.rerun()

    _render_mindmap_inline(nodes, viewer)


def _is_mindmap_request(prompt: str) -> bool:
    normalized = _safe_str(prompt).lower()
    keywords = [
        "mindmap",
        "mind map",
        "sơ đồ tư duy",
        "so do tu duy",
        "vẽ sơ đồ",
        "ve so do",
    ]
    return any(keyword in normalized for keyword in keywords)


def _create_student_chat_session(user_id: str, mode: str) -> str:
    session_id = f"chat-{int(datetime.utcnow().timestamp() * 1000)}-{uuid4().hex[:6]}"
    session = ChatSessionModel(
        id=session_id,
        userId=user_id,
        channel=STUDENT_CHAT_CHANNEL,
        persona=mode,
        sessionStatus="open",
        startedAt=datetime.utcnow().isoformat(),
        endedAt=None,
        isActive=True,
    )
    created_id = chat_session_svc.create_chat_session(session)
    if not created_id:
        raise RuntimeError("Khong tao duoc chat session")
    _append_chat_message(session_id, "assistant", _mode_welcome(mode), mode)
    return session_id


def _append_chat_message(
    session_id: str,
    sender_type: str,
    content: str,
    mode: str,
    links=None,
    intent_override: str = "",
    entities_extra=None,
    citations=None,
) -> str:
    message_id = f"msg-{int(datetime.utcnow().timestamp() * 1000)}-{uuid4().hex[:6]}"
    entities = {"links": links or []}
    if isinstance(entities_extra, dict):
        entities.update(entities_extra)
    resolved_citations = citations if isinstance(citations, dict) else {}
    message = ChatMessageModel(
        id=message_id,
        sessionId=session_id,
        senderType=sender_type,
        intent=_safe_str(intent_override) or mode,
        content=content,
        citations=resolved_citations,
        entities=entities,
        createdAt=datetime.utcnow().isoformat(),
        isActive=True,
    )
    created_id = chat_message_svc.create_chat_message(message)
    if not created_id:
        raise RuntimeError("Không lưu được tin nhắn chat")
    return created_id


def _load_student_sessions(user_id: str):
    if not user_id:
        return []
    sessions = []
    for session in chat_session_svc.get_all_chat_sessions():
        if _safe_str(session.get_userId()) != _safe_str(user_id):
            continue
        if _safe_str(session.get_channel()) != STUDENT_CHAT_CHANNEL:
            continue
        if not _as_bool(session.get_state(), default=True):
            continue
        sessions.append(
            {
                "session_id": session.get_id(),
                "mode": _safe_str(session.get_persona()).lower(),
                "status": _safe_str(session.get_sessionStatus()).lower(),
                "started_at": session.get_startedAt(),
            }
        )
    sessions.sort(key=lambda x: _parse_datetime(x.get("started_at")), reverse=True)
    return sessions


def _load_session_messages(session_id: str, limit: int = 200):
    if not session_id:
        return []
    messages = []
    for msg in chat_message_svc.get_messages_by_session(session_id, limit=limit):
        links = []
        entities = msg.get_entities() or {}
        mindmap_nodes = []
        if isinstance(entities, dict):
            candidate_links = entities.get("links")
            if isinstance(candidate_links, list):
                links = candidate_links
            if entities.get("type") == "mindmap" and isinstance(entities.get("nodes"), list):
                mindmap_nodes = entities.get("nodes")

        citations = msg.get_citations() or {}
        messages.append(
            {
                "sender": _safe_str(msg.get_senderType()).lower(),
                "content": _safe_str(msg.get_content()),
                "created_at": msg.get_createdAt(),
                "links": links,
                "mindmap_nodes": mindmap_nodes,
                "citations": citations if isinstance(citations, dict) else {},
            }
        )
    messages.sort(key=lambda x: _parse_datetime(x.get("created_at")))
    return messages


def _get_session_mode(session_id: str, fallback_mode: str = "regulation") -> str:
    if not session_id:
        return fallback_mode
    session = chat_session_svc.get_chat_session(session_id)
    if not session:
        return fallback_mode
    mode = _safe_str(session.get_persona()).lower()
    return mode if mode in STUDENT_CHAT_MODES else fallback_mode


def _generate_unified_chat_answer(mode: str, prompt: str, student_id: str):
    mode_key = _safe_str(mode).lower()
    if mode_key == "regulation":
        answer = reg_service.answer_regulation_question(prompt)
        links = []
        regulations = reg_service.get_all_regulations()
        if regulations:
            top_reg = regulations[0]
            links = [{"title": top_reg.get_title(), "url": top_reg.get_sourceUrl()}]
        return answer, links, {}, {}, mode_key

    if mode_key == "exam":
        if not _safe_str(student_id):
            return "Không tìm thấy mã sinh viên trong phiên đăng nhập. Vui lòng đăng nhập lại.", [], {}, {}, mode_key
        answer = exam_service.answer_exam_question(student_id, prompt)
        return answer, [], {}, {}, mode_key

    chunks = kb_service.retrieve_relevant_chunks(prompt, "ALL")
    if not chunks:
        return "Chưa tìm thấy nội dung phù hợp trong kho tài liệu ôn tập hiện có.", [], {}, {}, mode_key

    context = "\n\n".join([c.get("content", "") for c in chunks])

    if _is_mindmap_request(prompt):
        mindmap_result = generate_mindmap_payload(study_svc, prompt, context, chunks, output_file="src/tmp/data.js")
        nodes = mindmap_result.get("nodes", []) if isinstance(mindmap_result, dict) else []
        if mindmap_result.get("ok") and nodes:
            entities = {"type": "mindmap", "nodes": nodes}
            citations = {
                "renderer": "gc_mindmap",
                "viewer": "src/tmp/gc_mindmap.html",
                "dataFile": "src/tmp/data.js",
            }
            return mindmap_result.get("message", "Đã tạo sơ đồ tư duy."), [], entities, citations, "provide_mindmap"
        return mindmap_result.get("message", "Không thể tạo sơ đồ tư duy."), [], {}, {}, mode_key

    sys_prompt = (
        "Bạn là trợ lý ôn tập cho sinh viên. "
        "Chỉ được phép trả lời dựa trên tài liệu được cung cấp. "
        "Nếu tài liệu không đủ để trả lời, hãy nói rõ điều đó.\n\n"
        f"TÀI LIỆU:\n{context}\n\n"
        f"CÂU HỎI: {prompt}"
    )
    response = study_svc.model.generate_content(sys_prompt)
    return response.text, [], {}, {}, mode_key


def render_unified_student_chat_page():
    st.header("GC Proctor")
    st.caption("Một session chỉ gắn với một thể loại chat. Muốn đổi thể loại, hay tạo session mới.")

    user_id = _safe_str(st.session_state.get("user_id"))
    student_id = _safe_str(st.session_state.get("student_id"))
    if not user_id:
        st.error("Không tìm thấy thông tin người dùng trong phiên đăng nhập. Vui lòng đăng nhập lại.")
        return

    sessions = _load_student_sessions(user_id)
    active_session_id = _safe_str(st.session_state.get("student_chat_active_session_id"))
    force_new = bool(st.session_state.get("student_chat_force_new"))

    if active_session_id and not any(s["session_id"] == active_session_id for s in sessions):
        active_session_id = ""
        st.session_state.student_chat_active_session_id = None

    if not active_session_id and sessions and not force_new:
        active_session_id = sessions[0]["session_id"]
        st.session_state.student_chat_active_session_id = active_session_id

    if force_new or not active_session_id:
        st.info("Bắt đầu bằng cách nhập câu hỏi đầu tiên và chọn thể loại chat session.")
        with st.form("new_unified_chat_session_form", clear_on_submit=False):
            selected_mode = st.selectbox(
                "Thể loại",
                options=list(STUDENT_CHAT_MODES.keys()),
                format_func=lambda key: f"{_mode_icon(key)} {_mode_label(key)}",
            )
            initial_prompt = st.text_area("Prompt khởi tạo", placeholder="Nhập câu hỏi đầu tiên của bạn...", height=120)
            create_clicked = st.form_submit_button("Tạo session và gửi", use_container_width=True, type="primary")

        if create_clicked:
            if not _safe_str(initial_prompt):
                st.warning("Vui lòng nhập prompt khởi tạo để bắt đầu cuộc trò chuyện.")
            else:
                try:
                    new_session_id = _create_student_chat_session(user_id, selected_mode)
                    _append_chat_message(new_session_id, "user", initial_prompt, selected_mode)
                    with st.spinner(_mode_spinner(selected_mode)):
                        answer, links, entities, citations, intent_value = _generate_unified_chat_answer(selected_mode, initial_prompt, student_id)
                    _append_chat_message(
                        new_session_id,
                        "assistant",
                        answer,
                        selected_mode,
                        links=links,
                        intent_override=intent_value,
                        entities_extra=entities,
                        citations=citations,
                    )
                    st.session_state.student_chat_active_session_id = new_session_id
                    st.session_state.student_chat_force_new = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Khong the tao session moi: {e}")
        return

    active_mode = _get_session_mode(active_session_id)
    st.caption(f"Session: {active_session_id} | The loai: {_mode_icon(active_mode)} {_mode_label(active_mode)}")

    messages = _load_session_messages(active_session_id, limit=300)
    for idx, msg in enumerate(messages):
        role = "user" if msg.get("sender") == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg.get("content", ""))
            for link in msg.get("links", []):
                title = _safe_str(link.get("title"))
                url = _safe_str(link.get("url"))
                if title and url:
                    st.caption(f"🔗 [Nguon: {title}]({url})")

            mindmap_nodes = msg.get("mindmap_nodes", [])
            if isinstance(mindmap_nodes, list) and mindmap_nodes:
                citations = msg.get("citations", {}) if isinstance(msg.get("citations"), dict) else {}
                viewer_file = _safe_str(citations.get("viewer")) or "src/tmp/gc_mindmap.html"
                data_file = _safe_str(citations.get("dataFile")) or "src/tmp/data.js"
                if st.button("🗺️ Xem sơ đồ", key=f"view_mindmap_{active_session_id}_{idx}"):
                    try:
                        generate_mindmap_js(
                            json.dumps({"nodes": mindmap_nodes}, ensure_ascii=False),
                            output_file=data_file,
                        )
                        st.session_state.inline_mindmap_payload = {
                            "nodes": mindmap_nodes,
                            "viewer": viewer_file,
                        }
                        st.success(f"✅ Đã cập nhật dữ liệu sơ đồ tại {data_file}.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Không thể render sơ đồ: {e}")

    _show_inline_mindmap_panel()

    if prompt := st.chat_input("Hoi tiep trong session hien tai..."):
        try:
            _append_chat_message(active_session_id, "user", prompt, active_mode)
            with st.spinner(_mode_spinner(active_mode)):
                answer, links, entities, citations, intent_value = _generate_unified_chat_answer(active_mode, prompt, student_id)
            _append_chat_message(
                active_session_id,
                "assistant",
                answer,
                active_mode,
                links=links,
                intent_override=intent_value,
                entities_extra=entities,
                citations=citations,
            )
            st.rerun()
        except Exception as e:
            st.error(f"Khong the xu ly tin nhan: {e}")

# ==========================================
# 2. THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("GC-Proctor")

    if st.session_state.role:
        role_label = "Sinh viên" if st.session_state.role == "student" else "Admin"
        st.caption(f"Đang đăng nhập: {st.session_state.get('user_code', 'N/A')} ({role_label})")
        if st.button("Đăng xuất", width="stretch"):
            logout_portal_user()
            st.rerun()
    st.markdown("---")
    
    # Menu cho Sinh viên
    if st.session_state.role == "student":
        st.caption("DASHBOARD STUDENT")
        if st.button("✨ Cuộc trò chuyện mới", width="stretch"):
            st.session_state.student_chat_force_new = True
            st.session_state.student_chat_active_session_id = None
            navigate_to("chat_hub")
            st.rerun()
        if st.button("💬 Đoạn chat hiện tại", width="stretch"):
            st.session_state.student_chat_force_new = False
            navigate_to("chat_hub")
            st.rerun()
        if st.button("🆘 Yêu cầu hỗ trợ", use_container_width=True):
            navigate_to("chat_bot_guidance")
            st.rerun()
        if st.button("🔄 Làm mới danh sách", use_container_width=True, key="student_support_refresh_sidebar"):
            navigate_to("chat_bot_guidance")
            st.rerun()
            
        st.markdown("---")
        st.caption("Lịch sử")
        current_user_id = _safe_str(st.session_state.get("user_id"))
        student_sessions = _load_student_sessions(current_user_id)
        if not student_sessions:
            st.caption("Chưa có session nào")
        else:
            for sess in student_sessions[:25]:
                sid = sess.get("session_id")
                mode = sess.get("mode")
                started = _format_datetime_short(sess.get("started_at"))
                label = f"{_mode_icon(mode)} {_mode_label(mode)}"
                if started:
                    label = f"{label} • {started}"
                if st.button(label, key=f"student_session_btn_{sid}", use_container_width=True):
                    st.session_state.student_chat_active_session_id = sid
                    st.session_state.student_chat_force_new = False
                    navigate_to("chat_hub")
                    st.rerun()
        
    # Menu cho Admin
    elif st.session_state.role == "admin":
        st.caption("DASHBOARD ADMIN")
        open_help_count = _get_open_help_request_count()
        if open_help_count > st.session_state.get("admin_help_last_count", 0):
            st.toast(f"🔔 Có {open_help_count} yêu cầu hỗ trợ đang mở")
        st.session_state.admin_help_last_count = open_help_count

        if st.button("📊 Trang quản lý", use_container_width=True):
            st.session_state.admin_dashboard_view = "home"
            navigate_to("admin_home")

        if st.button("📚 Upload Quy chế", use_container_width=True):
            st.session_state.admin_dashboard_view = "regulation"
            navigate_to("admin_home")

        if st.button("📅 Quản lý Lịch thi", use_container_width=True):
            st.session_state.admin_dashboard_view = "exam"
            navigate_to("admin_home")

        support_btn_label = f"🆘 Hỗ trợ User ({open_help_count})"
        if st.button(support_btn_label, use_container_width=True):
            st.session_state.admin_dashboard_view = "support"
            navigate_to("admin_home")

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
                        ai_response = exam_service.answer_exam_question(student_id, prompt)
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
    # st.markdown("<h1 style='text-align: center;'>GC-Proctor</h1>", unsafe_allow_html=True)
    # st.markdown("<p style='text-align: center;'>Đăng nhập bằng mã số, mật khẩu và chọn đúng role.</p><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.info("### ĐĂNG NHẬP\n Đăng nhập bằng mã số, mật khẩu và chọn đúng role")
        with st.form("portal_login_form", clear_on_submit=False):
            login_user_code = st.text_input("Mã số", placeholder="VD: 312241000 hoặc 3121410005")
            login_password = st.text_input("Mật khẩu", type="password", placeholder="Nhập gì cũng được")
            st.caption("Mật khẩu chỉ là trường mô phỏng, hệ thống sẽ dùng mã số để xác định thông tin sinh viên/admin.")
            login_role = st.selectbox(
                "Role",
                options=["student", "admin"],
                format_func=lambda role: "Sinh viên" if role == "student" else "Admin",
            )
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True, type="primary")

            if submitted:
                ok, error_message, user_payload = authenticate_portal_user(
                    login_user_code,
                    login_password,
                    login_role,
                )
                if not ok:
                    st.error(f"❌ {error_message}")
                else:
                    st.session_state.role = user_payload["role"]
                    st.session_state.user_id = user_payload["user_id"]
                    st.session_state.user_code = user_payload["user_code"]
                    st.session_state.full_name = user_payload["full_name"]

                    # Lưu mã sinh viên cho toàn bộ các tính năng cần student_id.
                    if user_payload["role"] == "student":
                        st.session_state.student_id = user_payload["user_code"]
                        st.session_state.student_chat_force_new = True
                        st.session_state.student_chat_active_session_id = None
                        navigate_to("chat_hub", "student")
                    else:
                        st.session_state.student_id = None
                        navigate_to("admin_home", "admin")
                    st.rerun()

elif st.session_state.page == "student_home":
    st.session_state.student_chat_force_new = True
    st.session_state.student_chat_active_session_id = None
    navigate_to("chat_hub", "student")
    st.rerun()

elif st.session_state.page == "chat_hub":
    render_unified_student_chat_page()

elif st.session_state.page == "chat_quyche":
    render_chat_ui("chat_quyche", "💬 Trợ lý Quy chế", "Hỏi đáp mọi thứ về Sổ tay sinh viên và Quy chế thi.", is_rag=True)

elif st.session_state.page == "chat_lichthi":
    st.header("📅 Lịch thi & Trợ lý Khảo thí")

    student_id = _safe_str(st.session_state.get("student_id"))
    if not student_id:
        st.error("⚠️ Chưa có mã sinh viên trong phiên đăng nhập. Vui lòng đăng nhập lại bằng tài khoản sinh viên.")
        if st.button("↩️ Quay về trang đăng nhập", use_container_width=True):
            navigate_to("home", None)
            st.rerun()
        st.stop()

    st.info(f"ℹ️ Bạn đang tra cứu theo Mã sinh viên: **{student_id}**")
    
    st.divider()
    
    st.markdown("##### Bảng lịch thi sắp tới:")
    try:
        upcoming_exams = exam_schedule_svc.get_upcoming_exams(student_id)
        if upcoming_exams:
            df_exams = pd.DataFrame(
                [
                    {
                        "Mã môn thi": exam.get("examId", ""),
                        "Ngày thi": exam.get("examDate", ""),
                        "Giờ thi": exam.get("startTime", ""),
                        "Phòng": exam.get("room", ""),
                        "Trạng thái": exam.get("status", ""),
                    }
                    for exam in upcoming_exams
                ]
            )
            st.dataframe(df_exams, hide_index=True, use_container_width=True)
        else:
            st.info("Chưa có lịch thi nào được gán cho mã sinh viên này trong database.")
    except Exception as e:
        st.error(f"Không thể tải lịch thi từ database: {e}")
    st.divider()
    
    render_chat_ui("chat_lichthi", "🤖 Hỏi đáp lịch thi", "Bạn có thắc mắc gì về danh sách môn thi ở trên không?", is_exam_lookup=True)

elif st.session_state.page == "chat_ontap":
    st.header("📚 Trợ Lý Ôn Tập AI Toàn Năng")

    # ==========================================
    # 1. KHU VỰC TẢI TÀI LIỆU
    # ==========================================
    with st.expander("📁 Tải lên tài liệu bài giảng (PDF/DOCX) để AI học"):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            uploaded_doc = st.file_uploader("File", type=["pdf", "docx"], label_visibility="collapsed")
        with c2:
            course_code = st.text_input("Mã môn", placeholder="VD: PRM392", label_visibility="collapsed")
        with c3:
            if st.button("🚀 Bắt đầu học", width="stretch"):
                if uploaded_doc and course_code:
                    with st.spinner("AI đang đọc và ghi nhớ tài liệu..."):
                        try:
                            import base64
                            file_bytes = uploaded_doc.getvalue()
                            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
                            kb_service.upload_document(encoded_file, course_code.upper(), uploaded_doc.name)
                            
                            st.session_state.chat_ontap.append({"role": "assistant", "content": f"✅ Đã thuộc nằm lòng tài liệu **{uploaded_doc.name}**! Bạn có thể hỏi mình bất cứ điều gì về nó."})
                            st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
                else:
                    st.warning("Thiếu file hoặc mã môn!")

    # ==========================================
    # 2. KHU VỰC CHAT THUẦN TÚY (AI AGENT)
    # ==========================================
    st.divider()
    
    col_title, col_clear = st.columns([5, 1])
    with col_title:
        st.markdown(f"**Phạm vi tìm kiếm:** `Tất cả tài liệu trên hệ thống`")
    with col_clear:
        if st.button("🗑️ Xoá Chat", width="stretch"):
            st.session_state.chat_ontap = [{"role": "assistant", "content": "Sẵn sàng! Bạn cần tìm hiểu hoặc ôn tập kiến thức gì?"}]
            st.rerun()

    # Khung hiển thị chat
    chat_container = st.container(height=500, border=True)
    with chat_container:
        for idx, message in enumerate(st.session_state.chat_ontap):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                entities = message.get("entities", {}) if isinstance(message, dict) else {}
                if isinstance(entities, dict) and entities.get("type") == "mindmap" and isinstance(entities.get("nodes"), list):
                    if st.button("🗺️ Xem sơ đồ", key=f"legacy_mindmap_btn_{idx}"):
                        try:
                            mindmap_nodes = entities.get("nodes", [])
                            generate_mindmap_js(
                                json.dumps({"nodes": mindmap_nodes}, ensure_ascii=False),
                                output_file="src/tmp/data.js",
                            )
                            st.session_state.inline_mindmap_payload = {
                                "nodes": mindmap_nodes,
                                "viewer": "src/tmp/gc_mindmap.html",
                            }
                            st.success("✅ Đã cập nhật dữ liệu tại src/tmp/data.js.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Không thể render sơ đồ: {e}")

    _show_inline_mindmap_panel()

    # Ô nhập liệu duy nhất
    if prompt := st.chat_input("Hỏi kiến thức (VD: AI là gì? OOP là gì?)..."):
        st.session_state.chat_ontap.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                assistant_entities = {}
                with st.spinner("Đang lục tìm trong toàn bộ hệ thống..."):
                    
                    # 1. Tìm trong TẤT CẢ tài liệu (Bỏ giới hạn mã môn, dùng "ALL")
                    chunks = kb_service.retrieve_relevant_chunks(prompt, "ALL")
                    context = "\n\n".join([c.get("content", "") for c in chunks]) if chunks else ""

                    # 2. Đưa cho LLM đánh giá xem tài liệu CÓ chứa câu trả lời hay không
                    sys_prompt = f"""
                    Nhiệm vụ: Bạn là trợ lý ôn tập kiến thức cho sinh viên. Bạn là một người trợ lí có giọng điệu nhí nhảnh và luôn hỗ trợ sinh viên hết mình.
                    
                    CÂU HỎI / YÊU CẦU CỦA SINH VIÊN: "{prompt}"
                    
                    HÃY PHÂN TÍCH CÂU HỎI VÀ ĐỐI CHIẾU VỚI TÀI LIỆU, SAU ĐÓ BẮT BUỘC PHẢI LÀM THEO 1 TRONG 5 QUY TẮC DƯỚI ĐÂY:
                    
                    1. NÊU CẦU NGOÀI LỀ: Nếu ý định của họ KHÔNG liên quan gì đến học tập, ôn thi (ví dụ hỏi thời tiết, trêu đùa), CHỈ TRẢ LỜI ĐÚNG 1 CHỮ: OUT_OF_SCOPE
                    
                    2. KHÔNG CÓ THÔNG TIN TRONG TÀI LIỆU: Nếu họ hỏi kiến thức (VD: "AI là gì?"), nhưng TÀI LIỆU BÊN DƯỚI KHÔNG CHỨA THÔNG TIN ĐÓ, bạn KHÔNG ĐƯỢC bẻ lái sang chuyện khác, mà CHỈ TRẢ LỜI ĐÚNG 1 CHỮ: NO_DATA
                    
                    3. YÊU CẦU FLASHCARD: Nếu sinh viên muốn tạo thẻ ghi nhớ, flashcard, CHỈ TRẢ LỜI ĐÚNG 1 CHỮ: ACTION_FLASHCARD
                    
                    4. YÊU CẦU MINDMAP: Nếu sinh viên muốn vẽ sơ đồ tư duy, mindmap, CHỈ TRẢ LỜI ĐÚNG 1 CHỮ: ACTION_MINDMAP
                    
                    5. CÓ THÔNG TIN: Nếu tài liệu THỰC SỰ CÓ CHỨA thông tin để giải đáp, hãy trả lời chi tiết, dùng nhiều emoji nhí nhảnh. TUYỆT ĐỐI không tự bịa thêm kiến thức ngoài tài liệu.

                    TÀI LIỆU CỦA HỆ THỐNG:
                    {context}
                    """
                    
                    try:
                        llm_response = study_svc.model.generate_content(sys_prompt).text.strip()

                        # --- NHÁNH 1: HỎI NGOÀI LỀ ---
                        if "OUT_OF_SCOPE" in llm_response:
                            ai_response = "⚠️ Hihi, câu hỏi này nằm ngoài chuyên môn của mình mất rồi! Mình chỉ giúp bạn ôn thi thôi nha! 📚"

                        # --- NHÁNH 2: HỎI TRÚNG NHƯNG KHÔNG CÓ DATA -> CRAWL WEB ---
                        elif "NO_DATA" in llm_response or not chunks:
                            message_placeholder.markdown("🔍 *Không có trong kho lưu trữ, đang cào dữ liệu trên TailieuHUST...*")                           
                            # Dùng chính câu hỏi của sinh viên làm từ khóa tìm kiếm trên mạng
                            mats = study_svc.get_recommendations(prompt)
                            
                            if mats:
                                ai_response = f"⚠️ Trong kho dữ liệu hiện tại của mình chưa có tài liệu nào giải thích về **'{prompt}'**.\n\n"
                                ai_response += "💡 **Tuy nhiên:** Mình lượm được mấy file này trên TailieuHUST. Bạn tải về rồi **Upload ngược lên đây** để mình đọc và giải đáp cho nha:\n\n"
                                for m in mats:
                                    ai_response += f"- 📄 [{m['title']}]({m['url']})\n"
                            else:
                                ai_response = f"⚠️ Mình đã tìm trong hệ thống và cả TailieuHUST nhưng không thấy thông tin về **'{prompt}'**. Bạn thử đổi từ khóa khác xem sao!"

                        # --- NHÁNH 3: VẼ SƠ ĐỒ ---
                        elif "ACTION_MINDMAP" in llm_response:
                            message_placeholder.markdown("🌳 *Đang cầm cọ vẽ sơ đồ tư duy, đợi xíu nha...*")
                            mindmap_result = generate_mindmap_payload(study_svc, prompt, context, chunks, output_file="src/tmp/data.js")
                            ai_response = mindmap_result.get("message", "⚠️ Không thể tạo sơ đồ tư duy.")
                            if mindmap_result.get("ok"):
                                assistant_entities = {
                                    "type": "mindmap",
                                    "nodes": mindmap_result.get("nodes", []),
                                }
                        
                        # --- NHÁNH 4: TẠO FLASHCARD ---
                        elif "ACTION_FLASHCARD" in llm_response:
                            message_placeholder.markdown("🗂️ *Đang soạn thẻ ghi nhớ cho bạn đây...*")
                            ai_response = generate_flashcards_markdown(study_svc, prompt)

                        # --- NHÁNH 5: TRẢ LỜI BÌNH THƯỜNG ---
                        else:
                            ai_response = llm_response

                    except Exception as e:
                        ai_response = f"Lỗi khi gọi AI: {e}"
                
                # Render nội dung ra màn hình
                message_placeholder.markdown(ai_response)
                assistant_payload = {"role": "assistant", "content": ai_response}
                if assistant_entities:
                    assistant_payload["entities"] = assistant_entities
                st.session_state.chat_ontap.append(assistant_payload)

elif st.session_state.page == "chat_bot_guidance":
    st.header("Yêu cầu hỗ trợ")
    st.caption("Bot trả lời trước về cách sử dụng chức năng. Nếu chưa rõ, bấm Hỏi admin dưới câu trả lời.")

    user_code = _safe_str(st.session_state.get("user_code"))
    user_id = _safe_str(st.session_state.get("user_id"))
    if not user_code or not user_id:
        st.error("⚠️ Thiếu thông tin phiên đăng nhập (userCode/userId). Vui lòng đăng nhập lại.")
        if st.button("↩️ Quay về trang đăng nhập", use_container_width=True, key="bot_guidance_back_to_login"):
            navigate_to("home", None)
            st.rerun()
        st.stop()

    active_escalation_id = _safe_str(st.session_state.get("bot_escalation_session_id"))
    bot_locked_after_handoff = bool(active_escalation_id)

    st.markdown("#### Phiên hỏi Admin")
    if user_id:
        try:
            bot_sessions_result = help_request_service.get_bot_escalation_sessions_by_user(
                user_id,
                include_closed=True,
                limit=100,
            )
            bot_sessions = bot_sessions_result.get("sessions", [])
        except Exception as e:
            st.error(f"❌ Không thể tải phiên hỏi admin từ botchat: {str(e)}")
            bot_sessions = []

        if bot_sessions:
            rows = []
            for s in bot_sessions:
                rows.append(
                    {
                        "Session ID": s.get("sessionId"),
                        "Trạng thái": s.get("status"),
                        "Tin nhắn gần nhất": s.get("lastMessage"),
                        "Bắt đầu": s.get("startedAt"),
                        "Kết thúc": s.get("endedAt"),
                    }
                )
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=400)

            selectable = {
                f"{s.get('sessionId')} | {s.get('status')} | {s.get('startedAt')}": s.get("sessionId")
                for s in bot_sessions
            }
            selected_label = st.selectbox(
                "Chọn phiên Hỏi admin",
                options=list(selectable.keys()),
                key="bot_escalation_session_selector",
            )
            selected_session = selectable.get(selected_label)
            is_opened = selected_session and selected_session == st.session_state.get("bot_escalation_session_id")

            c1, c2, c3 = st.columns(3)
            with c1:
                if is_opened:
                    if st.button("📁 Đóng phiên đã chọn", use_container_width=True, key="bot_escalation_close_selected"):
                        st.session_state.bot_escalation_session_id = None
                        st.rerun()
                else:
                    if st.button("📂 Mở phiên đã chọn", use_container_width=True, key="bot_escalation_open_selected"):
                        st.session_state.bot_escalation_session_id = selected_session
                        st.rerun()
            with c2:
                if st.button("➕ Tạo phiên mới", use_container_width=True, key="bot_escalation_create_new_btn"):
                    st.session_state.bot_escalation_session_id = None
                    st.session_state.bot_escalate_target_idx = None
                    st.rerun()
        else:
            st.info("Chưa có phiên chuyển tiếp nào từ botchat.")

    st.markdown("---")
    st.markdown("#### 💬 Đối thoại giữa bạn và bot")

    if not bot_locked_after_handoff:
        for idx, message in enumerate(st.session_state.chat_bot_guidance):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            if message.get("role") == "assistant":
                ask_key = f"bot_ask_admin_{idx}"
                if st.button("🔗 Hỏi admin", key=ask_key):
                    st.session_state.bot_escalate_target_idx = idx
                    st.rerun()

        if prompt := st.chat_input("Hỏi bot về cách dùng chức năng sinh viên..."):
            st.session_state.chat_bot_guidance.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Bot đang phân tích câu hỏi..."):
                    result = help_request_service.get_guidance_response(
                        user_code,
                        prompt,
                    )
                    answer = result.get("answer", "")
                st.markdown(answer)
                if result.get("usedFallback"):
                    reason = _safe_str(result.get("error"))
                    if reason:
                        st.warning(f"Bot đang dùng phản hồi dự phòng. Lý do: {reason}")
                    else:
                        st.warning("Bot đang dùng phản hồi dự phòng do lỗi kết nối AI.")
            st.session_state.chat_bot_guidance.append({"role": "assistant", "content": answer})
            st.rerun()

        target_idx = st.session_state.get("bot_escalate_target_idx")
        if target_idx is not None:
            st.markdown("---")
            st.markdown("#### 📨 Gửi Hỏi admin")
            with st.form("bot_escalation_form", clear_on_submit=True):
                default_msg = "Em chưa hiểu phần bot vừa giải thích, nhờ admin hướng dẫn thêm."
                admin_message = st.text_area(
                    "Tin nhắn gửi admin",
                    value=default_msg,
                    height=120,
                    key="bot_escalation_message",
                )
                sent = st.form_submit_button("Gửi cho admin", use_container_width=True)
                if sent:
                    if not user_id:
                        st.error("⚠️ Không tìm thấy userId trong phiên đăng nhập.")
                    elif not _safe_str(admin_message):
                        st.error("⚠️ Vui lòng nhập nội dung gửi admin.")
                    else:
                        try:
                            transcript = _format_bot_transcript(st.session_state.chat_bot_guidance, max_turns=12)
                            result = help_request_service.create_bot_escalation_session(
                                user_id,
                                admin_message,
                                transcript,
                            )
                            st.session_state.bot_escalation_session_id = result.get("sessionId")
                            st.session_state.bot_escalate_target_idx = None
                            st.success("✅ Đã bàn giao cho admin. Từ bây giờ bạn trao đổi trực tiếp với admin ở khung chat bên dưới.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Không thể chuyển tiếp cho admin: {str(e)}")
    else:
        st.info("Phiên đã bàn giao cho admin. Khung hỏi bot đã tạm ẩn, bạn trao đổi trực tiếp với admin bên dưới.")

    bot_session_id = st.session_state.get("bot_escalation_session_id")
    if bot_session_id:
        try:
            detail = help_request_service.get_bot_escalation_session_detail(bot_session_id)
            session_info = detail.get("session", {})
            messages = detail.get("messages", [])
            st.caption(
                f"Session: {session_info.get('sessionId', '')} | Sinh viên: {session_info.get('userId', '')} | Trạng thái: {session_info.get('status', '')}"
            )

            for msg in messages:
                sender = msg.get("sender", "unknown")
                content = msg.get("content", "")
                ts = msg.get("timestamp", "")
                if sender == "student":
                    with st.chat_message("user"):
                        st.markdown(content)
                        if ts:
                            st.caption(f"🕒 {ts}")
                elif sender == "admin":
                    with st.chat_message("assistant"):
                        st.markdown(f"**Admin:** {content}")
                        if ts:
                            st.caption(f"🕒 {ts}")

            st.divider()
            if session_info.get("status") != "closed":
                col_msg, col_end = st.columns([5, 1])
                with col_msg:
                    msg_to_admin = st.chat_input("Nhắn thêm cho admin trong phiên này...", key="bot_escalation_student_followup")
                    if msg_to_admin:
                        try:
                            help_request_service.send_bot_escalation_message(
                                bot_session_id,
                                user_id,
                                msg_to_admin,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Không thể gửi tin nhắn cho admin: {str(e)}")
                with col_end:
                    student_close_clicked = st.button("❌ Kết thúc", key="bot_escalation_student_close_btn", use_container_width=True)
                    if student_close_clicked:
                        try:
                            help_request_service.end_help_session(bot_session_id, user_id)
                            st.session_state.bot_escalation_session_id = None
                            st.success("✅ Đã kết thúc phiên hỗ trợ.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Không thể kết thúc phiên hỗ trợ: {str(e)}")
            else:
                st.info("Phiên này đã đóng. Bạn có thể tạo yêu cầu mới nếu cần.")
        except Exception as e:
            st.error(f"❌ Không thể tải chi tiết phiên hỏi admin từ botchat: {str(e)}")


# ----------------------------------------
# TRANG ADMIN: QUẢN LÝ DỮ LIỆU
# ----------------------------------------
elif st.session_state.page == "admin_home":
    st.header("Quản trị Hệ thống GC-Proctor")

    admin_view = _safe_str(st.session_state.get("admin_dashboard_view")).lower()
    if admin_view not in {"home", "regulation", "exam", "support"}:
        admin_view = "home"

    if admin_view == "home":
        st.caption("Chọn chức năng quản lý ở menu bên trái hoặc dùng các nút tắt bên dưới.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("📚 Upload Quy chế")
            if st.button("Mở Upload Quy chế", use_container_width=True, key="admin_home_go_regulation"):
                st.session_state.admin_dashboard_view = "regulation"
                st.rerun()
        with c2:
            st.info("📅 Quản lý Lịch thi")
            if st.button("Mở Quản lý Lịch thi", use_container_width=True, key="admin_home_go_exam"):
                st.session_state.admin_dashboard_view = "exam"
                st.rerun()
        with c3:
            open_help_count = _get_open_help_request_count()
            st.info(f"🆘 Hỗ trợ User ({open_help_count} mở)")
            if st.button("Mở Hỗ trợ User", use_container_width=True, key="admin_home_go_support"):
                st.session_state.admin_dashboard_view = "support"
                st.rerun()

    elif admin_view == "regulation":
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


    elif admin_view == "exam":
        st.subheader("📅 Quản lý Lịch thi")
        st.info("Mục này đang sẵn sàng để mở rộng dashboard lịch thi theo nhu cầu quản trị.")

    # ==== HỖ TRỢ USER: CHUYỂN TIẾP TỪ BOTCHAT ====
    elif admin_view == "support":
        st.subheader("Danh sách yêu cầu hỗ trợ")

        col1, col2 = st.columns([1, 1])
        with col1:
            show_closed_bot = st.checkbox("Hiển thị cả phiên đã đóng", value=True, key="admin_bot_show_closed")

        try:
            sessions_result = help_request_service.get_bot_escalation_sessions(include_closed=show_closed_bot)
            bot_sessions = sessions_result.get("sessions", [])
        except Exception as e:
            st.error(f"❌ Không thể tải danh sách phiên botchat: {str(e)}")
            bot_sessions = []

        if not bot_sessions:
            st.info("📭 Chưa có phiên chuyển tiếp từ botchat.")
        else:
            rows = []
            for s in bot_sessions:
                rows.append(
                    {
                        "Session ID": s.get("sessionId"),
                        "Sinh viên": s.get("userId"),
                        "Trạng thái": s.get("status"),
                        "Tin nhắn gần nhất": s.get("lastMessage"),
                        "Bắt đầu": s.get("startedAt"),
                        "Kết thúc": s.get("endedAt"),
                    }
                )
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=400)

            selectable = {
                f"{s.get('sessionId')} | SV:{s.get('userId')} | {s.get('status')}": s.get("sessionId")
                for s in bot_sessions
            }
            selected_key = st.selectbox("Chọn phiên botchat để xử lý", options=list(selectable.keys()), key="admin_bot_session_select")
            selected_session_id = selectable.get(selected_key)
            is_opened = selected_session_id and selected_session_id == st.session_state.get("admin_bot_session_id")

            col_action1, col_action2 = st.columns(2)
            with col_action1:
                if is_opened:
                    if st.button("📁 Đóng phiên đã chọn", use_container_width=True, key="admin_bot_close_selected"):
                        st.session_state.admin_bot_session_id = None
                        st.rerun()
                else:
                    if st.button("📂 Mở phiên đã chọn", use_container_width=True, key="admin_bot_open_selected"):
                        st.session_state.admin_bot_session_id = selected_session_id
                        st.rerun()
            with col_action2:
                if st.button("🔄 Làm mới danh sách", use_container_width=True, key="admin_bot_refresh_sessions"):
                    st.rerun()

        admin_bot_session_id = st.session_state.get("admin_bot_session_id")
        if admin_bot_session_id:
            try:
                detail = help_request_service.get_bot_escalation_session_detail(admin_bot_session_id)
                session_info = detail.get("session", {})
                messages = detail.get("messages", [])

                st.markdown(
                    f"**Chi tiết phiên:** {session_info.get('sessionId', '')} | SV: {session_info.get('userId', '')} | Trạng thái: {session_info.get('status', '')}"
                )

                for msg in messages:
                    sender = msg.get("sender", "unknown")
                    content = msg.get("content", "")
                    ts = msg.get("timestamp", "")
                    if sender == "student":
                        with st.chat_message("user"):
                            st.markdown(content)
                            if ts:
                                st.caption(f"🕒 {ts}")
                    elif sender == "admin":
                        with st.chat_message("assistant"):
                            st.markdown(f"**Admin:** {content}")
                            if ts:
                                st.caption(f"🕒 {ts}")

                st.divider()
                if session_info.get("status") != "closed":
                    with st.form("admin_bot_reply_form", clear_on_submit=True):
                        input_col, action_col = st.columns([5, 1])
                        with input_col:
                            admin_reply = st.text_input(
                                "Nhập phản hồi cho sinh viên...",
                                key="admin_bot_reply_input",
                                placeholder="Nhập phản hồi...",
                                label_visibility="collapsed",
                            )
                        with action_col:
                            send_clicked = st.form_submit_button("Gửi", use_container_width=True)

                    close_col = st.columns([1, 5])[0]
                    with close_col:
                        admin_close_clicked = st.button("❌ Kết thúc", key="admin_bot_close_inline_btn", use_container_width=True)

                    if send_clicked:
                        if not _safe_str(admin_reply):
                            st.warning("⚠️ Vui lòng nhập nội dung phản hồi.")
                        else:
                            try:
                                help_request_service.add_admin_response_to_bot_escalation(admin_bot_session_id, "admin", admin_reply)
                                st.success("✅ Đã gửi phản hồi cho sinh viên.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Không thể gửi phản hồi admin: {str(e)}")

                    if admin_close_clicked:
                        try:
                            help_request_service.close_bot_escalation_by_admin(admin_bot_session_id, "admin")
                            st.success("✅ Đã đóng phiên botchat.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Không thể đóng phiên botchat: {str(e)}")

            except Exception as e:
                st.error(f"❌ Không thể tải chi tiết phiên botchat: {str(e)}")