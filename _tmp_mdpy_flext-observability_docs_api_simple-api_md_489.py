# from flext-observability_docs/api/simple-api.md:489
from __future__ import annotations


def handle_user_request(user_id: str, operation: str) -> p.Result[m.Dict]:
    """Example of propagating context through observability."""
    # Create base context
    context = {"user_id": user_id, "operation": operation}

    # Create trace with context
    trace_result = flext_create_trace(
        operation_name=operation, service_name="user-service", context=context
    )

    if trace_result.failure:
        return r[bool].fail(f"Tracing failed: {trace_result.error}")

    trace_id = trace_result.value.id

    # Create metric with tags from context
    metric_result = flext_create_metric(
        name="user_operations",
        value=1,
        unit="count",
        tags={"operation": operation, "user_id": user_id},
    )

    # Create log entry with correlation
    log_result = flext_create_log_entry(
        level="info",
        message=f"Processing {operation} for user {user_id}",
        context=context,
        correlation_id=trace_id,
    )

    return r[bool].ok({"trace_id": trace_id, "status": "success", "context": context})
