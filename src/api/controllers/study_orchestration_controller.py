from services.study_service import StudyService
from services.user_service import UserService
from services.exam_schedule_service import ExamScheduleService
from pydantic import BaseModel
from typing import Optional


class StudyAskRequest(BaseModel):
    """Request model for study questions"""
    question: str
    user_id: Optional[str] = "default_user"
    context: Optional[dict] = {}


class StudyOrchestrationController:
    """Routes study questions to study service with user context"""

    def __init__(self):
        self.study_service = StudyService()
        self.user_service = UserService()
        self.exam_schedule_service = ExamScheduleService()

    def ask(self, payload: dict) -> dict:
        """
        Handle study questions with user context
        - Get user info and exam schedule
        - Pass to study service for RAG processing
        """
        question = payload.get("question", "")
        user_id = payload.get("user_id", "default_user")

        if not question:
            return {
                "success": False,
                "error": "Question is required"
            }

        # Get user context
        try:
            user_info = self.user_service.get_user(user_id)
            upcoming_exams = self.exam_schedule_service.get_upcoming_exams(user_id)
        except Exception as e:
            user_info = {}
            upcoming_exams = []

        # Process with study service
        result = self.study_service.process_study_workflow(
            question=question,
            user_info=user_info,
            upcoming_exams=upcoming_exams
        )

        return {
            "success": True,
            "data": result
        }

    def generate_flashcards(self, payload: dict) -> dict:
        """Generate flashcards for a topic"""
        course_code = payload.get("course_code", "")
        topic = payload.get("topic", "")
        num_cards = payload.get("num_cards", 10)

        if not course_code or not topic:
            return {
                "success": False,
                "error": "course_code and topic are required"
            }

        result = self.study_service.generate_flashcards(
            course_code=course_code,
            topic=topic,
            num_cards=num_cards
        )

        return {
            "success": True,
            "data": result
        }

    def summarize_material(self, payload: dict) -> dict:
        """Generate course/material summary"""
        course_code = payload.get("course_code", "")
        length = payload.get("length", "short")

        if not course_code:
            return {
                "success": False,
                "error": "course_code is required"
            }

        result = self.study_service.summarize_material(
            course_code=course_code,
            length=length
        )

        return {
            "success": True,
            "data": result
        }