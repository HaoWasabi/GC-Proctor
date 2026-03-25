from fastapi import HTTPException

from services.nlp_service import NLPService
from services.safety_service import SafetyService


class ChatOrchestrationService:
    def __init__(self):
        self.nlp_service = NLPService()
        self.safety_service = SafetyService()

    def ask(self, payload: dict, authorization: str | None) -> dict:
        question = payload.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: question")

        intent_result = self.nlp_service.parse_intent({"question": question, "entities": payload.get("context", {})})
        intent_name = intent_result["intent"]

        # Enforce auth for personalized exam schedule queries.
        if intent_name == "exam_schedule" and not (authorization and authorization.startswith("Bearer ")):
            raise HTTPException(status_code=401, detail="UNAUTHENTICATED")

        safety = self.safety_service.check_query({"query": question, "context": {"intent": intent_name}})
        fallback_triggered = not safety["allowed"] or intent_name == "unknown"

        if fallback_triggered:
            fallback_payload = {
                "reason": safety.get("reason") or "unknown_intent",
                "originalQuestion": question,
                "intent": intent_name,
                "locale": payload.get("context", {}).get("locale", "vi-VN"),
            }
            fb = self.safety_service.fallback_response(fallback_payload)
            answer_text = fb["message"]
            citations = []
        else:
            answer_text = "Thong tin da duoc xu ly theo intent va nguon du lieu lien quan."
            citations = [
                {
                    "type": "system",
                    "source": "gc-proctor",
                    "ref": "internal",
                }
            ]

        return {
            "sessionId": payload.get("sessionId") or "ses_generated_001",
            "messageId": "msg_bot_001",
            "intent": {
                "name": intent_name,
                "confidence": intent_result["confidence"],
            },
            "answer": {
                "text": answer_text,
                "tone": payload.get("context", {}).get("persona", "friendly"),
                "requiresFollowUp": fallback_triggered,
            },
            "citations": citations,
            "entities": intent_result.get("entities", {}),
            "fallback": {
                "triggered": fallback_triggered,
                "reason": safety.get("reason") if fallback_triggered else None,
            },
        }

    def end_session(self, session_id: str) -> dict:
        if not session_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: session_id")

        return {
            "sessionId": session_id,
            "sessionStatus": "closed",
            "endedAt": "2026-03-25T10:40:00Z",
        }

    def get_context(self, session_id: str, limit: int, before_message_id: str | None) -> dict:
        if not session_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: session_id")

        return {
            "session": {
                "id": session_id,
                "userId": "usr_demo",
                "channel": "web",
                "persona": "friendly",
                "sessionStatus": "active",
                "startedAt": "2026-03-25T10:00:00Z",
                "endedAt": None,
                "isActive": True,
            },
            "messages": [
                {
                    "id": before_message_id or "msg_user_001",
                    "senderType": "user",
                    "intent": "unknown",
                    "content": "Cho minh hoi...",
                    "citations": [],
                    "entities": {},
                    "createdAt": "2026-03-25T10:01:00Z",
                    "isActive": True,
                }
            ][: max(1, min(limit, 100))],
        }
