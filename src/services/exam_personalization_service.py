from datetime import date
from datetime import datetime

from fastapi import HTTPException


class ExamPersonalizationService:
    def _sample_item(self) -> dict:
        return {
            "id": "sch_123",
            "examId": "ex_001",
            "studentId": "stu_001",
            "examDate": "2026-03-26",
            "startTime": "2026-03-26T09:00:00Z",
            "room": "A2.302",
            "status": "scheduled",
            "updatedAt": "2026-03-24T04:00:00Z",
            "isActive": True,
            "course": {
                "courseCode": "SE101",
                "courseName": "Nhap mon Ky thuat phan mem",
            },
        }

    def upcoming(self, days: int = 14, status: str | None = None) -> dict:
        if days <= 0 or days > 60:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: days")
        item = self._sample_item()
        if status:
            item["status"] = status
        return {"items": [item], "total": 1}

    def today(self) -> dict:
        item = self._sample_item()
        item["examDate"] = date.today().isoformat()
        return {"items": [item], "total": 1}

    def search(self, from_date: str, to_date: str, course_code: str | None, status: str | None) -> dict:
        try:
            start_dt = datetime.fromisoformat(from_date)
            end_dt = datetime.fromisoformat(to_date)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: fromDate/toDate") from exc

        if start_dt > end_dt:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: fromDate > toDate")

        item = self._sample_item()
        if course_code:
            item["course"]["courseCode"] = course_code
        if status:
            item["status"] = status

        return {"items": [item], "total": 1}

    def next_exam(self) -> dict:
        return {"nextExam": self._sample_item()}
