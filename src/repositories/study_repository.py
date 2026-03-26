from typing import List, Dict
from datetime import datetime
from models.study_log_model import StudyLogModel
from models.study_log_model import FlashcardModel
import firebase_admin
from firebase_admin import firestore


class StudyRepository:
    def __init__(self):
        self.db = firestore.client()

    def log_study_query(self, user_id: str, question: str, answer: str, citations: List) -> Dict:
        """Store study query log"""
        doc = {
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "citations": citations,
            "created_at": datetime.utcnow(),
            "type": "query"
        }
        ref = self.db.collection("study_logs").add(doc)
        return doc

    def log_study_summary(self, user_id: str, source: str, summary: str, length: str) -> Dict:
        """Store summary generation log"""
        doc = {
            "user_id": user_id,
            "source": source,
            "summary": summary,
            "length": length,
            "created_at": datetime.utcnow(),
            "type": "summary"
        }
        self.db.collection("study_logs").add(doc)
        return doc

    def save_flashcards(self, user_id: str, topic: str, flashcards: List[Dict]) -> List[Dict]:
        """Save generated flashcards"""
        saved = []
        for card in flashcards:
            doc = {
                "user_id": user_id,
                "topic": topic,
                "front": card.get("front"),
                "back": card.get("back"),
                "difficulty": card.get("difficulty"),
                "created_at": datetime.utcnow(),
                "mastered": False,
                "attempts": 0
            }
            ref = self.db.collection("flashcards").add(doc)
            doc["id"] = ref[1].id
            saved.append(doc)
        return saved

    def log_concept_explanation(self, user_id: str, concept: str, level: str) -> Dict:
        """Log concept explanation requests"""
        doc = {
            "user_id": user_id,
            "concept": concept,
            "level": level,
            "created_at": datetime.utcnow(),
            "type": "explanation"
        }
        self.db.collection("study_logs").add(doc)
        return doc

    def get_user_study_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve user's study history"""
        docs = self.db.collection("study_logs") \
            .where("user_id", "==", user_id) \
            .order_by("created_at", direction=firestore.Query.DESCENDING) \
            .limit(limit) \
            .stream()
        return [doc.to_dict() for doc in docs]

    def get_user_flashcards(self, user_id: str, topic: str = None) -> List[Dict]:
        """Retrieve user's flashcards"""
        query = self.db.collection("flashcards").where("user_id", "==", user_id)
        if topic:
            query = query.where("topic", "==", topic)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]