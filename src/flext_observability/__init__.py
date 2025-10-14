"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.factories import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)
from flext_observability.fields import (
    FlextObservabilityFields,
)
from flext_observability.models import (
    FlextObservabilityModels,
)
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.services import (
    FlextObservabilityMasterFactory,
    FlextObservabilityServices,
    get_global_factory,
    reset_global_factory,
)
from flext_observability.typings import (
    FlextObservabilityTypes,
    HealthCheckProtocol,
    LogEntryProtocol,
    MetricProtocol,
    ObservabilityTypes,
    TagsDict,
    TraceProtocol,
)

# Direct model exports from consolidated models
FlextMetric = FlextObservabilityModels.Metrics.MetricEntry
FlextTrace = FlextObservabilityModels.Tracing.TraceEntry
FlextAlert = FlextObservabilityModels.Alerting.AlertEntry
FlextHealthCheck = FlextObservabilityModels.Health.HealthCheckEntry
FlextLogEntry = FlextObservabilityModels.Logging.LogEntry

# Removed over-engineered FlextObservability facade class - not used anywhere in flext ecosystem


# Removed over-engineered FlextObservability facade class - not used anywhere in flext ecosystem

__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityFields",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityServices",
    "FlextObservabilityTypes",
    "FlextTrace",
    "HealthCheckProtocol",
    "LogEntryProtocol",
    "MetricProtocol",
    "ObservabilityTypes",
    "TagsDict",
    "TraceProtocol",
    "__version__",
    "__version_info__",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_monitor_function",
    "get_global_factory",
    "get_global_observability_service",
    "reset_global_factory",
]
