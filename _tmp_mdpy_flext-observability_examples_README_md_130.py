# from flext-observability_examples/README.md:130
from __future__ import annotations

# Automatic function monitoring
from flext_observability import flext_monitor_function


@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> t.JsonMapping:
    """Process order with automatic monitoring.

    This function automatically gets:
    - Execution time metrics
    - Success/failure tracking
    - Distributed tracing spans
    - Structured logging with correlation IDs
    """
    # Business logic
    processed_order = {
        "order_id": order_data["id"],
        "status": "processed",
        "items": len(order_data.get("items", [])),
    }

    return processed_order


# Advanced monitoring with context
@flext_monitor_function("payment_processing")
def process_payment(amount: float, currency: str) -> p.Result[m.Dict]:
    """Process payment with error handling and monitoring."""
    if amount <= 0:
        return r[bool].fail("Invalid payment amount")

    # Payment processing logic
    transaction = {
        "transaction_id": "txn_123",
        "amount": amount,
        "currency": currency,
        "status": "completed",
    }

    return r[bool].ok(transaction)
