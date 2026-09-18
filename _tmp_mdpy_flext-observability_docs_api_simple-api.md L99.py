# from flext-observability/docs/api/simple-api.md:99
from __future__ import annotations

def flext_create_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    tags: t.StringDict | None = None,
    metric_type: str = "gauge"
) -> p.Result[FlextMetric]
