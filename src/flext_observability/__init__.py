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

import math
from datetime import UTC, datetime
from typing import ClassVar, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from flext import FlextContainer, FlextLogger, FlextResult
from flext_observability.__version__ import __version__, __version_info__


class FlextObservability:
    """Main observability class - single Flext[Project] class pattern.

    Provides unified observability for the FLEXT ecosystem with complete
    separation of concerns and SOLID principles.

    Architecture layers:
    - Layer 0: Constants and enumerations
    - Layer 1: Domain entities (Metric, Trace, Alert, HealthCheck, LogEntry)
    - Layer 2: Application services (MetricsService, TracingService, etc.)
    - Layer 3: Infrastructure and factories
    """

    # ========================================================================
    # LAYER 0: DOMAIN CONSTANTS
    # ========================================================================

    class Constants:
        """Domain constants and enumerations."""

        METRIC_TYPES: ClassVar[set[str]] = {"counter", "gauge", "histogram"}
        TRACE_STATUSES: ClassVar[set[str]] = {"unset", "ok", "error"}
        ALERT_SEVERITIES: ClassVar[set[str]] = {"info", "warning", "error", "critical"}
        ALERT_STATUSES: ClassVar[set[str]] = {"firing", "resolved"}
        HEALTH_STATUSES: ClassVar[set[str]] = {"healthy", "degraded", "unhealthy"}
        LOG_LEVELS: ClassVar[set[str]] = {
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        }

    # ========================================================================
    # LAYER 1: DOMAIN ENTITIES (PYDANTIC MODELS)
    # ========================================================================

    class Metric(BaseModel):
        """Observability metric entity - immutable value object."""

        model_config = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        name: str = Field(description="Metric name")
        value: float = Field(description="Metric value")
        unit: str = Field(default="count")
        metric_type: Literal["counter", "gauge", "histogram"] = Field(default="gauge")
        labels: dict[str, str] = Field(default_factory=dict)
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    class Trace(BaseModel):
        """Distributed trace span entity."""

        model_config = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        name: str = Field(description="Span name")
        trace_id: str = Field(default_factory=lambda: str(uuid4()))
        parent_span_id: str | None = Field(default=None)
        status: Literal["unset", "ok", "error"] = Field(default="unset")
        attributes: dict[str, str] = Field(default_factory=dict)
        start_time: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
        end_time: datetime | None = Field(default=None)
        duration_ms: float | None = Field(default=None)
        error_message: str | None = Field(default=None)

    class Alert(BaseModel):
        """Alert entity - immutable alert definition."""

        model_config = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        title: str = Field(default="", description="Alert title")
        message: str = Field(description="Alert message")
        severity: Literal["info", "warning", "error", "critical"] = Field(
            default="warning",
        )
        source: str = Field(default="system")
        labels: dict[str, str] = Field(default_factory=dict)
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    class HealthCheck(BaseModel):
        """Health check status entity."""

        model_config = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        component: str = Field(description="Component name")
        status: Literal["healthy", "degraded", "unhealthy"] = Field(default="healthy")
        details: dict[str, object] = Field(default_factory=dict)
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    class LogEntry(BaseModel):
        """Log entry entity."""

        model_config = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        message: str = Field(description="Log message")
        level: Literal["debug", "info", "warning", "error", "critical"] = Field(
            default="info",
        )
        component: str = Field(default="application")
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
        context: dict[str, object] = Field(default_factory=dict)

    # ========================================================================
    # LAYER 2: APPLICATION SERVICES
    # ========================================================================

    class MetricsService:
        """Service for metrics collection and recording.

        Single Responsibility: Handle all metric operations
        Dependency Inversion: Uses FlextResult pattern for error handling
        """

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextLogger(__name__)
            self._metrics: list[FlextObservability.Metric] = []

        def record_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            labels: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservability.Metric]:
            """Record a metric with validation."""
            try:
                if not name or not isinstance(name, str):
                    return FlextResult[FlextObservability.Metric].fail(
                        "Metric name must be non-empty string",
                    )
                if not isinstance(value, (int, float)) or math.isnan(float(value)):
                    return FlextResult[FlextObservability.Metric].fail(
                        "Metric value must be a valid number",
                    )

                # Auto-detect metric type from name
                metric_type: Literal["counter", "gauge", "histogram"] = "gauge"
                if name.endswith(("_total", "_count")):
                    metric_type = "counter"
                elif name.endswith(("_duration", "_seconds")):
                    metric_type = "histogram"

                metric = FlextObservability.Metric(
                    name=name,
                    value=float(value),
                    unit=unit,
                    metric_type=metric_type,
                    labels=labels or {},
                )
                self._metrics.append(metric)
                return FlextResult[FlextObservability.Metric].ok(metric)
            except (
                ValueError,
                TypeError,
                AttributeError,
            ) as e:
                self._logger.warning("Metric recording failed: %s", e, exc_info=True)
                return FlextResult[FlextObservability.Metric].fail(
                    f"Metric recording failed: {e}",
                )

    class TracingService:
        """Service for distributed tracing."""

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextLogger(__name__)
            self._traces: list[FlextObservability.Trace] = []

        def start_trace(
            self,
            name: str,
            attributes: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservability.Trace]:
            """Start a distributed trace."""
            try:
                if not name or not isinstance(name, str):
                    return FlextResult[FlextObservability.Trace].fail(
                        "Trace name must be non-empty string",
                    )

                trace = FlextObservability.Trace(
                    name=name,
                    attributes=attributes or {},
                )
                self._traces.append(trace)
                return FlextResult[FlextObservability.Trace].ok(trace)
            except (
                ValueError,
                TypeError,
                AttributeError,
            ) as e:
                self._logger.warning("Trace creation failed: %s", e, exc_info=True)
                return FlextResult[FlextObservability.Trace].fail(
                    f"Trace creation failed: {e}",
                )

    class AlertingService:
        """Service for alert management."""

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextLogger(__name__)
            self._alerts: list[FlextObservability.Alert] = []

        def create_alert(
            self,
            title: str,
            message: str,
            severity: Literal["info", "warning", "error", "critical"] = ("warning"),
            source: str = "system",
            labels: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservability.Alert]:
            """Create an alert with validation."""
            try:
                if not title or not isinstance(title, str):
                    return FlextResult[FlextObservability.Alert].fail(
                        "Alert title cannot be empty",
                    )
                if not message or not isinstance(message, str):
                    return FlextResult[FlextObservability.Alert].fail(
                        "Alert message cannot be empty",
                    )

                alert = FlextObservability.Alert(
                    title=title,
                    message=message,
                    severity=severity,
                    source=source,
                    labels=labels or {},
                )
                self._alerts.append(alert)
                return FlextResult[FlextObservability.Alert].ok(alert)
            except (
                ValueError,
                TypeError,
                AttributeError,
            ) as e:
                self._logger.warning("Alert creation failed: %s", e, exc_info=True)
                return FlextResult[FlextObservability.Alert].fail(
                    f"Alert creation failed: {e}",
                )

    class HealthService:
        """Service for health check management."""

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextLogger(__name__)
            self._checks: list[FlextObservability.HealthCheck] = []

        def check_component(
            self,
            component: str,
            status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
            details: dict[str, object] | None = None,
        ) -> FlextResult[FlextObservability.HealthCheck]:
            """Create a health check."""
            try:
                if not component or not isinstance(component, str):
                    return FlextResult[FlextObservability.HealthCheck].fail(
                        "Component name cannot be empty",
                    )
                if status not in {
                    "healthy",
                    "degraded",
                    "unhealthy",
                }:
                    return FlextResult[FlextObservability.HealthCheck].fail(
                        f"Invalid health status: {status}",
                    )

                health = FlextObservability.HealthCheck(
                    component=component,
                    status=status,
                    details=details or {},
                )
                self._checks.append(health)
                return FlextResult[FlextObservability.HealthCheck].ok(health)
            except (
                ValueError,
                TypeError,
                AttributeError,
            ) as e:
                self._logger.warning("Health check failed: %s", e, exc_info=True)
                return FlextResult[FlextObservability.HealthCheck].fail(
                    f"Health check failed: {e}",
                )

    class LoggingService:
        """Service for structured logging."""

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextLogger(__name__)
            self._entries: list[FlextObservability.LogEntry] = []

        def log_entry(
            self,
            message: str,
            level: Literal["debug", "info", "warning", "error", "critical"] = "info",
            component: str = "application",
            context: dict[str, object] | None = None,
        ) -> FlextResult[FlextObservability.LogEntry]:
            """Create a log entry."""
            try:
                if not message or not isinstance(message, str):
                    return FlextResult[FlextObservability.LogEntry].fail(
                        "Log message cannot be empty",
                    )

                entry = FlextObservability.LogEntry(
                    message=message,
                    level=level,
                    component=component,
                    context=context or {},
                )
                self._entries.append(entry)
                return FlextResult[FlextObservability.LogEntry].ok(entry)
            except (
                ValueError,
                TypeError,
                AttributeError,
            ) as e:
                self._logger.warning("Log entry creation failed: %s", e, exc_info=True)
                return FlextResult[FlextObservability.LogEntry].fail(
                    f"Log entry creation failed: {e}",
                )


# ============================================================================
# LAYER 3: FACTORY FUNCTIONS (SIMPLE API)
# ============================================================================


def flext_metric(
    name: str,
    value: float,
    unit: str = "count",
    metric_type: Literal["counter", "gauge", "histogram"] | None = None,
    metric_id: str | None = None,
    tags: dict[str, str] | None = None,
    labels: dict[str, str] | None = None,
) -> FlextResult[FlextObservability.Metric]:
    """Create a metric entity directly."""
    # metric_id parameter reserved for future use
    _ = metric_id
    try:
        if not name or not isinstance(name, str):
            return FlextResult[FlextObservability.Metric].fail(
                "Metric name must be non-empty string",
            )
        if not isinstance(value, (int, float)) or math.isnan(float(value)):
            return FlextResult[FlextObservability.Metric].fail(
                "Metric value must be a valid number",
            )

        all_labels = {**(tags or {}), **(labels or {})}

        detected_type: Literal["counter", "gauge", "histogram"] = metric_type or "gauge"
        if not metric_type:
            if name.endswith(("_total", "_count")):
                detected_type = "counter"
            elif name.endswith(("_duration", "_seconds")):
                detected_type = "histogram"

        metric = FlextObservability.Metric(
            id=metric_id or str(uuid4()),
            name=name,
            value=float(value),
            unit=unit,
            metric_type=detected_type,
            labels=all_labels,
        )
        return FlextResult[FlextObservability.Metric].ok(metric)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult[FlextObservability.Metric].fail(
            f"Metric creation failed: {e}",
        )


def flext_trace(
    name: str,
    attributes: dict[str, str] | None = None,
    trace_id: str | None = None,
) -> FlextResult[FlextObservability.Trace]:
    """Create a trace entity directly."""
    try:
        if not name or not isinstance(name, str):
            return FlextResult[FlextObservability.Trace].fail(
                "Trace name must be non-empty string",
            )

        trace = FlextObservability.Trace(
            name=name,
            trace_id=trace_id or str(uuid4()),
            attributes=attributes or {},
        )
        return FlextResult[FlextObservability.Trace].ok(trace)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult[FlextObservability.Trace].fail(f"Trace creation failed: {e}")


def flext_alert(
    title: str = "",
    message: str = "",
    severity: Literal["info", "warning", "error", "critical"] = "warning",
    status: Literal["firing", "resolved"] = "firing",
    alert_id: str | None = None,
    source: str = "system",
    labels: dict[str, str] | None = None,
) -> FlextResult[FlextObservability.Alert]:
    """Create an alert entity directly."""
    # Reserved for future status-based alert handling
    _ = status  # Reserved for future use

    try:
        if not message and not title:
            return FlextResult[FlextObservability.Alert].fail(
                "Alert message cannot be empty",
            )
        if not title and message:
            return FlextResult[FlextObservability.Alert].fail(
                "Alert title cannot be empty",
            )

        alert = FlextObservability.Alert(
            id=alert_id or str(uuid4()),
            title=title,
            message=message,
            severity=severity,
            source=source,
            labels=labels or {},
        )
        return FlextResult[FlextObservability.Alert].ok(alert)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult[FlextObservability.Alert].fail(f"Alert creation failed: {e}")


def flext_health_check(
    component: str,
    status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
    health_check_id: str | None = None,
    details: dict[str, object] | None = None,
) -> FlextResult[FlextObservability.HealthCheck]:
    """Create a health check entity directly."""
    # health_check_id parameter reserved for future use
    _ = health_check_id
    try:
        if not component or not isinstance(component, str):
            return FlextResult[FlextObservability.HealthCheck].fail(
                "Component name cannot be empty",
            )
        if status not in {"healthy", "degraded", "unhealthy"}:
            return FlextResult[FlextObservability.HealthCheck].fail(
                f"Invalid health status: {status}",
            )

        health = FlextObservability.HealthCheck(
            id=health_check_id or str(uuid4()),
            component=component,
            status=status,
            details=details or {},
        )
        return FlextResult[FlextObservability.HealthCheck].ok(health)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult[FlextObservability.HealthCheck].fail(
            f"Health check creation failed: {e}",
        )


def flext_create_health_check(
    component: str,
    status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
    health_check_id: str | None = None,
    details: dict[str, object] | None = None,
) -> FlextResult[FlextObservability.HealthCheck]:
    """Create a health check (alias for compatibility)."""
    return flext_health_check(
        component=component,
        status=status,
        health_check_id=health_check_id,
        details=details,
    )


def flext_log_entry(
    message: str,
    level: Literal["debug", "info", "warning", "error", "critical"] = "info",
    component: str = "application",
    timestamp: datetime | None = None,
    context: dict[str, object] | None = None,
) -> FlextResult[FlextObservability.LogEntry]:
    """Create a log entry entity directly."""
    try:
        if not message or not isinstance(message, str):
            return FlextResult[FlextObservability.LogEntry].fail(
                "Log message cannot be empty",
            )

        entry = FlextObservability.LogEntry(
            id=str(uuid4()),
            message=message,
            level=level,
            component=component,
            timestamp=timestamp or datetime.now(tz=UTC),
            context=context or {},
        )
        return FlextResult[FlextObservability.LogEntry].ok(entry)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult[FlextObservability.LogEntry].fail(
            f"Log entry creation failed: {e}",
        )


# ============================================================================
# MODULE EXPORTS AND COMPATIBILITY ALIASES
# ============================================================================


# Top-level entity classes with real inheritance for test compatibility
class FlextMetric(FlextObservability.Metric):
    """FlextMetric - real inheritance from FlextObservability.Metric."""


class FlextTrace(FlextObservability.Trace):
    """FlextTrace - real inheritance from FlextObservability.Trace."""


class FlextAlert(FlextObservability.Alert):
    """FlextAlert - real inheritance from FlextObservability.Alert."""


class FlextHealthCheck(FlextObservability.HealthCheck):
    """FlextHealthCheck - real inheritance from FlextObservability.HealthCheck."""


class FlextLogEntry(FlextObservability.LogEntry):
    """FlextLogEntry - real inheritance from FlextObservability.LogEntry."""


# Factory function aliases for backward compatibility
flext_create_metric = flext_metric
flext_create_trace = flext_trace
flext_create_alert = flext_alert
flext_create_log_entry = flext_log_entry

__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextObservability",
    "FlextTrace",
    "__version__",
    "__version_info__",
    "flext_alert",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    "flext_log_entry",
    "flext_metric",
    "flext_trace",
]
