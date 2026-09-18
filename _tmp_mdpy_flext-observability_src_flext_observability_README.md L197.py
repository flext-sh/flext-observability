# from flext-observability/src/flext_observability/README.md:197
from __future__ import annotations

from flext_observability import flext_monitor_function


@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> t.JsonMapping:
    # Automatically monitored for execution time, success/failure
    return {"status": "processed", "order_id": order_data["id"]}
