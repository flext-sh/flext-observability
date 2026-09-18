# from flext-observability/src/flext_observability/README.md:151
from __future__ import annotations

from flext_observability import FlextMetricsService
from flext_cli import u
from flext_core import FlextSettings

container = FlextContainer()
metrics_service = FlextMetricsService(container)

result = metrics_service.record_metric(metric)
if result.success:
    print(f"Recorded: {result.data.name}")
