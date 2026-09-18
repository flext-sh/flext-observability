# from flext-observability_docs/api/simple-api.md:433
from __future__ import annotations

from flext_observability import flext_create_metric, flext_create_trace


def process_business_operation(data: dict) -> p.Result[m.Dict]:
    """Example of chaining observability operations."""
    # Create metric - handle potential failure
    metric_result = flext_create_metric("operations_started", 1, "count")
    if metric_result.failure:
        return r[bool].fail(f"Failed to create metric: {metric_result.error}")

    # Create trace - handle potential failure
    trace_result = flext_create_trace("business_operation", "main-service")
    if trace_result.failure:
        return r[bool].fail(f"Failed to create trace: {trace_result.error}")

    # Business logic here
    result_data = {"status": "processed", "data": data}

    # Success metric
    success_metric = flext_create_metric("operations_completed", 1, "count")
    # Note: In production, you might want to handle this error too

    return r[bool].ok(result_data)
