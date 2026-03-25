from datetime import datetime
from datetime import timezone

from fastapi import APIRouter

from api.controllers.metrics_controller import MetricsController


router = APIRouter(prefix="/metrics", tags=["Metrics"])
controller = MetricsController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.get("/fallback-rate")
def fallback_rate():
    return _ok(controller.fallback_rate(), "req_metrics_fallback_rate")


@router.get("/retrieval-quality")
def retrieval_quality():
    return _ok(controller.retrieval_quality(), "req_metrics_retrieval_quality")


@router.get("/intent-distribution")
def intent_distribution():
    return _ok(controller.intent_distribution(), "req_metrics_intent_distribution")


@router.get("/latency")
def latency():
    return _ok(controller.latency(), "req_metrics_latency")
