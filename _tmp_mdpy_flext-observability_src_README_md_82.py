# from flext-observability_src/README.md:82
from __future__ import annotations

from flext_observability import FlextObservability, flext_monitor_function, t


# Create observability data
metric_result = FlextObservability.flext_metric("api_requests", 42, "count")
trace_result = FlextObservability.flext_trace("user_login", {"service": "auth-service"})


# Use monitoring decorators
@flext_monitor_function("business_operation")
def process_order(order_data: dict) -> t.JsonMapping:
    return {"status": "processed"}


_ = metric_result, trace_result, process_order
