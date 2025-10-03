"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any, Final

from flext_core import FlextConstants, FlextContainer, FlextLogger, FlextTypes
from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.factories import (
    FlextObservabilityMasterFactory,
    get_global_factory,
    reset_global_factory,
)
from flext_observability.fields import (
    AlertLevelField,
    HealthStatusField,
    MetricUnitField,
    MetricValueField,
    TraceStatusField,
    alert_message_field,
    metric_name_field,
    metric_unit_field,
    metric_value_field,
    timestamp_field,
    trace_name_field,
)
from flext_observability.models import (
    FlextObservabilityModels,
)
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.protocols import FlextObservabilityProtocols
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextMetricsService,
    FlextObservabilityService,
    FlextObservabilityUtilities,
    FlextTracingService,
    FlextUtilitiesGenerators,
)
from flext_observability.typings import (
    AlertLevel,
    AlertProtocol,
    HealthCheckProtocol,
    HealthStatus,
    LogEntryProtocol,
    LogLevel,
    MetricProtocol,
    MetricValue,
    ObservabilityTypes,
    TagsDict,
    TraceProtocol,
    TraceStatus,
)
from flext_observability.version import VERSION

# Expose entity classes for backward compatibility
FlextAlert = FlextObservabilityModels.FlextAlert
FlextHealthCheck = FlextObservabilityModels.FlextHealthCheck
FlextLogEntry = FlextObservabilityModels.FlextLogEntry
FlextMetric = FlextObservabilityModels.FlextMetric
FlextTrace = FlextObservabilityModels.FlextTrace


# Create thin facade functions using global factory
def flext_create_alert(
    title: str, message: str, severity: str = "info", source: str = "system"
) -> Any:
    """Create an alert using the global factory."""
    return get_global_factory().create_alert(title, message, severity, source)


def flext_create_health_check(
    service_name: str, status: str = "healthy", details: dict[str, Any] | None = None
) -> Any:
    """Create a health check using the global factory."""
    return get_global_factory().create_health_check(service_name, status, details)


def flext_create_log_entry(
    level: str, message: str, metadata: dict[str, Any] | None = None
) -> Any:
    """Create a log entry using the global factory."""
    return get_global_factory().create_log_entry(level, message, metadata)


def flext_create_metric(name: str, value: float, unit: str = "count") -> Any:
    """Create a metric using the global factory."""
    return get_global_factory().create_metric(name, value, unit)


def flext_create_trace(
    name: str, operation: str, context: dict[str, Any] | None = None
) -> Any:
    """Create a trace using the global factory."""
    return get_global_factory().create_trace(name, operation, context)


# Create aliases for backward compatibility
alert = flext_create_alert
health_check = flext_create_health_check
log = flext_create_log_entry
metric = flext_create_metric
trace = flext_create_trace

flext_health_status = flext_create_health_check

PROJECT_VERSION: Final[str] = VERSION

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "AlertLevel",
    "AlertLevelField",
    "AlertProtocol",
    "FlextAlert",
    "FlextAlertService",
    "FlextConstants",
    "FlextContainer",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLogger",
    "FlextMetric",
    "FlextMetricsService",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityMonitor",
    "FlextObservabilityProtocols",
    "FlextObservabilityService",
    "FlextObservabilityUtilities",
    "FlextTrace",
    "FlextTracingService",
    "FlextTypes",
    "FlextUtilitiesGenerators",
    "HealthCheckProtocol",
    "HealthStatus",
    "HealthStatusField",
    "LogEntryProtocol",
    "LogLevel",
    "MetricProtocol",
    "MetricUnitField",
    "MetricValue",
    "MetricValueField",
    "ObservabilityTypes",
    "TagsDict",
    "TraceProtocol",
    "TraceStatus",
    "TraceStatusField",
    "__version__",
    "__version_info__",
    "alert",
    "alert_message_field",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_status",
    "flext_monitor_function",
    "get_global_factory",
    "health_check",
    "log",
    "metric",
    "metric_name_field",
    "metric_unit_field",
    "metric_value_field",
    "reset_global_factory",
    "timestamp_field",
    "trace",
    "trace_name_field",
]
