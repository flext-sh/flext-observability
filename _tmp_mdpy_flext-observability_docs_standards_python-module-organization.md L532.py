# from flext-observability/docs/standards/python-module-organization.md:532
from __future__ import annotations

# Import from main package - gets essential observability tools
from flext_observability import flext_create_metric, flext_monitor_function


# Use patterns directly in business logic
@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> p.Result[m.Dict]:
    # Create business metrics
    flext_create_metric("orders_processed", 1, "count")

    # Business logic here
    return r[bool].ok({"status": "processed"})
