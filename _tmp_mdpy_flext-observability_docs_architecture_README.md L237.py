# from flext-observability/docs/architecture/README.md:237
from __future__ import annotations

# All services use flext-core patterns
from flext_observability import FlextMetricsService

container = FlextContainer()
service = FlextMetricsService(container)

# Railway-oriented programming throughout
result = service.record_metric(metric)
if result.success:
    # Success path
    return result.value
else:
    # Error path - no exceptions
    return result.error
