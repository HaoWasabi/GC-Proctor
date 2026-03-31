"""
Help Request Service - Xử lý yêu cầu trợ giúp (hướng dẫn sử dụng hệ thống)
Cho phép học sinh hỏi về cách hệ thống hoạt động và chatbot sẽ khởi tạo cuộc hội thoại
"""

import json
from datetime import datetime, timezone
from uuid import uuid4
from services.nlp_service import NLPService
from services.chat_session_service import ChatSessionService
from services.chat_message_service import ChatMessageService
from models.chat_session_model import ChatSessionModel
from models.chat_message_model import ChatMessageModel
from fastapi import HTTPException


class HelpRequestService:
    """Xử lý yêu cầu trợ giúp và khởi tạo cuộc hội thoại hỗ trợ"""

    def __init__(self):
        self.nlp_service = NLPService()
        self.chat_session_service = ChatSessionService()
        self.chat_message_service = ChatMessageService()

    def create_help_session(self, user_id: str, help_topic: str) -> dict:
        """
        Tạo session hỗ trợ mới và response ban đầu từ chatbot
        
        Args:
            user_id: ID của học sinh
            help_topic: Chủ đề cần hỏi (ví dụ: "Cách dùng hệ thống", "Làm thế nào để nộp bài thi", v.v)
        
        Returns:
            dict: Chứa session_id, lời chào từ chatbot, và các gợi ý tiếp theo
        """
        try:
            # Tạo session chat mới cho help request
            session_id = str(uuid4())
            now = datetime.now(timezone.utc)
            
            help_session = ChatSessionModel(
                id=session_id,
                userId=user_id,
                channel="help_request",  # Phân biệt loại session
                persona="help_assistant",  # Chatbot trợ giúp
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
            
            # 2. Xác định loại hỗ trợ cần thiết
            support_type = self._classify_help_topic(help_topic)
            
            # 3. Tạo response từ chatbot
            bot_response = self._generate_initial_response(help_topic, support_type, user_id)
            
            # 4. Lưu response của chatbot
            bot_message_id = str(uuid4())
            bot_message = ChatMessageModel(
                id=bot_message_id,
                sessionId=session_id,
                senderType="bot",
                intent="help_response",
                content=bot_response["content"],
                citations=bot_response.get("citations", {}),
                entities={},
                createdAt=now,
                isActive=True
            )
            self.chat_message_service.create_chat_message(bot_message)
            
            # Trả về session info và response ban đầu
            return {
                "sessionId": session_id,
                "channel": "help_request",
                "botResponse": {
                    "messageId": bot_message_id,
                    "content": bot_response["content"],
                    "citations": bot_response.get("citations", {}),
                    "suggestedQuestions": bot_response.get("suggestedQuestions", [])
                },
                "timestamp": now.isoformat()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi tạo phiên hỗ trợ: {str(e)}")

    def send_help_message(self, session_id: str, user_id: str, message: str) -> dict:
        """
        Gửi tin nhắn trong phiên hỗ trợ và nhận phản hồi từ chatbot
        
        Args:
            session_id: ID của session
            user_id: ID của học sinh
            message: Nội dung tin nhắn
        
        Returns:
            dict: Chứa response từ chatbot
        """
        try:
            # Xác minh session tồn tại
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_userId() != user_id:
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
            
            # 2. Phân tích nội dung tin nhắn
            message_analysis = self._analyze_help_message(message)
            
            # 3. Tạo phản hồi từ chatbot
            bot_response = self._generate_contextual_response(
                message,
                message_analysis,
                session_id
            )
            
            # 4. Lưu phản hồi của chatbot
            bot_msg_id = str(uuid4())
            bot_message = ChatMessageModel(
                id=bot_msg_id,
                sessionId=session_id,
                senderType="bot",
                intent="help_response",
                content=bot_response["content"],
                citations=bot_response.get("citations", {}),
                entities={},
                createdAt=now,
                isActive=True
            )
            self.chat_message_service.create_chat_message(bot_message)
            
            return {
                "sessionId": session_id,
                "messageId": bot_msg_id,
                "botResponse": {
                    "content": bot_response["content"],
                    "citations": bot_response.get("citations", {}),
                    "suggestedQuestions": bot_response.get("suggestedQuestions", [])
                },
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
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_userId() != user_id:
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

    # ===== HELPER METHODS =====

    def _classify_help_topic(self, topic: str) -> str:
        """Phân loại chủ đề hỗ trợ"""
        topic_lower = topic.lower()
        
        if any(kw in topic_lower for kw in ["thi", "exam", "tòng", "phòng"]):
            return "exam_guidance"
        elif any(kw in topic_lower for kw in ["tài liệu", "document", "upload"]):
            return "document_help"
        elif any(kw in topic_lower for kw in ["chat", "trò chuyện", "message"]):
            return "chat_help"
        elif any(kw in topic_lower for kw in ["quy chế", "rule", "regulation"]):
            return "regulation_help"
        else:
            return "general_help"

    def _generate_initial_response(self, help_topic: str, support_type: str, user_id: str) -> dict:
        """Tạo phản hồi ban đầu từ chatbot"""
        
        # Prompt để Gemini tạo lời chào phù hợp
        prompt = f"""
Bạn là một trợ lý thông minh giúp học sinh hiểu về hệ thống GC-Proctor.
Một học sinh vừa bắt đầu phiên hỗ trợ với câu hỏi: "{help_topic}"

Hãy:
1. Chào đón học sinh một cách thân thiện
2. Xác nhận hiểu rõ câu hỏi của họ
3. Cung cấp 1-2 câu trả lời ban đầu giúp ích
4. Đề xuất 2-3 câu hỏi tiếp theo mà học sinh có thể hỏi
5. Mã hóa kết quả thành JSON với các key: "greeting", "answer", "suggestedQuestions"

Trả về JSON đơn giản, không markdown.
"""
        
        try:
            response = self.nlp_service.generate_json(prompt)
            
            content = f"{response.get('greeting', '')}\n\n{response.get('answer', '')}"
            suggested_questions = response.get('suggestedQuestions', [])
            
            return {
                "content": content,
                "citations": {},
                "suggestedQuestions": suggested_questions
            }
        except:
            # Fallback nếu Gemini gặp lỗi
            return {
                "content": f"""Xin chào! 👋

Tôi hiểu bạn muốn hỏi: "{help_topic}"

Tôi là trợ lý hỗ trợ của hệ thống GC-Proctor. Tôi sẽ giúp bạn hiểu:
- Cách sử dụng hệ thống
- Quy định và hướng dẫn thi
- Cách thức làm việc các tính năng
- Các câu hỏi thường gặp

Vui lòng tiếp tục hỏi chi tiết hơn hoặc chọn một trong những gợi ý dưới đây:""",
                "citations": {},
                "suggestedQuestions": [
                    "Hệ thống hoạt động như thế nào?",
                    "Tôi cần làm gì để chuẩn bị thi?",
                    "Có những tính năng nào hữu ích?"
                ]
            }

    def _analyze_help_message(self, message: str) -> dict:
        """Phân tích tin nhắn từ học sinh - xác định nhu cầu cụ thể"""
        
        message_lower = message.lower()
        
        analysis = {
            "intent": "clarification",
            "category": "general",
            "keywords": []
        }
        
        # Xác định category
        if any(kw in message_lower for kw in ["thi", "exam", "tòng", "phòng"]):
            analysis["category"] = "exam"
            analysis["keywords"] = ["exam", "test", "schedule"]
        elif any(kw in message_lower for kw in ["tài liệu", "document", "upload", "tải"]):
            analysis["category"] = "documents"
            analysis["keywords"] = ["documents", "materials", "upload"]
        elif any(kw in message_lower for kw in ["ôn tập", "study", "learn", "học"]):
            analysis["category"] = "study"
            analysis["keywords"] = ["study", "materials", "learning"]
        elif any(kw in message_lower for kw in ["chat", "trò chuyện", "message", "tin nhắn"]):
            analysis["category"] = "communication"
            analysis["keywords"] = ["chat", "messages"]
        elif any(kw in message_lower for kw in ["quy chế", "rule", "regulation", "điều lệ"]):
            analysis["category"] = "regulations"
            analysis["keywords"] = ["rules", "regulations"]
        
        return analysis

    def _generate_contextual_response(self, message: str, analysis: dict, session_id: str) -> dict:
        """Tạo phản hồi có ngữ cảnh dựa trên tin nhắn của học sinh"""
        
        category = analysis.get("category", "general")
        
        # Tạo prompt phù hợp dựa trên category
        category_context = {
            "exam": """Học sinh đang hỏi về kỳ thi. Hãy cung cấp:
- Hướng dẫn chuẩn bị thi
- Quy định phòng thi
- Cách thức toàn bộ quy trình thi
- Các câu hỏi thường gặp về thi""",
            
            "documents": """Học sinh đang hỏi về tài liệu. Hãy cung cấp:
- Cách tải lên tài liệu
- Các tài liệu được hỗ trợ
- Cách tìm kiếm tài liệu
- Cách sử dụng thư viện tài liệu""",
            
            "study": """Học sinh đang hỏi về ôn tập. Hãy cung cấp:
- Các tài nguyên ôn tập có sẵn
- Cách sử dụng flashcard
- Cách yêu cầu hướng dẫn ôn tập
- Lời khuyên ôn tập hiệu quả""",
            
            "communication": """Học sinh đang hỏi về chat. Hãy cung cấp:
- Cách sử dụng tính năng chat
- Cách hỏi trợ giúp qua chat
- Các công việc có thể làm qua chat
- Mô tả các persona/vai trò của chatbot""",
            
            "regulations": """Học sinh đang hỏi về quy chế. Hãy cung cấp:
- Tóm tắt các quy chế chính
- Quy định về hành vi kỳ thi
- Quy định bị cấm
- Nơi xem toàn bộ quy chế""",
            
            "general": """Hãy trả lời câu hỏi của học sinh một cách chi tiết và thân thiện.
Nếu cần, gợi ý các tính năng khác của hệ thống."""
        }
        
        prompt = f"""
Bạn là trợ lý hỗ trợ của hệ thống GC-Proctor.
Học sinh hỏi: "{message}"

{category_context.get(category, category_context['general'])}

Hướng dẫn:
1. Trả lời trực tiếp và chi tiết
2. Nếu cần, cung cấp bước thực hiện cụ thể
3. Gợi ý 2-3 câu hỏi tiếp theo
4. Trả về JSON với keys: "answer", "suggestedQuestions", "additionalInfo"

Trả về JSON đơn giản, không markdown.
"""
        
        try:
            response = self.nlp_service.generate_json(prompt)
            
            content = response.get('answer', '')
            additional_info = response.get('additionalInfo', '')
            
            if additional_info:
                content += f"\n\n📌 Thông tin thêm: {additional_info}"
            
            return {
                "content": content,
                "citations": {},
                "suggestedQuestions": response.get('suggestedQuestions', [])
            }
        except:
            # Fallback response
            return {
                "content": f"""Cảm ơn câu hỏi của bạn!

Tôi đang xử lý yêu cầu của bạn: "{message}"

Tôi sẽ sớm cung cấp câu trả lời chi tiết. Trong khi đó, bạn có thể:
- Xem phần Hướng dẫn trên ứng dụng
- Hỏi các câu hỏi khác
- Quay lại khi cần thêm trợ giúp

Có gì tôi còn có thể giúp bạn không?""",
                "citations": {},
                "suggestedQuestions": [
                    "Có câu hỏi khác không?",
                    "Tôi muốn về trang chủ",
                    "Kết thúc phiên hỗ trợ"
                ]
            }

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
            session = self.chat_session_service.get_chat_session(session_id)
            if not session or session.get_userId() != user_id:
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
