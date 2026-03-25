class MetricsService:
    def fallback_rate(self) -> dict:
        return {
            "value": 0.08,
            "window": "7d",
            "target": 0.1,
        }

    def retrieval_quality(self) -> dict:
        return {
            "avgSimilarity": 0.82,
            "p95LatencyMs": 250,
            "window": "7d",
        }

    def intent_distribution(self) -> dict:
        return {
            "window": "7d",
            "distribution": {
                "regulation": 0.35,
                "exam_schedule": 0.30,
                "study_support": 0.25,
                "unknown": 0.10,
            },
        }

    def latency(self) -> dict:
        return {
            "window": "24h",
            "chatAskP50Ms": 1200,
            "chatAskP95Ms": 3100,
            "regulationQueryP95Ms": 1700,
            "examScheduleP95Ms": 1300,
        }
