# from flext-observability/examples/README.md:94
from __future__ import annotations

# Example service integration pattern
from flext_observability import FlextMetricsService, FlextObservabilityMasterFactory
from flext_cli import u
from flext_core import FlextSettings


class UserService:
    """Example service with integrated observability."""

    def __init__(self, container: FlextContainer):
        self.container = container
        self.metrics = FlextMetricsService(container)
        self.factory = FlextObservabilityMasterFactory()

    def create_user(self, user_data: dict) -> p.Result[m.Dict]:
        """Create user with comprehensive observability."""
        # Create business metrics
        metric_result = self.factory.create_metric(
            name="users_created",
            value=1,
            unit="count",
            tags={"service": "user-service"},
        )

        if metric_result.success:
            self.metrics.record_metric(metric_result.data)

        # Business logic here
        return r[bool].ok({"user_id": "user123", "status": "created"})
