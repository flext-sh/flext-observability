# from flext-observability/docs/api/simple-api.md:541
from __future__ import annotations

# ❌ MyPy will catch these type errors
flext_create_metric(123, "not_a_number")  # Wrong parameter types
flext_create_trace(None, "service")  # None not allowed for required params

# ✅ Correct usage
flext_create_metric("cpu_usage", 75.5, "percent")
flext_create_trace("operation", "service")
