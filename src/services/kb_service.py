from fastapi import HTTPException


class KBService:
    def upload_document(self, payload: dict) -> dict:
        title = payload.get("title")
        storage_path = payload.get("storagePath")
        if not title or not storage_path:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: title/storagePath")

        return {
            "documentId": "doc_001",
            "status": "uploaded",
            "title": title,
            "storagePath": storage_path,
        }

    def ingest_document(self, document_id: str) -> dict:
        if not document_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: document_id")
        return {
            "jobId": "job_ingest_001",
            "documentId": document_id,
            "status": "queued",
            "stage": "ingest",
        }

    def rechunk_document(self, document_id: str, payload: dict) -> dict:
        if not document_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: document_id")
        return {
            "jobId": "job_rechunk_001",
            "documentId": document_id,
            "chunkSize": payload.get("chunkSize", 500),
            "status": "queued",
            "stage": "rechunk",
        }

    def reindex(self, payload: dict) -> dict:
        return {
            "jobId": "job_reindex_001",
            "status": "queued",
            "scope": payload.get("scope", "all"),
            "stage": "reindex",
        }

    def get_ingestion_job(self, job_id: str) -> dict:
        if not job_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: job_id")
        return {
            "jobId": job_id,
            "status": "running",
            "progress": 65,
            "currentStep": "embedding",
        }


