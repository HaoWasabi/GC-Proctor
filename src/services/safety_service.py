class SafetyService:
    def check_query(self, payload: dict) -> dict:
        query = (payload.get("query") or "").lower()
        blocked_keywords = {"diem thi", "mat khau", "thong tin nhay cam"}

        matched = [word for word in blocked_keywords if word in query]
        if matched:
            return {
                "allowed": False,
                "riskLevel": "high",
                "categories": ["privacy", "out_of_scope"],
                "action": "fallback",
                "reason": "requests_personal_sensitive_data",
            }

        return {
            "allowed": True,
            "riskLevel": "low",
            "categories": [],
            "action": "allow",
            "reason": None,
        }

    def fallback_response(self, payload: dict) -> dict:
        return {
            "message": "Minh chua du co so de tra loi chinh xac cau hoi nay. Ban co the cung cap them thong tin hoac lien he phong giao vu.",
            "suggestions": [
                "Hoi lai theo dinh dang: lich thi + ngay + mon hoc",
                "Dang nhap de truy van thong tin ca nhan",
            ],
            "contact": {
                "unit": "Phong giao vu",
                "email": "giaovu@example.edu",
                "phone": "028-1234-5678",
            },
            "reason": payload.get("reason"),
        }

    def escalation_contacts(self) -> dict:
        return {
            "contacts": [
                {
                    "unit": "Phong giao vu",
                    "email": "giaovu@example.edu",
                    "phone": "028-1234-5678",
                    "hours": "08:00-17:00",
                }
            ]
        }
