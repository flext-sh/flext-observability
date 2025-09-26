"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants, FlextContainer, FlextLogger, FlextTypes
from flext_observability.api import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    FlextUtilitiesGenerators,
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)
from flext_observability.factories import FlextObservabilityService
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
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
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

# Backward compatibility aliases
alert = flext_create_alert
health_check = flext_create_health_check
log = flext_create_log_entry
metric = flext_create_metric
trace = flext_create_trace

# Legacy function alias
flext_health_status = flext_create_health_check

# Remove unused TYPE_CHECKING - not needed

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Import FlextLogger from flext_core

# Simple API from api module
# No public API classes currently

# Factory patterns from factories module

# Core entities from models module

# Monitor patterns from monitoring module

# Services from services module


# flext_health_status function moved to api.py module


# Legacy facades removed - use direct imports from flext-core and factory classes

__all__: FlextTypes.Core.StringList = [
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
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    "FlextObservabilityConstants",
    "FlextObservabilityConstants",
    "FlextObservabilityMonitor",
    "FlextObservabilityService",
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
    "flext_alert",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    "flext_health_status",
    "flext_metric",
    "flext_monitor_function",
    "flext_trace",
    "health_check",
    "log",
    "metric",
    "metric_name_field",
    "metric_unit_field",
    "metric_value_field",
    "timestamp_field",
    "trace",
    "trace_name_field",
]
