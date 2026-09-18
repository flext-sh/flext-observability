# from flext-observability/examples/README.md:315
from __future__ import annotations

# Example FastAPI service with observability
from flext_observability import flext_monitor_function, flext_create_metric


class FlextAPIService:
    """Example FastAPI service with observability."""

    @flext_monitor_function("api_endpoint")
    def handle_user_request(self, request_data: dict) -> p.Result[m.Dict]:
        """Handle API request with comprehensive observability."""

        # Request metrics
        flext_create_metric(
            name="api_requests",
            value=1,
            unit="count",
            tags={"endpoint": "/users", "method": "POST", "service": "user-api"},
        )

        # Business logic
        result = self._process_user_request(request_data)

        # Response metrics
        status = "success" if result.success else "error"
        flext_create_metric(
            name="api_responses",
            value=1,
            unit="count",
            tags={"endpoint": "/users", "status": status, "service": "user-api"},
        )

        return result
