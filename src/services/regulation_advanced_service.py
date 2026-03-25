from fastapi import HTTPException


class RegulationAdvancedService:
    def query(self, payload: dict) -> dict:
        query = payload.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: query")

        return {
            "answer": "Theo Dieu 12, Khoan 3, sinh vien khong duoc mang thiet bi thu phat vao phong thi.",
            "citations": [
                {
                    "regulationId": "reg_001",
                    "regulationCode": "QC-EXAM",
                    "version": "2026.1",
                    "article": "12",
                    "clause": "3",
                    "chunkId": "chk_001",
                    "quote": "Sinh vien khong duoc mang thiet bi thu phat vao phong thi.",
                    "sourceUrl": "https://example.edu/regulation.pdf",
                }
            ],
            "retrieval": {
                "topK": payload.get("topK", 5),
                "latencyMs": 120,
                "modelVersion": "rag-v1",
            },
        }

    def get_clauses(self, regulation_id: str) -> dict:
        if not regulation_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: regulation_id")

        return {
            "regulationId": regulation_id,
            "clauses": [
                {
                    "article": "12",
                    "clause": "3",
                    "title": "Vat dung cam",
                    "content": "Khong duoc mang thiet bi thu phat vao phong thi.",
                }
            ],
        }

    def validate_answer(self, payload: dict) -> dict:
        answer = payload.get("answer", "")
        citations = payload.get("citations", [])

        is_valid = bool(answer) and bool(citations)
        return {
            "isValid": is_valid,
            "violations": [] if is_valid else ["missing_citation"],
            "score": 1.0 if is_valid else 0.2,
        }
