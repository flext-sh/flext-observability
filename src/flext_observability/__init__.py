"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

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
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)
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
from flext_observability.version import VERSION, FlextObservabilityVersion

alert = flext_create_alert
health_check = flext_create_health_check
log = flext_create_log_entry
metric = flext_create_metric
trace = flext_create_trace

flext_health_status = flext_create_health_check

PROJECT_VERSION: Final[FlextObservabilityVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

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
    "FlextObservabilityConstants",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityMonitor",
    "FlextObservabilityProtocols",
    "FlextObservabilityService",
    "FlextObservabilityUtilities",
    "FlextObservabilityVersion",
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
