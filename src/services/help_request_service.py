"""
Help Request Service - Kênh hỗ trợ trực tiếp giữa sinh viên và admin.
"""

from datetime import datetime, timezone
from uuid import uuid4
from services.chat_session_service import ChatSessionService
from services.chat_message_service import ChatMessageService
from services.nlp_service import NLPService
from services.user_service import UserService
from models.chat_session_model import ChatSessionModel
from models.chat_message_model import ChatMessageModel
from fastapi import HTTPException


class HelpRequestService:
    """Xử lý yêu cầu trợ giúp giữa sinh viên và admin"""

    BOT_ESCALATION_CHANNEL = "bot_escalation"

    GUIDANCE_PROMPT_TEMPLATE = """
Bạn là trợ lý vận hành hệ thống GC-Proctor cho sinh viên.

Mục tiêu:
- Hướng dẫn rõ ràng cách dùng các chức năng phía sinh viên.
- Trả lời theo từng bước thao tác thực tế trong ứng dụng.
- Nếu câu hỏi ngoài phạm vi hoặc thiếu dữ liệu, nói rõ giới hạn và đề xuất bấm "Hỏi admin".

Các chức năng sinh viên có trong hệ thống:
1) Dashboard Sinh viên
2) Hỏi đáp Quy chế
3) Lịch thi của tôi
4) Ôn tập kiến thức
5) Yêu cầu hỗ trợ
6) Trợ lý vận hành (bot)

Ràng buộc trả lời:
- Ngắn gọn, dễ hiểu, tiếng Việt.
- Không bịa thông tin kỹ thuật nội bộ hoặc dữ liệu không có.
- Luôn ưu tiên hướng dẫn theo bước: "Bước 1", "Bước 2", ...
- Nếu cần liên hệ người thật, kết thúc bằng: "Nếu bạn vẫn chưa rõ, hãy bấm Hỏi admin bên dưới câu trả lời này."

Ngữ cảnh sinh viên:
- Mã sinh viên: {student_id}

Câu hỏi sinh viên:
{question}
""".strip()

    def __init__(self):
        self.chat_session_service = ChatSessionService()
        self.chat_message_service = ChatMessageService()
        self.user_service = UserService()
        self._nlp_service = None

    def _normalize_user_ref(self, value: str) -> str:
        return str(value or "").strip()

    def _resolve_user_id(self, user_ref: str) -> str:
        clean_ref = self._normalize_user_ref(user_ref)
        if not clean_ref:
            return clean_ref

        try:
            user = self.user_service.get_user_by_userCode(clean_ref)
            if user and user.get_id():
                return str(user.get_id()).strip()
        except Exception:
            pass

        return clean_ref

    def _build_user_id_candidates(self, user_ref: str) -> list[str]:
        clean_ref = self._normalize_user_ref(user_ref)
        candidates = [clean_ref]
        resolved_id = self._resolve_user_id(clean_ref)
        if resolved_id not in candidates:
            candidates.append(resolved_id)
        return candidates

    def _require_user_id(self, user_ref: str) -> str:
        user_id = self._resolve_user_id(user_ref)
        if not user_id:
            raise HTTPException(status_code=400, detail="Thiếu thông tin user")
        return user_id

    def _get_nlp_service(self):
        if self._nlp_service is None:
            self._nlp_service = NLPService()
        return self._nlp_service

    def _fallback_guidance_answer(self, question: str) -> str:
        return (
            "Mình chưa thể tạo phản hồi AI lúc này.\n\n"
            "Bước 1: Vào đúng mục chức năng ở menu bên trái.\n"
            "Bước 2: Nhập đầy đủ thông tin bắt buộc (ví dụ: mã sinh viên).\n"
            "Bước 3: Bấm nút thao tác tương ứng và kiểm tra thông báo hệ thống.\n"
            "Bước 4: Nếu vẫn lỗi, chụp màn hình + mô tả câu hỏi: "
            f"\"{question}\" để gửi admin.\n\n"
            "Nếu bạn vẫn chưa rõ, hãy bấm Hỏi admin bên dưới câu trả lời này."
        )

    def get_guidance_response(self, student_id: str, question: str) -> dict:
        """Sinh phản hồi hướng dẫn vận hành cho sinh viên bằng prompt template chặt chẽ"""
        clean_student_id = str(student_id or "chưa cung cấp").strip()
        clean_question = str(question or "").strip()
        if not clean_question:
            raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")

        prompt = self.GUIDANCE_PROMPT_TEMPLATE.format(
            student_id=clean_student_id,
            question=clean_question,
        )

        try:
            answer = self._get_nlp_service().generate_text(prompt)
            return {
                "answer": answer,
                "usedFallback": False,
                "promptTemplate": self.GUIDANCE_PROMPT_TEMPLATE,
                "error": "",
            }
        except Exception as e:
            error_reason = str(e)
            if len(error_reason) > 240:
                error_reason = error_reason[:240] + "..."
            return {
                "answer": self._fallback_guidance_answer(clean_question),
                "usedFallback": True,
                "promptTemplate": self.GUIDANCE_PROMPT_TEMPLATE,
                "error": error_reason,
            }

    def create_bot_escalation_session(self, user_id: str, message: str, transcript: str) -> dict:
        """Tạo phiên chuyển tiếp từ bot sang admin, kèm trích dẫn lịch sử chat bot"""
        try:
            clean_user_id = self._require_user_id(user_id)
            session_id = str(uuid4())
            now = datetime.now(timezone.utc)

            help_session = ChatSessionModel(
                id=session_id,
                userId=clean_user_id,
                channel=self.BOT_ESCALATION_CHANNEL,
                persona="admin_support",
                sessionStatus="active",
                startedAt=now,
                endedAt=None,
                isActive=True,
            )

            session_created = self.chat_session_service.create_chat_session(help_session)
            if not session_created:
                raise HTTPException(status_code=500, detail="Không thể tạo phiên chuyển tiếp admin")

            student_message_id = str(uuid4())
            escalation_content = (
                "[Yêu cầu từ botchat]\n"
                f"Nội dung sinh viên: {message}\n\n"
                "[Trích dẫn lịch sử botchat]\n"
                f"{transcript}"
            )
            student_message = ChatMessageModel(
                id=student_message_id,
                sessionId=session_id,
                senderType="student",
                intent="bot_escalation_request",
                content=escalation_content,
                citations={},
                entities={"source": "botchat"},
                createdAt=now,
                isActive=True,
            )
            self.chat_message_service.create_chat_message(student_message)

            return {
                "sessionId": session_id,
                "channel": self.BOT_ESCALATION_CHANNEL,
                "messageId": student_message_id,
                "status": "active",
                "timestamp": now.isoformat(),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi tạo phiên chuyển tiếp admin: {str(e)}")

    def get_bot_escalation_sessions(self, include_closed: bool = True, limit: int = 200) -> dict:
        """Lấy danh sách phiên chuyển tiếp từ botchat để admin xử lý"""
        try:
            sessions = self.chat_session_service.get_sessions_by_channel(self.BOT_ESCALATION_CHANNEL)
            sessions = sorted(
                sessions,
                key=lambda s: s.get_startedAt() or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True,
            )

            if not include_closed:
                sessions = [s for s in sessions if s.get_sessionStatus() != "closed"]

            formatted = []
            for session in sessions[:limit]:
                session_messages = self.chat_message_service.get_messages_by_session(session.get_id(), limit=200)
                last_message = session_messages[-1] if session_messages else None
                formatted.append(
                    {
                        "sessionId": session.get_id(),
                        "userId": session.get_userId(),
                        "status": session.get_sessionStatus(),
                        "isActive": session.get_state(),
                        "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                        "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                        "lastMessage": last_message.get_content() if last_message else "",
                    }
                )

            return {"count": len(formatted), "sessions": formatted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách chuyển tiếp botchat: {str(e)}")

    def get_bot_escalation_sessions_by_user(self, user_id: str, include_closed: bool = True, limit: int = 50) -> dict:
        """Lấy danh sách phiên chuyển tiếp botchat theo sinh viên"""
        try:
            normalized_user_id = self._require_user_id(user_id)
            sessions = self.chat_session_service.get_sessions_by_channel(self.BOT_ESCALATION_CHANNEL)
            sessions = [s for s in sessions if str(s.get_userId()).strip() == normalized_user_id]
            sessions = sorted(
                sessions,
                key=lambda s: s.get_startedAt() or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True,
            )

            if not include_closed:
                sessions = [s for s in sessions if s.get_sessionStatus() != "closed"]

            formatted = []
            for session in sessions[:limit]:
                session_messages = self.chat_message_service.get_messages_by_session(session.get_id(), limit=100)
                last_message = session_messages[-1] if session_messages else None
                formatted.append(
                    {
                        "sessionId": session.get_id(),
                        "status": session.get_sessionStatus(),
                        "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                        "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                        "lastMessage": last_message.get_content() if last_message else "",
                    }
                )

            return {"count": len(formatted), "sessions": formatted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy phiên chuyển tiếp botchat theo sinh viên: {str(e)}")

    def get_bot_escalation_session_detail(self, session_id: str, limit: int = 200) -> dict:
        """Lấy chi tiết hội thoại của một phiên chuyển tiếp botchat"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != self.BOT_ESCALATION_CHANNEL:
                raise HTTPException(status_code=404, detail="Phiên chuyển tiếp botchat không tìm thấy")

            messages = self.chat_message_service.get_messages_by_session(session_id, limit)
            formatted_messages = []
            for msg in messages:
                formatted_messages.append(
                    {
                        "id": msg.get_id(),
                        "sender": msg.get_senderType(),
                        "intent": msg.get_intent(),
                        "content": msg.get_content(),
                        "timestamp": msg.get_createdAt().isoformat() if msg.get_createdAt() else None,
                    }
                )

            return {
                "session": {
                    "sessionId": session.get_id(),
                    "userId": session.get_userId(),
                    "status": session.get_sessionStatus(),
                    "isActive": session.get_state(),
                    "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                    "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                },
                "messages": formatted_messages,
                "messageCount": len(formatted_messages),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy chi tiết phiên chuyển tiếp botchat: {str(e)}")

    def send_bot_escalation_message(self, session_id: str, user_id: str, message: str) -> dict:
        """Sinh viên gửi thêm tin nhắn trong phiên chuyển tiếp botchat"""
        try:
            normalized_user_id = self._require_user_id(user_id)
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != self.BOT_ESCALATION_CHANNEL or str(session.get_userId()).strip() != normalized_user_id:
                raise HTTPException(status_code=404, detail="Phiên chuyển tiếp botchat không tìm thấy")

            now = datetime.now(timezone.utc)
            student_msg_id = str(uuid4())
            student_message = ChatMessageModel(
                id=student_msg_id,
                sessionId=session_id,
                senderType="student",
                intent="bot_escalation_follow_up",
                content=message,
                citations={},
                entities={"source": "botchat"},
                createdAt=now,
                isActive=True,
            )
            self.chat_message_service.create_chat_message(student_message)

            return {
                "sessionId": session_id,
                "messageId": student_msg_id,
                "sender": "student",
                "content": message,
                "timestamp": now.isoformat(),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi gửi tin nhắn chuyển tiếp botchat: {str(e)}")

    def add_admin_response_to_bot_escalation(self, session_id: str, admin_id: str, message: str) -> dict:
        """Admin phản hồi phiên chuyển tiếp botchat"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != self.BOT_ESCALATION_CHANNEL:
                raise HTTPException(status_code=404, detail="Phiên chuyển tiếp botchat không tìm thấy")

            now = datetime.now(timezone.utc)
            msg_id = str(uuid4())
            admin_message = ChatMessageModel(
                id=msg_id,
                sessionId=session_id,
                senderType="admin",
                intent="bot_escalation_admin_response",
                content=message,
                citations={},
                entities={"adminId": str(admin_id), "source": "botchat"},
                createdAt=now,
                isActive=True,
            )
            created = self.chat_message_service.create_chat_message(admin_message)
            if not created:
                raise HTTPException(status_code=500, detail="Không thể gửi phản hồi của admin")

            if session.get_sessionStatus() != "active":
                session.set_sessionStatus("active")
                session.set_state(True)
                session.set_endedAt(None)
                self.chat_session_service.update_chat_session(session)

            return {
                "sessionId": session_id,
                "messageId": msg_id,
                "sender": "admin",
                "content": message,
                "timestamp": now.isoformat(),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi phản hồi admin cho chuyển tiếp botchat: {str(e)}")

    def close_bot_escalation_by_admin(self, session_id: str, admin_id: str) -> dict:
        """Admin đóng phiên chuyển tiếp botchat"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != self.BOT_ESCALATION_CHANNEL:
                raise HTTPException(status_code=404, detail="Phiên chuyển tiếp botchat không tìm thấy")

            now = datetime.now(timezone.utc)
            session.set_sessionStatus("closed")
            session.set_endedAt(now)
            session.set_state(False)
            updated = self.chat_session_service.update_chat_session(session)
            if not updated:
                raise HTTPException(status_code=500, detail="Không thể đóng phiên chuyển tiếp botchat")

            return {
                "sessionId": session_id,
                "status": "closed",
                "closedBy": str(admin_id),
                "timestamp": now.isoformat(),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đóng phiên chuyển tiếp botchat: {str(e)}")

    def create_help_session(self, user_id: str, help_topic: str) -> dict:
        """
        Tạo session hỗ trợ mới với tin nhắn đầu tiên của sinh viên
        
        Args:
            user_id: ID của học sinh
            help_topic: Chủ đề cần hỏi (ví dụ: "Cách dùng hệ thống", "Làm thế nào để nộp bài thi", v.v)
        
        Returns:
            dict: Chứa thông tin session vừa tạo
        """
        try:
            clean_user_id = self._require_user_id(user_id)
            # Tạo session chat mới cho help request
            session_id = str(uuid4())
            now = datetime.now(timezone.utc)
            
            help_session = ChatSessionModel(
                id=session_id,
                userId=clean_user_id,
                channel="help_request",  # Phân biệt loại session
                persona="admin_support",
                sessionStatus="active",
                startedAt=now,
                endedAt=None,
                isActive=True
            )
            
            # Lưu session vào database
            session_created = self.chat_session_service.create_chat_session(help_session)
            if not session_created:
                raise HTTPException(status_code=500, detail="Không thể tạo phiên hỗ trợ")
            
            # 1. Lưu câu hỏi/chủ đề của học sinh
            student_message_id = str(uuid4())
            student_message = ChatMessageModel(
                id=student_message_id,
                sessionId=session_id,
                senderType="student",
                intent="help_request",
                content=help_topic,
                citations={},
                entities={},
                createdAt=now,
                isActive=True
            )
            self.chat_message_service.create_chat_message(student_message)

            return {
                "sessionId": session_id,
                "channel": "help_request",
                "messageId": student_message_id,
                "status": "active",
                "timestamp": now.isoformat()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi tạo phiên hỗ trợ: {str(e)}")

    def send_help_message(self, session_id: str, user_id: str, message: str) -> dict:
        """
        Gửi thêm tin nhắn của sinh viên trong phiên hỗ trợ
        
        Args:
            session_id: ID của session
            user_id: ID của học sinh
            message: Nội dung tin nhắn
        
        Returns:
            dict: Xác nhận tin nhắn đã được lưu
        """
        try:
            normalized_user_id = self._require_user_id(user_id)
            # Xác minh session tồn tại
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or str(session.get_userId()).strip() != normalized_user_id:
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")
            
            now = datetime.now(timezone.utc)
            
            # 1. Lưu tin nhắn của học sinh
            student_msg_id = str(uuid4())
            student_message = ChatMessageModel(
                id=student_msg_id,
                sessionId=session_id,
                senderType="student",
                intent="help_follow_up",
                content=message,
                citations={},
                entities={},
                createdAt=now,
                isActive=True
            )
            self.chat_message_service.create_chat_message(student_message)
            
            return {
                "sessionId": session_id,
                "messageId": student_msg_id,
                "sender": "student",
                "content": message,
                "timestamp": now.isoformat()
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi gửi tin nhắn hỗ trợ: {str(e)}")

    def end_help_session(self, session_id: str, user_id: str) -> dict:
        """
        Kết thúc phiên hỗ trợ
        
        Args:
            session_id: ID của session
            user_id: ID của học sinh
        
        Returns:
            dict: Xác nhận kết thúc session
        """
        try:
            normalized_user_id = self._require_user_id(user_id)
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or str(session.get_userId()).strip() != normalized_user_id:
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")
            
            # Cập nhật trạng thái session
            session.set_sessionStatus("closed")
            session.set_endedAt(datetime.now(timezone.utc))
            session.set_state(False)
            self.chat_session_service.update_chat_session(session)
            
            return {
                "sessionId": session_id,
                "status": "closed",
                "message": "Phiên hỗ trợ đã kết thúc. Cảm ơn bạn!"
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi kết thúc phiên hỗ trợ: {str(e)}")

    def get_session_history(self, session_id: str, user_id: str, limit: int = 50) -> dict:
        """
        Lấy lịch sử chat trong phiên hỗ trợ
        
        Args:
            session_id: ID của session
            user_id: ID của học sinh
            limit: Số tin nhắn tối đa để lấy
        
        Returns:
            dict: Chứa lịch sử tin nhắn
        """
        try:
            normalized_user_id = self._require_user_id(user_id)
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or str(session.get_userId()).strip() != normalized_user_id:
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")
            
            # Lấy lịch sử tin nhắn từ session này
            messages = self.chat_message_service.get_messages_by_session(session_id, limit)
            
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "id": msg.get_id(),
                    "sender": msg.get_senderType(),
                    "content": msg.get_content(),
                    "timestamp": msg.get_createdAt().isoformat() if msg.get_createdAt() else None
                })
            
            return {
                "sessionId": session_id,
                "messageCount": len(formatted_messages),
                "messages": formatted_messages
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy lịch sử chat: {str(e)}")

    def get_help_sessions(self, include_closed: bool = True, limit: int = 200) -> dict:
        """Lấy danh sách phiên hỗ trợ để admin theo dõi"""
        try:
            sessions = self.chat_session_service.get_sessions_by_channel("help_request")
            sessions = sorted(
                sessions,
                key=lambda s: s.get_startedAt() or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True,
            )

            if not include_closed:
                sessions = [s for s in sessions if s.get_sessionStatus() != "closed"]

            formatted = []
            for session in sessions[:limit]:
                session_messages = self.chat_message_service.get_messages_by_session(session.get_id(), limit=200)
                last_message = session_messages[-1] if session_messages else None
                last_student_messages = [m for m in session_messages if m.get_senderType() == "student"]
                last_student_message = last_student_messages[-1] if last_student_messages else None
                formatted.append(
                    {
                        "sessionId": session.get_id(),
                        "userId": session.get_userId(),
                        "status": session.get_sessionStatus(),
                        "isActive": session.get_state(),
                        "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                        "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                        "lastMessage": last_message.get_content() if last_message else "",
                        "lastMessageAt": last_message.get_createdAt().isoformat() if last_message and last_message.get_createdAt() else None,
                        "lastStudentMessage": last_student_message.get_content() if last_student_message else "",
                    }
                )

            return {"count": len(formatted), "sessions": formatted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách phiên hỗ trợ: {str(e)}")

    def get_help_sessions_by_user(self, user_id: str, include_closed: bool = True, limit: int = 50) -> dict:
        """Lấy danh sách phiên hỗ trợ theo user để sinh viên xem lại lịch sử"""
        try:
            normalized_user_id = self._require_user_id(user_id)
            sessions = self.chat_session_service.get_sessions_by_channel("help_request")
            sessions = [s for s in sessions if str(s.get_userId()).strip() == normalized_user_id]
            sessions = sorted(
                sessions,
                key=lambda s: s.get_startedAt() or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True,
            )

            if not include_closed:
                sessions = [s for s in sessions if s.get_sessionStatus() != "closed"]

            formatted = []
            for session in sessions[:limit]:
                session_messages = self.chat_message_service.get_messages_by_session(session.get_id(), limit=100)
                last_message = session_messages[-1] if session_messages else None
                formatted.append(
                    {
                        "sessionId": session.get_id(),
                        "status": session.get_sessionStatus(),
                        "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                        "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                        "lastMessage": last_message.get_content() if last_message else "",
                    }
                )

            return {"count": len(formatted), "sessions": formatted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách phiên theo sinh viên: {str(e)}")

    def get_help_session_detail(self, session_id: str, limit: int = 200) -> dict:
        """Lấy chi tiết hội thoại của một phiên hỗ trợ cho admin"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != "help_request":
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")

            messages = self.chat_message_service.get_messages_by_session(session_id, limit)
            formatted_messages = []
            for msg in messages:
                formatted_messages.append(
                    {
                        "id": msg.get_id(),
                        "sender": msg.get_senderType(),
                        "intent": msg.get_intent(),
                        "content": msg.get_content(),
                        "timestamp": msg.get_createdAt().isoformat() if msg.get_createdAt() else None,
                    }
                )

            return {
                "session": {
                    "sessionId": session.get_id(),
                    "userId": session.get_userId(),
                    "status": session.get_sessionStatus(),
                    "isActive": session.get_state(),
                    "startedAt": session.get_startedAt().isoformat() if session.get_startedAt() else None,
                    "endedAt": session.get_endedAt().isoformat() if session.get_endedAt() else None,
                },
                "messages": formatted_messages,
                "messageCount": len(formatted_messages),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lấy chi tiết phiên hỗ trợ: {str(e)}")

    def add_admin_response(self, session_id: str, admin_id: str, message: str) -> dict:
        """Thêm phản hồi từ admin vào phiên hỗ trợ"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != "help_request":
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")

            now = datetime.now(timezone.utc)
            msg_id = str(uuid4())
            admin_message = ChatMessageModel(
                id=msg_id,
                sessionId=session_id,
                senderType="admin",
                intent="help_admin_response",
                content=message,
                citations={},
                entities={"adminId": str(admin_id)},
                createdAt=now,
                isActive=True,
            )
            created = self.chat_message_service.create_chat_message(admin_message)
            if not created:
                raise HTTPException(status_code=500, detail="Không thể gửi phản hồi của admin")

            if session.get_sessionStatus() != "active":
                session.set_sessionStatus("active")
                session.set_state(True)
                session.set_endedAt(None)
                self.chat_session_service.update_chat_session(session)

            return {
                "sessionId": session_id,
                "messageId": msg_id,
                "sender": "admin",
                "content": message,
                "timestamp": now.isoformat(),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi phản hồi hỗ trợ từ admin: {str(e)}")

    def close_help_session_by_admin(self, session_id: str, admin_id: str) -> dict:
        """Đóng một phiên hỗ trợ bởi admin"""
        try:
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_channel() != "help_request":
                raise HTTPException(status_code=404, detail="Phiên hỗ trợ không tìm thấy")

            now = datetime.now(timezone.utc)
            session.set_sessionStatus("closed")
            session.set_endedAt(now)
            session.set_state(False)
            updated = self.chat_session_service.update_chat_session(session)
            if not updated:
                raise HTTPException(status_code=500, detail="Không thể đóng phiên hỗ trợ")

            return {
                "sessionId": session_id,
                "status": "closed",
                "closedBy": str(admin_id),
                "timestamp": now.isoformat(),
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đóng phiên hỗ trợ: {str(e)}")