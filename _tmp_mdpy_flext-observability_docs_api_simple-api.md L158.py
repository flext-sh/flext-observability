# from flext-observability/docs/api/simple-api.md:158
from __future__ import annotations

# Invalid metric name
result = flext_create_metric("", 100.0)
assert not result.success
assert "Invalid metric name" in result.error

# Invalid value type
result = flext_create_metric("test", "not_a_number")
assert not result.success
assert "Invalid metric value" in result.error
