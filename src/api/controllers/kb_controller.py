from services.kb_service import KBService


class KBController:
    def __init__(self):
        self.service = KBService()

    def upload_document(self, payload: dict) -> dict:
        return self.service.upload_document(payload)

    def ingest_document(self, document_id: str) -> dict:
        return self.service.ingest_document(document_id)

    def rechunk_document(self, document_id: str, payload: dict) -> dict:
        return self.service.rechunk_document(document_id, payload)

    def reindex(self, payload: dict) -> dict:
        return self.service.reindex(payload)

    def get_ingestion_job(self, job_id: str) -> dict:
        return self.service.get_ingestion_job(job_id)
