# from flext-observability_docs/architecture/README.md:258
from __future__ import annotations

# Consistent monitoring across all FLEXT projects
from flext_observability import flext_monitor_function


@flext_monitor_function("flext_api_endpoint")
def process_api_request(request_data):
    """Automatic metrics, tracing, and logging."""
    return {"status": "processed"}
