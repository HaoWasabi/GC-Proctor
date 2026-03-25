from services.metrics_service import MetricsService


class MetricsController:
    def __init__(self):
        self.service = MetricsService()

    def fallback_rate(self) -> dict:
        return self.service.fallback_rate()

    def retrieval_quality(self) -> dict:
        return self.service.retrieval_quality()

    def intent_distribution(self) -> dict:
        return self.service.intent_distribution()

    def latency(self) -> dict:
        return self.service.latency()
