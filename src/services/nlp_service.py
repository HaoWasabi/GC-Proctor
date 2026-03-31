import json
import os
import re
import google.generativeai as genai
from fastapi import HTTPException


class NLPService:
    def __init__(self):
        """Initialize Gemini API once for the service"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def parse_intent(self, question: str) -> dict:
        """Extract intent from user question - SIMPLIFIED"""
        question_lower = question.lower()

        # Help request keywords
        help_keywords = ["cách dùng", "hướng dẫn", "làm sao", "hỏi", "giúp", "trợ giúp", "hệ thống hoạt động", "có gì mới", "tính năng", "support"]
        
        study_keywords = ["ôn tập", "tài liệu", "đề thi", "flashcard", "giải thích", "tóm tắt", "học bài"]
        if "lịch thi" in question_lower or "phòng thi" in question_lower:
            intent = "exam_schedule"
        elif "quy chế" in question_lower or "điều lệ" in question_lower:
            intent = "regulation"
        elif any(kw in question_lower for kw in help_keywords):
            intent = "help_request"
        elif any(kw in question_lower for kw in study_keywords):
            intent = "study_support"
        else:
            intent = "unknown"

        return {"intent": intent}

    def generate_text(self, prompt: str) -> str:
        """Call Gemini API to generate text response"""
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                if parts:
                    return parts[0].text
            return "Không thể tạo phản hồi từ Gemini"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    def generate_json(self, prompt: str) -> dict:
        """Call Gemini API and parse JSON response"""
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text

            # Extract JSON from response if wrapped in markdown
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            return json.loads(response_text)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="LLM did not return valid JSON")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")