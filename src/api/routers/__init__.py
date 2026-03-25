from fastapi import APIRouter

from api.routers.audit_log_router import router as audit_log_router
from api.routers.auth_router import router as auth_router
from api.routers.chat_router import router as chat_router
from api.routers.chat_message_router import router as chat_message_router
from api.routers.chat_session_router import router as chat_session_router
from api.routers.course_router import router as course_router
from api.routers.document_chunk_router import router as document_chunk_router
from api.routers.document_router import router as document_router
from api.routers.exam_router import router as exam_router
from api.routers.exam_schedule_router import router as exam_schedule_router
from api.routers.feedback_router import router as feedback_router
from api.routers.kb_router import router as kb_router
from api.routers.me_router import router as me_router
from api.routers.metrics_router import router as metrics_router
from api.routers.nlp_router import router as nlp_router
from api.routers.regulation_advanced_router import router as regulation_advanced_router
from api.routers.regulation_router import router as regulation_router
from api.routers.retrieval_log_router import router as retrieval_log_router
from api.routers.safety_router import router as safety_router
from api.routers.study_router import router as study_router
from api.routers.user_router import router as user_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(nlp_router)
api_router.include_router(regulation_advanced_router)
api_router.include_router(me_router)
api_router.include_router(study_router)
api_router.include_router(kb_router)
api_router.include_router(safety_router)
api_router.include_router(metrics_router)
api_router.include_router(audit_log_router)
api_router.include_router(chat_message_router)
api_router.include_router(chat_session_router)
api_router.include_router(course_router)
api_router.include_router(document_chunk_router)
api_router.include_router(document_router)
api_router.include_router(exam_router)
api_router.include_router(exam_schedule_router)
api_router.include_router(feedback_router)
api_router.include_router(regulation_router)
api_router.include_router(retrieval_log_router)
api_router.include_router(user_router)


__all__ = ["api_router"]