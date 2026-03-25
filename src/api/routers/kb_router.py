from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body

from api.controllers.kb_controller import KBController


router = APIRouter(prefix="/kb", tags=["KnowledgeBase"])
controller = KBController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/documents/upload")
def upload_document(payload: dict = Body(...)):
    return _ok(controller.upload_document(payload), "req_kb_upload_document")


@router.post("/documents/{document_id}/ingest")
def ingest_document(document_id: str):
    return _ok(controller.ingest_document(document_id), "req_kb_ingest_document")


@router.post("/documents/{document_id}/rechunk")
def rechunk_document(document_id: str, payload: dict = Body(...)):
    return _ok(controller.rechunk_document(document_id, payload), "req_kb_rechunk_document")


@router.post("/reindex")
def reindex(payload: dict = Body(default={})): 
    return _ok(controller.reindex(payload), "req_kb_reindex")


@router.get("/ingestion-jobs/{job_id}")
def get_ingestion_job(job_id: str):
    return _ok(controller.get_ingestion_job(job_id), "req_kb_ingestion_job")
