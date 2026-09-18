# from flext-observability/docs/standards/python-module-organization.md:730
from __future__ import annotations

# Basic metric creation
def create_business_metrics(operation: str, duration: float, success: bool) -> None:
    """Create comprehensive business metrics."""

    # Performance metric
    duration_result = flext_create_metric(
        name=f"{operation}_duration",
        value=duration,
        unit="seconds",
        tags={"operation": operation, "service": "payment-service"}
    )

    # Success/failure metric
    status_result = flext_create_metric(
        name=f"{operation}_status",
        value=1,
        unit="count",
        tags={"operation": operation, "status": "success" if success else "failure"},
        metric_type="counter"
    )

    # Business KPI metric
    kpi_result = flext_create_metric(
        name="business_transactions",
        value=1,
        unit="count",
        tags={"type": operation, "outcome": "success" if success else "failure"},
        metric_type="counter"
    )

# Advanced metric patterns with validation
def create_validated_metric(name: str, value: float) -> p.Result[bool]:
    """Create metric with comprehensive validation."""
    metric_result = flext_create_metric(name, value, "count")

    if metric_result.failure:
        # Log metric creation failure
        log_result = flext_create_log_entry(
            level="error",
            message=f"Failed to create metric {name}: {metric_result.error}",
            context={"metric_name": name, "metric_value": str(value)}
        )
        return r[bool].fail(f"Metric creation failed: {metric_result.error}")

    return r[bool].| ok(value=True)
