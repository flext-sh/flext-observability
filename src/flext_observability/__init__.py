"""FLEXT Observability - Clean Architecture using flext-core.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture implementation using flext-core as foundation.
Following SOLID, KISS, DRY principles with dependency injection.

Simple usage:
>>> from flext_observability import configure_observability_container, get_observability_service
>>> from flext_observability import Metric, LogEntry, Trace, Alert, HealthCheck
>>>
>>> # Configure DI container
>>> configure_observability_container()
>>>
>>> # Use services through DI
>>> metrics_service = get_observability_service("metrics_service")
>>> metric = Metric(name="cpu_usage", value=75.5, unit="percentage")
>>> result = metrics_service.record_metric(metric)
"""

from __future__ import annotations

# Application services with DI
from flext_observability.application.services import (
    AlertService,
    HealthService,
    LoggingService,
    MetricsService,
    TracingService,
)

# Constants from flext-observability specific
# from flext_observability.constants import (
#     ALERT_SEVERITY_LEVELS,
#     HEALTH_STATUS_VALUES,
#     LOG_LEVELS,
#     METRIC_TYPES,
#     TRACE_STATUS_VALUES,
# )
# DI container configuration
from flext_observability.container import (
    configure_observability_container,
    get_observability_service,
)

# Core domain entities using flext-core bases
from flext_observability.domain.entities import (
    Alert,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)

__version__ = "0.8.0"

# Clean public API - Essential components only
__all__ = [
    # Core entities
    "Alert",
    # Application services
    "AlertService",
    "HealthCheck",
    "HealthService",
    "LogEntry",
    "LoggingService",
    "Metric",
    "MetricsService",
    "Trace",
    "TracingService",
    # Version
    "__version__",
    # DI container
    "configure_observability_container",
    "get_observability_service",
]
