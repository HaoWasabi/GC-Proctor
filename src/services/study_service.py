from fastapi import HTTPException


class StudyService:
    def query(self, payload: dict) -> dict:
        question = payload.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: question")
        return {
            "answer": "Noi dung on tap da duoc tong hop tu tai lieu mon hoc.",
            "citations": payload.get("citations", []),
        }

    def summarize(self, payload: dict) -> dict:
        source = payload.get("source")
        if not source:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: source")
        return {
            "summary": "Day la ban tom tat ngan gon tu nguon tai lieu da cung cap.",
            "length": payload.get("length", "short"),
        }

    def generate_flashcards(self, payload: dict) -> dict:
        topic = payload.get("topic")
        if not topic:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: topic")
        return {
            "topic": topic,
            "flashcards": [
                {"front": "Cau hoi 1", "back": "Tra loi 1"},
                {"front": "Cau hoi 2", "back": "Tra loi 2"},
            ],
        }

    def explain(self, payload: dict) -> dict:
        concept = payload.get("concept")
        if not concept:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: concept")
        return {
            "concept": concept,
            "level": payload.get("level", "basic"),
            "explanation": "Day la giai thich theo muc do duoc yeu cau.",
        }
