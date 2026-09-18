# from flext-observability/docs/standards/python-module-organization.md:485
from __future__ import annotations

# Module names focus on observability concerns
entities.py  # Contains FlextMetric, FlextTrace, FlextAlert entities
services.py  # Contains FlextMetricsService, FlextTracingService
factory.py  # Contains FlextObservabilityMasterFactory
flext_simple.py  # Contains flext_create_* simple API functions
flext_monitor.py  # Contains @flext_monitor_function decorators
flext_structured.py  # Contains structured logging with correlation IDs
obs_platform.py  # Contains FlextObservabilityPlatformV2 orchestration
