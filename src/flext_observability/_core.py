"""Core FlextObservability class and factory functions.

Internal module; use flext_observability package API.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import ClassVar, Literal
from uuid import uuid4

from flext_core import FlextContainer, FlextRuntime, r
from flext_core.protocols import FlextProtocols as p
from flext_core.typings import t

from flext_observability.constants import FlextObservabilityConstants as c
from flext_observability.models import FlextObservabilityModels as _m


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

    class Constants:
        """Domain constants and enumerations."""

        METRIC_TYPES: ClassVar[set[str]] = {
            c.Observability.MetricType.COUNTER,
            c.Observability.MetricType.GAUGE,
            c.Observability.MetricType.HISTOGRAM,
        }
        TRACE_STATUSES: ClassVar[set[str]] = {
            c.Observability.TraceStatus.UNSET,
            c.Observability.TraceStatus.OK,
            c.Observability.TraceStatus.ERROR,
        }
        ALERT_SEVERITIES: ClassVar[set[str]] = set(c.Observability.AlertSeverity)
        ALERT_STATUSES: ClassVar[set[str]] = set(c.Observability.AlertStatus)
        HEALTH_STATUSES: ClassVar[set[str]] = set(c.Observability.HealthStatus)
        LOG_LEVELS: ClassVar[set[str]] = {
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        }

    # Model classes live in models.py — aliases kept here for backward compatibility
    Metric = _m.Observability.Metric
    Trace = _m.Observability.Trace
    Alert = _m.Observability.Alert
    HealthCheck = _m.Observability.HealthCheck
    LogEntry = _m.Observability.LogEntry

    class MetricsService:
        """Service for metrics collection and recording.

        Single Responsibility: Handle all metric operations
        Dependency Inversion: Uses r pattern for error handling
        """

        _container: p.Container
        _logger: p.Logger
        _metrics: list[FlextObservability.Metric]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextRuntime.get_logger(__name__)
            self._metrics = []

        def record_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            labels: dict[str, t.Scalar] | None = None,
        ) -> r[FlextObservability.Metric]:
            """Record a metric with validation."""
            try:
                if not name:
                    return r[FlextObservability.Metric].fail(
                        "Metric name must be non-empty string",
                    )
                if math.isnan(float(value)):
                    return r[FlextObservability.Metric].fail(
                        "Metric value must be a valid number",
                    )
                metric_type: c.Observability.MetricType = (
                    c.Observability.MetricType.GAUGE
                )
                if name.endswith(("_total", "_count")):
                    metric_type = c.Observability.MetricType.COUNTER
                elif name.endswith(("_duration", "_seconds")):
                    metric_type = c.Observability.MetricType.HISTOGRAM
                metric = FlextObservability.Metric(
                    id=str(uuid4()),
                    name=name,
                    value=float(value),
                    unit=unit,
                    metric_type=metric_type,
                    labels=labels or {},
                    domain_events=[],
                )
                self._metrics.append(metric)
                return r[FlextObservability.Metric].ok(metric)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(f"Metric recording failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Metric].fail(
                    f"Metric recording failed: {e}",
                )

    class TracingService:
        """Service for distributed tracing."""

        _container: p.Container
        _logger: p.Logger
        _traces: list[FlextObservability.Trace]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextRuntime.get_logger(__name__)
            self._traces = []

        def start_trace(
            self,
            name: str,
            attributes: dict[str, t.Scalar] | None = None,
        ) -> r[FlextObservability.Trace]:
            """Start a distributed trace."""
            try:
                if not name:
                    return r[FlextObservability.Trace].fail(
                        "Trace name must be non-empty string",
                    )
                trace = FlextObservability.Trace(
                    trace_id=str(uuid4()),
                    name=name,
                    attributes=attributes or {},
                    domain_events=[],
                )
                self._traces.append(trace)
                return r[FlextObservability.Trace].ok(trace)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(f"Trace creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Trace].fail(f"Trace creation failed: {e}")

    class AlertingService:
        """Service for alert management."""

        _container: p.Container
        _logger: p.Logger
        _alerts: list[FlextObservability.Alert]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextRuntime.get_logger(__name__)
            self._alerts = []

        def create_alert(
            self,
            title: str,
            message: str,
            severity: Literal["info", "warning", "error", "critical"] = "warning",
            source: str = "system",
            labels: dict[str, t.Scalar] | None = None,
        ) -> r[FlextObservability.Alert]:
            """Create an alert with validation."""
            try:
                if not title:
                    return r[FlextObservability.Alert].fail(
                        "Alert title cannot be empty",
                    )
                if not message:
                    return r[FlextObservability.Alert].fail(
                        "Alert message cannot be empty",
                    )
                alert = FlextObservability.Alert(
                    id=str(uuid4()),
                    title=title,
                    message=message,
                    severity=severity,
                    source=source,
                    labels=labels or {},
                    domain_events=[],
                )
                self._alerts.append(alert)
                return r[FlextObservability.Alert].ok(alert)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(f"Alert creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Alert].fail(f"Alert creation failed: {e}")

    class HealthService:
        """Service for health check management."""

        _container: p.Container
        _logger: p.Logger
        _checks: list[FlextObservability.HealthCheck]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextRuntime.get_logger(__name__)
            self._checks = []

        def check_component(
            self,
            component: str,
            status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
            details: dict[str, t.Scalar] | None = None,
        ) -> r[FlextObservability.HealthCheck]:
            """Create a health check."""
            try:
                if not component:
                    return r[FlextObservability.HealthCheck].fail(
                        "Component name cannot be empty",
                    )
                if status not in FlextObservability.Constants.HEALTH_STATUSES:
                    return r[FlextObservability.HealthCheck].fail(
                        f"Invalid health status: {status}",
                    )
                health = FlextObservability.HealthCheck(
                    id=str(uuid4()),
                    component=component,
                    status=status,
                    details=details or {},
                    domain_events=[],
                )
                self._checks.append(health)
                return r[FlextObservability.HealthCheck].ok(health)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(f"Health check failed: %s: {e}", exc_info=True)
                return r[FlextObservability.HealthCheck].fail(
                    f"Health check failed: {e}",
                )

    class LoggingService:
        """Service for structured logging."""

        _container: p.Container
        _logger: p.Logger
        _entries: list[FlextObservability.LogEntry]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextContainer.get_global()
            self._logger = FlextRuntime.get_logger(__name__)
            self._entries = []

        def log_entry(
            self,
            message: str,
            level: Literal["debug", "info", "warning", "error", "critical"] = "info",
            component: str = "application",
            context: dict[str, t.Scalar] | None = None,
        ) -> r[FlextObservability.LogEntry]:
            """Create a log entry."""
            try:
                if not message:
                    return r[FlextObservability.LogEntry].fail(
                        "Log message cannot be empty",
                    )
                entry = FlextObservability.LogEntry(
                    id=str(uuid4()),
                    message=message,
                    level=level,
                    component=component,
                    timestamp=datetime.now(tz=UTC),
                    context=context or {},
                    domain_events=[],
                )
                self._entries.append(entry)
                return r[FlextObservability.LogEntry].ok(entry)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(
                    f"Log entry creation failed: %s: {e}",
                    exc_info=True,
                )
                return r[FlextObservability.LogEntry].fail(
                    f"Log entry creation failed: {e}",
                )


def flext_metric(
    name: str,
    value: float,
    unit: str = "count",
    metric_type: c.Observability.MetricType | None = None,
    metric_id: str | None = None,
    tags: dict[str, t.Scalar] | None = None,
    labels: dict[str, t.Scalar] | None = None,
) -> r[FlextObservability.Metric]:
    """Create a metric entity directly."""
    _ = metric_id
    try:
        if not name:
            return r[FlextObservability.Metric].fail(
                "Metric name must be non-empty string",
            )
        if math.isnan(float(value)):
            return r[FlextObservability.Metric].fail(
                "Metric value must be a valid number",
            )
        all_labels_data: dict[str, t.Scalar] = {}
        if tags:
            all_labels_data.update(tags)
        if labels:
            all_labels_data.update(labels)
        all_labels: dict[str, t.Scalar] = all_labels_data
        detected_type: c.Observability.MetricType = (
            metric_type or c.Observability.MetricType.GAUGE
        )
        if not metric_type:
            if name.endswith(("_total", "_count")):
                detected_type = c.Observability.MetricType.COUNTER
            elif name.endswith(("_duration", "_seconds")):
                detected_type = c.Observability.MetricType.HISTOGRAM
        metric = FlextObservability.Metric(
            id=metric_id or str(uuid4()),
            name=name,
            value=float(value),
            unit=unit,
            metric_type=detected_type,
            labels=all_labels,
            domain_events=[],
        )
        return r[FlextObservability.Metric].ok(metric)
    except (ValueError, TypeError, AttributeError) as e:
        return r[FlextObservability.Metric].fail(f"Metric creation failed: {e}")


def flext_trace(
    name: str,
    attributes: dict[str, t.Scalar] | None = None,
    trace_id: str | None = None,
) -> r[FlextObservability.Trace]:
    """Create a trace entity directly."""
    try:
        if not name:
            return r[FlextObservability.Trace].fail(
                "Trace name must be non-empty string",
            )
        trace = FlextObservability.Trace(
            name=name,
            trace_id=trace_id or str(uuid4()),
            attributes=attributes or {},
            domain_events=[],
        )
        return r[FlextObservability.Trace].ok(trace)
    except (ValueError, TypeError, AttributeError) as e:
        return r[FlextObservability.Trace].fail(f"Trace creation failed: {e}")


def flext_alert(
    title: str = "",
    message: str = "",
    severity: Literal["info", "warning", "error", "critical"] = "warning",
    status: Literal["firing", "resolved"] = "firing",
    alert_id: str | None = None,
    source: str = "system",
    labels: dict[str, t.Scalar] | None = None,
) -> r[FlextObservability.Alert]:
    """Create an alert entity directly."""
    _ = status
    try:
        if not message and (not title):
            return r[FlextObservability.Alert].fail("Alert message cannot be empty")
        if not title and message:
            return r[FlextObservability.Alert].fail("Alert title cannot be empty")
        alert = FlextObservability.Alert(
            id=alert_id or str(uuid4()),
            title=title,
            message=message,
            severity=severity,
            source=source,
            labels=labels or {},
            domain_events=[],
        )
        return r[FlextObservability.Alert].ok(alert)
    except (ValueError, TypeError, AttributeError) as e:
        return r[FlextObservability.Alert].fail(f"Alert creation failed: {e}")


def flext_health_check(
    component: str,
    status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
    health_check_id: str | None = None,
    details: dict[str, t.Scalar] | None = None,
) -> r[FlextObservability.HealthCheck]:
    """Create a health check entity directly."""
    _ = health_check_id
    try:
        if not component:
            return r[FlextObservability.HealthCheck].fail(
                "Component name cannot be empty",
            )
        if status not in FlextObservability.Constants.HEALTH_STATUSES:
            return r[FlextObservability.HealthCheck].fail(
                f"Invalid health status: {status}",
            )
        health = FlextObservability.HealthCheck(
            id=health_check_id or str(uuid4()),
            component=component,
            status=status,
            details=details or {},
            domain_events=[],
        )
        return r[FlextObservability.HealthCheck].ok(health)
    except (ValueError, TypeError, AttributeError) as e:
        return r[FlextObservability.HealthCheck].fail(
            f"Health check creation failed: {e}",
        )


def flext_log_entry(
    message: str,
    level: Literal["debug", "info", "warning", "error", "critical"] = "info",
    component: str = "application",
    timestamp: datetime | None = None,
    context: dict[str, t.Scalar] | None = None,
) -> r[FlextObservability.LogEntry]:
    """Create a log entry entity directly."""
    try:
        if not message:
            return r[FlextObservability.LogEntry].fail("Log message cannot be empty")
        entry = FlextObservability.LogEntry(
            id=str(uuid4()),
            message=message,
            level=level,
            component=component,
            timestamp=timestamp or datetime.now(tz=UTC),
            context=context or {},
            domain_events=[],
        )
        return r[FlextObservability.LogEntry].ok(entry)
    except (ValueError, TypeError, AttributeError) as e:
        return r[FlextObservability.LogEntry].fail(f"Log entry creation failed: {e}")


class _GlobalFactoryState:
    factory: FlextObservabilityMasterFactory | None = None


_global_factory_state = _GlobalFactoryState()


class FlextObservabilityMasterFactory:
    """Master factory for creating observability entities."""

    _container: p.Container
    _metrics_service: FlextObservability.MetricsService
    _tracing_service: FlextObservability.TracingService
    _alerting_service: FlextObservability.AlertingService
    _health_service: FlextObservability.HealthService
    _logging_service: FlextObservability.LoggingService

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize factory with optional container."""
        self._container = container or FlextContainer.get_global()
        self._metrics_service = FlextObservability.MetricsService(self._container)
        self._tracing_service = FlextObservability.TracingService(self._container)
        self._alerting_service = FlextObservability.AlertingService(self._container)
        self._health_service = FlextObservability.HealthService(self._container)
        self._logging_service = FlextObservability.LoggingService(self._container)

    @property
    def container(self) -> p.Container:
        """Return the container."""
        return self._container

    def alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        tags: dict[str, t.Scalar] | None = None,
        status: str = c.Observability.AlertStatus.FIRING,
        timestamp: datetime | None = None,
    ) -> r[FlextObservability.Alert]:
        """Create an alert."""
        _ = timestamp
        valid_severity: Literal["info", "warning", "error", "critical"]
        match severity:
            case "info" | "low":
                valid_severity = "info"
            case "warning" | "medium":
                valid_severity = "warning"
            case "error" | "high":
                valid_severity = "error"
            case "critical":
                valid_severity = "critical"
            case _:
                valid_severity = "warning"
        valid_status: Literal["firing", "resolved"]
        match status:
            case "firing" | "active":
                valid_status = "firing"
            case "resolved":
                valid_status = "resolved"
            case _:
                valid_status = "firing"
        return flext_alert(
            title=title,
            message=message,
            severity=valid_severity,
            status=valid_status,
            labels=tags,
        )

    def create_alert(
        self,
        message: str,
        service: str = "default",
        severity: str = "warning",
        tags: dict[str, t.Scalar] | None = None,
    ) -> r[FlextObservability.Alert]:
        """Create an alert (alias)."""
        return self.alert(f"Alert: {service}", message, severity=severity, tags=tags)

    def create_health_check(
        self,
        component: str,
        status: str = c.Observability.HealthStatus.HEALTHY,
        details: dict[str, t.Scalar] | None = None,
    ) -> r[FlextObservability.HealthCheck]:
        """Create a health check (alias)."""
        return self.health_check(component, status=status, metrics=details)

    def create_log_entry(
        self,
        message: str,
        level: str = "info",
        context: dict[str, t.Scalar] | None = None,
    ) -> r[FlextObservability.LogEntry]:
        """Create a log entry (alias)."""
        return self.log(message, level=level, context=context)

    def create_metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        tags: dict[str, t.Scalar] | None = None,
    ) -> r[FlextObservability.Metric]:
        """Create a metric (alias)."""
        return self.metric(name, value, unit=unit, tags=tags)

    def create_trace(
        self,
        operation: str,
        service: str = "default",
        tags: dict[str, t.Scalar] | None = None,
    ) -> r[FlextObservability.Trace]:
        """Create a trace (alias)."""
        attrs: dict[str, t.Scalar] | None = None
        if tags is not None:
            attrs = dict(tags.items())
        return self.trace(f"trace-{service}", operation, span_attributes=attrs)

    def health_check(
        self,
        component: str,
        status: str = c.Observability.HealthStatus.HEALTHY,
        message: str | None = None,
        metrics: dict[str, t.Scalar] | None = None,
        timestamp: datetime | None = None,
    ) -> r[FlextObservability.HealthCheck]:
        """Create a health check."""
        _ = timestamp
        _ = message
        valid_status: Literal["healthy", "degraded", "unhealthy"]
        match status:
            case "healthy":
                valid_status = "healthy"
            case "degraded":
                valid_status = "degraded"
            case "unhealthy":
                valid_status = "unhealthy"
            case _:
                valid_status = "healthy"
        return flext_health_check(component, status=valid_status, details=metrics)

    def health_status(self) -> r[FlextObservability.HealthCheck]:
        """Get overall health status."""
        return flext_health_check("system", status="healthy")

    def log(
        self,
        message: str,
        level: str = c.Observability.ErrorSeverity.INFO,
        context: dict[str, t.Scalar] | None = None,
        timestamp: datetime | None = None,
    ) -> r[FlextObservability.LogEntry]:
        """Create a log entry."""
        valid_level: Literal["debug", "info", "warning", "error", "critical"]
        match level:
            case "debug":
                valid_level = "debug"
            case "info":
                valid_level = "info"
            case "warning":
                valid_level = "warning"
            case "error":
                valid_level = "error"
            case "critical":
                valid_level = "critical"
            case _:
                valid_level = "info"
        return flext_log_entry(
            message,
            level=valid_level,
            context=context,
            timestamp=timestamp,
        )

    def metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        tags: dict[str, t.Scalar] | None = None,
        timestamp: datetime | None = None,
    ) -> r[FlextObservability.Metric]:
        """Create a metric."""
        _ = timestamp
        return flext_metric(name, value, unit=unit, tags=tags)

    def trace(
        self,
        trace_id: str,
        operation: str,
        span_id: str | None = None,
        span_attributes: dict[str, t.Scalar] | None = None,
        duration_ms: float | None = None,
        status: str = "unset",
    ) -> r[FlextObservability.Trace]:
        """Create a trace span."""
        _ = span_id
        _ = duration_ms
        _ = status
        str_attributes: dict[str, t.Scalar] = {}
        if span_attributes:
            str_attributes = {k: str(v) for k, v in span_attributes.items()}
        return flext_trace(operation, attributes=str_attributes, trace_id=trace_id)


def get_global_factory() -> FlextObservabilityMasterFactory:
    """Get or create the global factory instance."""
    if _global_factory_state.factory is None:
        _global_factory_state.factory = FlextObservabilityMasterFactory()
    return _global_factory_state.factory


def reset_global_factory() -> None:
    """Reset the global factory instance."""
    _global_factory_state.factory = None
