# from flext-observability_docs/api/simple-api.md:202
from __future__ import annotations

from flext_observability import flext_create_trace

# Basic trace
result = flext_create_trace("user_login", "authentication-service")
if result.success:
    trace = result.value
    print(f"Started trace: {trace.operation_name} in {trace.service_name}")

# Trace with context
result = flext_create_trace(
    operation_name="process_payment",
    service_name="payment-service",
    context={
        "user_id": "user123",
        "order_id": "order456",
        "payment_method": "credit_card",
    },
)

# Child trace with parent correlation
parent_result = flext_create_trace("api_request", "user-api")
if parent_result.success:
    child_result = flext_create_trace(
        operation_name="database_query",
        service_name="user-api",
        parent_trace_id=parent_result.value.id,
    )
