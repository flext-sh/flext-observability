"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult
from pydantic import BaseModel, Field

from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.health import FlextObservabilityHealth
from flext_observability.logging import FlextObservabilityLogging
from flext_observability.models import FlextObservabilityModels
from flext_observability.monitoring import flext_monitor_function
from flext_observability.services import (
    FlextObservabilityServices,
    FlextObservabilityUtilities,
)

# Export entity classes
FlextHealthCheck = FlextObservabilityHealth.FlextHealthCheck
FlextLogEntry = FlextObservabilityLogging.FlextLogEntry

# Single generic entry for all observability types
FlextObservabilityEntry = FlextObservabilityModels.GenericObservabilityEntry


# Entity classes for missing modules
class FlextMetric(BaseModel):
    """Observability metric entity."""

    name: str = Field(description="Metric name")
    value: float = Field(description="Metric value")
    unit: str = Field(default="count", description="Metric unit")
    metric_type: str = Field(default="gauge", description="Metric type")
    timestamp: float = Field(
        default_factory=__import__("time").time, description="Metric timestamp"
    )


class FlextTrace(BaseModel):
    """Observability trace entity."""

    trace_id: str = Field(description="Trace ID")
    name: str = Field(description="Trace name")
    operation: str = Field(description="Operation name")
    timestamp: float = Field(
        default_factory=__import__("time").time, description="Trace timestamp"
    )


class FlextAlert(BaseModel):
    """Observability alert entity."""

    name: str = Field(description="Alert name")
    severity: str = Field(default="warning", description="Alert severity")
    message: str = Field(description="Alert message")
    source: str = Field(default="system", description="Alert source")
    timestamp: float = Field(
        default_factory=__import__("time").time, description="Alert timestamp"
    )


# Generic factory function - all observability creation goes through this
def flext_create_entry(
    name: str,
    entry_type: str,
    data: dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
) -> FlextResult[FlextObservabilityEntry]:
    """Create generic observability entry - all creation goes through this."""
    try:
        if not name or not isinstance(name, str):
            return FlextResult[FlextObservabilityEntry].fail(
                "Entry name must be non-empty string"
            )
        if not entry_type or not isinstance(entry_type, str):
            return FlextResult[FlextObservabilityEntry].fail(
                "Entry type must be non-empty string"
            )

        entry = FlextObservabilityEntry(
            name=name.strip(),
            type=entry_type.strip(),
            data=data or {},
            metadata=metadata or {},
        )
        return FlextResult[FlextObservabilityEntry].ok(entry)
    except Exception as e:
        return FlextResult[FlextObservabilityEntry].fail(f"Entry creation failed: {e}")


# Factory functions for entity creation
def flext_create_metric(
    name: str,
    value: float,
    unit: str = "count",
    metric_type: str | None = None,
) -> FlextResult[FlextMetric]:
    """Create observability metric."""
    try:
        # Auto-detect metric type if not provided
        inferred_type = metric_type
        if not inferred_type:
            if name.endswith(("_total", "_count")):
                inferred_type = "counter"
            elif name.endswith(("_duration", "_seconds")):
                inferred_type = "histogram"
            else:
                inferred_type = "gauge"

        metric = FlextMetric(
            name=name,
            value=value,
            unit=unit,
            metric_type=inferred_type,
        )
        return FlextResult[FlextMetric].ok(metric)
    except Exception as e:
        return FlextResult[FlextMetric].fail(f"Metric creation failed: {e}")


def flext_create_trace(
    trace_id: str,
    name: str,
    operation: str | None = None,
) -> FlextResult[FlextTrace]:
    """Create observability trace."""
    try:
        trace = FlextTrace(
            trace_id=trace_id,
            name=name,
            operation=operation or name,
        )
        return FlextResult[FlextTrace].ok(trace)
    except Exception as e:
        return FlextResult[FlextTrace].fail(f"Trace creation failed: {e}")


def flext_create_alert(
    name: str,
    severity: str = "warning",
    message: str = "",
    source: str = "system",
) -> FlextResult[FlextAlert]:
    """Create observability alert."""
    try:
        alert = FlextAlert(
            name=name,
            severity=severity,
            message=message,
            source=source,
        )
        return FlextResult[FlextAlert].ok(alert)
    except Exception as e:
        return FlextResult[FlextAlert].fail(f"Alert creation failed: {e}")


def flext_create_health_check(
    name: str,
    status: str = "healthy",
    details: dict[str, object] | None = None,
) -> FlextResult[FlextHealthCheck]:
    """Create observability health check."""
    try:
        health_check = FlextHealthCheck(
            name=name,
            status=status,
            details=details or {},
        )
        return FlextResult[FlextHealthCheck].ok(health_check)
    except Exception as e:
        return FlextResult[FlextHealthCheck].fail(f"Health check creation failed: {e}")


__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityEntry",
    "FlextObservabilityServices",
    "FlextObservabilityUtilities",
    "FlextTrace",
    "__version__",
    "__version_info__",
    "flext_create_alert",
    "flext_create_entry",
    "flext_create_health_check",
    "flext_create_metric",
    "flext_create_trace",
    "flext_monitor_function",
]
