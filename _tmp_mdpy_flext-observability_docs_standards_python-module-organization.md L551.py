# from flext-observability/docs/standards/python-module-organization.md:551
from __future__ import annotations

# Import services for advanced integration
from flext_observability import (
    FlextMetricsService,
    FlextTracingService,
    FlextObservabilityMasterFactory,
)


class UserAPIService:
    def __init__(self, container: FlextContainer) -> None:
        self.metrics = FlextMetricsService(container)
        self.tracing = FlextTracingService(container)
        self.factory = FlextObservabilityMasterFactory()

    def handle_user_request(self, request: dict) -> p.Result[m.Dict]:
        # Create request trace
        trace_result = self.factory.create_trace("user_request", "user-api")
        if trace_result.failure:
            return trace_result

        # Record request metric
        metric_result = self.factory.create_metric(
            "api_requests", 1, "count", tags={"endpoint": "/users"}
        )

        # Process with observability
        return self._process_user_request(request, trace_result.value)
