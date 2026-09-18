# from flext-observability_docs/standards/python-module-organization.md:1344
from __future__ import annotations


# ✅ Always use r for observability error handling
def create_comprehensive_observability(operation: str) -> p.Result[m.Dict]:
    """Create comprehensive observability data with error handling."""
    # Chain observability operations with proper error handling
    metric_result = flext_create_metric(f"{operation}_requests", 1, "count")
    if metric_result.failure:
        return r[bool].fail(f"Failed to create metric: {metric_result.error}")

    trace_result = flext_create_trace(operation, "main-service")
    if trace_result.failure:
        return r[bool].fail(f"Failed to create trace: {trace_result.error}")

    return r[bool].ok({
        "metric": metric_result.value,
        "trace": trace_result.value,
        "correlation_id": trace_result.value.id,
    })


# ✅ Chain observability operations safely
def monitor_business_operation(operation_data: dict) -> p.Result[m.Dict]:
    """Monitor business operation with comprehensive observability."""
    return (
        flext_create_trace("business_operation", "business-service")
        .flat_map(
            lambda trace: flext_create_metric("operations_started", 1, "count").map(
                lambda metric: {"trace": trace, "metric": metric}
            )
        )
        .flat_map(
            lambda obs_data: process_operation(
                operation_data, obs_data["trace"].id
            ).map(lambda result: {**result, **obs_data})
        )
    )


# ❌ Never raise exceptions for observability failures
def create_metric_bad(name: str, value: float) -> FlextMetric:
    """Bad example - raises exceptions."""
    if not name:
        raise ValueError("Name is required")  # Breaks railway pattern
    return FlextMetric(name=name, value=value)
