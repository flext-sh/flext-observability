# from flext-observability_src/flext_observability/README.md:168
from __future__ import annotations

from flext_observability import FlextObservabilityMasterFactory

factory = FlextObservabilityMasterFactory()
metric_result = factory.create_metric("cpu_usage", 75.2, "percent")

if metric_result.success:
    metric = metric_result.data
    print(f"Created metric: {metric.name}")
