# from flext-observability/docs/standards/python-module-organization.md:1498
from __future__ import annotations

# ✅ Standard observability imports across ecosystem
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    FlextMetricsService,
)


# ✅ Consistent observability patterns across FLEXT projects
class FlextUserService:
    """User service with standardized observability."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container
        self.observability = FlextMetricsService(container)

    @flext_monitor_function("user_creation")
    def create_user(self, user_data: dict) -> p.Result[m.Dict]:
        """Create user with automatic observability."""
        # Business metrics
        flext_create_metric(
            "users_created", 1, "count", tags={"service": "user-service"}
        )

        # Business logic
        result = self._create_user_impl(user_data)

        # Success/failure metrics
        status = "success" if result.success else "failure"
        flext_create_metric(
            "user_creation_status",
            1,
            "count",
            tags={"status": status, "service": "user-service"},
        )

        return result


# ✅ Cross-service observability correlation
def sync_user_between_services(user_id: str) -> p.Result[m.Dict]:
    """Sync user data between services with trace correlation."""
    # Create correlation trace
    correlation_trace = flext_create_trace("user_sync", "integration-service")
    if correlation_trace.failure:
        return correlation_trace

    trace_id = correlation_trace.data.id

    # LDAP service call with trace context
    ldap_result = fetch_user_from_ldap(user_id, trace_id)
    if ldap_result.failure:
        return ldap_result

    # Oracle service call with trace context
    oracle_result = update_user_in_oracle(user_id, ldap_result.value, trace_id)
    if oracle_result.failure:
        return oracle_result

    # Success metrics
    flext_create_metric(
        "user_sync_completed", 1, "count", tags={"correlation_id": trace_id}
    )

    return r[bool].ok({
        "user_id": user_id,
        "correlation_id": trace_id,
        "status": "synchronized",
    })


# ❌ Don't create service-specific observability types
class UserMetric:  # Use FlextMetric instead
    pass


class OracleTrace:  # Use FlextTrace instead
    pass
