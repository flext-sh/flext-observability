# from flext-observability/examples/README.md:221
from __future__ import annotations

# Parent-child trace correlation
from flext_observability import flext_create_trace


def process_user_workflow(user_id: str) -> p.Result[m.Dict]:
    """Process user workflow with distributed tracing."""

    # Create parent trace
    parent_trace_result = flext_create_trace(
        operation_name="user_workflow",
        service_name="workflow-service",
        context={"user_id": user_id},
    )

    if parent_trace_result.is_failure:
        return parent_trace_result

    parent_trace = parent_trace_result.data

    # Child operations with trace correlation
    validation_result = validate_user_data(user_id, parent_trace.id)
    if validation_result.is_failure:
        return validation_result

    processing_result = process_user_operation(user_id, parent_trace.id)
    if processing_result.is_failure:
        return processing_result

    return r[bool].ok({
        "user_id": user_id,
        "trace_id": parent_trace.id,
        "status": "completed",
    })


def validate_user_data(user_id: str, parent_trace_id: str) -> p.Result[m.Dict]:
    """Validate user with child trace."""
    child_trace_result = flext_create_trace(
        operation_name="user_validation",
        service_name="validation-service",
        context={"user_id": user_id, "parent_trace_id": parent_trace_id},
    )

    if child_trace_result.is_failure:
        return child_trace_result

    # Validation logic here
    return r[bool].ok({"status": "valid", "trace_id": child_trace_result.data.id})
