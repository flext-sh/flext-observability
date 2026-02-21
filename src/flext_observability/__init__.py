"""Enterprise observability and monitoring library for FLEXT ecosystem.

FLEXT Observability provides unified observability patterns for monitoring, metrics,
tracing, and alerting across the FLEXT ecosystem using FlextResult railway pattern.

Architecture:
- Single FlextObservability class (domain library pattern)
- Nested domain entities (Metric, Trace, Alert, HealthCheck, LogEntry)
- Nested application services (MetricsService, TracingService, etc.)
- Clean Architecture layers with SOLID principles
- Railway-oriented programming with FlextResult[T]

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_observability.__version__ import __version__, __version_info__
from flext_observability._core import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextObservability,
    FlextObservabilityConstants,
    FlextObservabilityMasterFactory,
    FlextTrace,
    flext_alert,
    flext_create_health_check,
    flext_health_check,
    flext_log_entry,
    flext_metric,
    flext_trace,
    get_global_factory,
    reset_global_factory,
)

# Import from submodules for re-export
from flext_observability.advanced_context import FlextObservabilityAdvancedContext
from flext_observability.constants import ErrorSeverity, MetricType
from flext_observability.context import FlextObservabilityContext
from flext_observability.custom_metrics import (
    CustomMetricDefinition,
    FlextObservabilityCustomMetrics,
)
from flext_observability.error_handling import (
    ErrorEvent,
    FlextObservabilityErrorHandling,
)

# Import additional exports
from flext_observability.fields import FlextObservabilityFields
from flext_observability.health import FlextObservabilityHealth
from flext_observability.http_client_instrumentation import FlextObservabilityHTTPClient
from flext_observability.http_instrumentation import FlextObservabilityHTTP
from flext_observability.logging_integration import FlextObservabilityLogging
from flext_observability.models import FlextObservabilityModels
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.performance import FlextObservabilityPerformance
from flext_observability.protocols import FlextObservabilityProtocols
from flext_observability.sampling import FlextObservabilitySampling
from flext_observability.settings import FlextObservabilitySettings
from flext_observability.typings import FlextObservabilityTypes, t

__all__ = [
    "CustomMetricDefinition",
    "ErrorEvent",
    "ErrorSeverity",
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityConstants",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityFields",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilityProtocols",
    "FlextObservabilitySampling",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextTrace",
    "MetricType",
    "__version__",
    "__version_info__",
    "flext_alert",
    "flext_create_health_check",
    "flext_health_check",
    "flext_log_entry",
    "flext_metric",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "reset_global_factory",
    "t",
]
