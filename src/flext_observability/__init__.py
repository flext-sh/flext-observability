"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from decimal import Decimal
from typing import Final

from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextTypes,
)

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
    FlextObservabilityServices,
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

# Expose entity classes for backward compatibility
FlextAlert = FlextObservabilityModels.FlextAlert
FlextHealthCheck = FlextObservabilityModels.FlextHealthCheck
FlextLogEntry = FlextObservabilityModels.FlextLogEntry
FlextMetric = FlextObservabilityModels.FlextMetric
FlextTrace = FlextObservabilityModels.FlextTrace


class FlextObservability:
    """Unified observability facade following namespace class pattern.

    Provides consolidated access to all observability operations through
    nested factory classes, maintaining the single-class-with-nested-structure pattern.
    """

    class Factory:
        """Factory operations for observability entities."""

        @staticmethod
        def create_alert(
            title: str, message: str, severity: str = "info", source: str = "system"
        ) -> FlextResult[FlextTypes.Dict]:
            """Create an alert using the global factory."""
            return get_global_factory().create_alert(title, message, severity, source)

        @staticmethod
        def create_health_check(
            service_name: str,
            status: str = "healthy",
            details: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a health check using the global factory."""
            return get_global_factory().create_health_check(
                service_name, status, details
            )

        @staticmethod
        def create_log_entry(
            level: str, message: str, metadata: FlextTypes.Dict | None = None
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a log entry using the global factory."""
            return get_global_factory().create_log_entry(level, message, metadata)

        @staticmethod
        def create_metric(
            name: str, value: float, unit: str = "count"
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a metric using the global factory."""
            return get_global_factory().create_metric(name, value, unit)

        @staticmethod
        def create_trace(
            name: str, operation: str, context: FlextTypes.Dict | None = None
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a trace using the global factory."""
            return get_global_factory().create_trace(name, operation, context)

    class Entities:
        """Direct entity creation operations."""

        @staticmethod
        def metric(
            name: str,
            value: float | Decimal,
            unit: str = "",
            metric_type: str = "gauge",
            **kwargs: object,
        ) -> FlextObservabilityModels.FlextMetric:
            """Create a FlextMetric entity directly."""
            result = FlextObservabilityModels.flext_metric(
                name, value, unit, metric_type, **kwargs
            )
            if result.is_failure:
                msg = f"Failed to create metric: {result.error}"
                raise ValueError(msg)
            return result.unwrap()

        @staticmethod
        def trace(
            trace_id: str,
            operation: str,
            span_id: str,
            status: str = "pending",
            **kwargs: object,
        ) -> FlextObservabilityModels.FlextTrace:
            """Create a FlextTrace entity directly."""
            result = FlextObservabilityModels.flext_trace(
                trace_id, operation, span_id, status, **kwargs
            )
            if result.is_failure:
                msg = f"Failed to create trace: {result.error}"
                raise ValueError(msg)
            return result.unwrap()

        @staticmethod
        def health_check(
            component: str,
            status: str = "unknown",
            message: str = "",
            **kwargs: object,
        ) -> FlextObservabilityModels.FlextHealthCheck:
            """Create a FlextHealthCheck entity directly."""
            result = FlextObservabilityModels.flext_health_check(
                component, status, message, **kwargs
            )
            if result.is_failure:
                msg = f"Failed to create health check: {result.error}"
                raise ValueError(msg)
            return result.unwrap()


# Backward compatibility aliases - use FlextResult properly
def flext_create_alert(
    title: str, message: str, severity: str = "info", source: str = "system"
) -> FlextResult[FlextTypes.Dict]:
    """Create an alert using the factory (backward compatibility)."""
    return FlextObservability.Factory.create_alert(title, message, severity, source)


def flext_create_health_check(
    service_name: str, status: str = "healthy", details: FlextTypes.Dict | None = None
) -> FlextResult[FlextTypes.Dict]:
    """Create a health check using the factory (backward compatibility)."""
    return FlextObservability.Factory.create_health_check(service_name, status, details)


def flext_create_log_entry(
    level: str, message: str, metadata: FlextTypes.Dict | None = None
) -> FlextResult[FlextTypes.Dict]:
    """Create a log entry using the factory (backward compatibility)."""
    return FlextObservability.Factory.create_log_entry(level, message, metadata)


def flext_create_metric(
    name: str, value: float, unit: str = "count"
) -> FlextResult[FlextTypes.Dict]:
    """Create a metric using the factory (backward compatibility)."""
    return FlextObservability.Factory.create_metric(name, value, unit)


def flext_create_trace(
    name: str, operation: str, context: FlextTypes.Dict | None = None
) -> FlextResult[FlextTypes.Dict]:
    """Create a trace using the factory (backward compatibility)."""
    return FlextObservability.Factory.create_trace(name, operation, context)


flext_metric = FlextObservability.Entities.metric
flext_trace = FlextObservability.Entities.trace
flext_health_check = FlextObservability.Entities.health_check

# Additional backward compatibility aliases
alert = flext_create_alert
health_check = flext_create_health_check
log = flext_create_log_entry
metric = flext_create_metric
trace = flext_create_trace
flext_health_status = flext_create_health_check

# Backward compatibility for consolidated classes
FlextObservabilityService = FlextObservabilityServices
FlextObservabilityUtilities = FlextObservabilityServices
FlextUtilitiesGenerators = FlextObservabilityServices.Generators

PROJECT_VERSION: Final[str] = VERSION

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "AlertLevel",
    "AlertLevelField",
    "AlertProtocol",
    "FlextAlert",
    "FlextConstants",
    "FlextContainer",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextLogger",
    "FlextMetric",
    "FlextObservability",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityMonitor",
    "FlextObservabilityProtocols",
    "FlextObservabilityService",
    "FlextObservabilityServices",
    "FlextObservabilityTypes",
    "FlextObservabilityTypesAlias",
    "FlextObservabilityUtilities",
    "FlextTrace",
    "FlextTracingService",
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
