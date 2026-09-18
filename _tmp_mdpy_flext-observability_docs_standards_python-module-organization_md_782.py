# from flext-observability_docs/standards/python-module-organization.md:782
from __future__ import annotations


# Parent-child trace correlation
def process_order_with_tracing(order_data: dict) -> p.Result[m.Dict]:
    """Process order with distributed tracing."""
    # Create parent trace
    parent_trace_result = flext_create_trace("process_order", "order-service")
    if parent_trace_result.failure:
        return parent_trace_result

    parent_trace = parent_trace_result.value

    # Create child operations with parent correlation
    validate_result = validate_order_with_trace(order_data, parent_trace.id)
    if validate_result.failure:
        return validate_result

    payment_result = process_payment_with_trace(order_data, parent_trace.id)
    if payment_result.failure:
        return payment_result

    return r[bool].ok({"order_id": "order123", "trace_id": parent_trace.id})


def validate_order_with_trace(
    order_data: dict, parent_trace_id: str
) -> p.Result[m.Dict]:
    """Validate order with child trace."""
    child_trace_result = flext_create_trace(
        operation_name="validate_order",
        service_name="validation-service",
        context={
            "parent_trace_id": parent_trace_id,
            "order_size": str(len(order_data)),
        },
    )

    if child_trace_result.failure:
        return child_trace_result

    # Validation logic with trace context
    return r[bool].ok({"status": "valid", "trace_id": child_trace_result.value.id})
