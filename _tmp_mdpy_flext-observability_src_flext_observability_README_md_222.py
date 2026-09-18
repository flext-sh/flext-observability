# from flext-observability_src/flext_observability/README.md:222
from __future__ import annotations


# Consistent observability across services
@flext_monitor_function("api_endpoint")
def handle_user_request(request: dict) -> p.Result[m.Dict]:
    # Automatic metrics, tracing, and logging
    return r[bool].ok({"status": "processed"})
