# from flext-observability_src/flext_observability/README.md:131
from __future__ import annotations

from flext_observability import FlextMetric, FlextTrace

# Create metric with validation
metric = FlextMetric(
    name="api_response_time",
    value=150.5,
    unit="milliseconds",
    tags={"service": "user-api"},
)

validation = metric.validate_business_rules()
if validation.success:
    print(f"Valid metric: {metric.name}")
