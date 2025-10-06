"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.factories import (
    FlextObservabilityFactories,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
    get_global_observability_service,
)
from flext_observability.fields import (
    AlertLevelField,
    FlextObservabilityFields,
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
    FlextAlert,
    FlextHealthCheck,
    FlextMetric,
    FlextObservabilityModels,
    FlextTrace,
)
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.protocols import FlextObservabilityProtocols
from flext_observability.services import (
    FlextObservabilityMasterFactory,
    FlextObservabilityServices,
    get_global_factory,
    reset_global_factory,
)
from flext_observability.typings import (
    AlertLevel,
    AlertProtocol,
    FlextObservabilityTypes,
    FlextObservabilityTypesAlias,
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

# Removed over-engineered FlextObservability facade class - not used anywhere in flext ecosystem

__all__ = [
    "VERSION",
    "AlertLevel",
    "AlertLevelField",
    "AlertProtocol",
    "FlextAlert",
    "FlextHealthCheck",
    "FlextMetric",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityFactories",
    "FlextObservabilityFields",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityProtocols",
    "FlextObservabilityServices",
    "FlextObservabilityTypes",
    "FlextObservabilityTypesAlias",
    "FlextTrace",
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
    "alert_message_field",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_monitor_function",
    "get_global_factory",
    "get_global_observability_service",
    "metric_name_field",
    "metric_unit_field",
    "metric_value_field",
    "reset_global_factory",
    "timestamp_field",
    "trace_name_field",
]
