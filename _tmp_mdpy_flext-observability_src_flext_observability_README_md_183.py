# from flext-observability_src/flext_observability/README.md:183
from __future__ import annotations

from flext_observability import flext_create_metric, flext_create_trace

# Quick metric creation
metric_result = flext_create_metric("requests_total", 1, "count")

# Quick trace creation
trace_result = flext_create_trace("user_login", "auth-service")
