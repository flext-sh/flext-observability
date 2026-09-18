# from flext-observability/docs/standards/python-module-organization.md:703
from __future__ import annotations

# Handled via decorators and context management
from flext_observability import flext_monitor_function, correlation_id


@flext_monitor_function("critical_business_operation")
def process_payment(payment_data: dict) -> p.Result[m.Dict]:
    """Function automatically gets observability patterns."""
    request_correlation_id = correlation_id()

    # Business logic with automatic:
    # - Execution time metrics
    # - Success/failure tracing
    # - Structured logging with correlation ID
    # - Error capture and categorization

    return r[bool].ok({"status": "processed", "correlation_id": correlation_id})
