class NLPService:
    def parse_intent(self, payload: dict) -> dict:
        question = (payload.get("question") or "").lower()
        if not question:
            return {"intent": "unknown", "confidence": 0.0, "entities": {}}

        if "lich thi" in question or "phong" in question:
            intent = "exam_schedule"
        elif "quy che" in question or "dieu" in question:
            intent = "regulation"
        elif "tom tat" in question or "flashcard" in question or "giai thich" in question:
            intent = "study_support"
        else:
            intent = "unknown"

        return {
            "intent": intent,
            "confidence": 0.88 if intent != "unknown" else 0.4,
            "entities": payload.get("entities", {}),
        }

    def fallback_check(self, payload: dict) -> dict:
        confidence = float(payload.get("confidence", 0.0))
        has_sources = bool(payload.get("hasSources", False))

        trigger = confidence < 0.6 or not has_sources
        reason = "low_confidence_or_missing_sources" if trigger else None

        return {
            "triggerFallback": trigger,
            "reason": reason,
        }
