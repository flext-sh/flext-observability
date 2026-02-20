"""Core FlextObservability class and factory functions.

Internal module; use flext_observability package API.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import ClassVar, Literal, cast
from uuid import uuid4

from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextLogger,
    FlextProtocols as p,
    FlextResult,
    FlextTypes as t,
)
from pydantic import BaseModel, ConfigDict, Field


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

        model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        name: str = Field(description="Metric name")
        value: float = Field(description="Metric value")
        unit: str = Field(default="count")
        metric_type: Literal["counter", "gauge", "histogram"] = Field(default="gauge")
        labels: dict[str, str] = Field(default_factory=dict)
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    class Trace(BaseModel):
        """Distributed trace span entity."""

        model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)

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

        model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)

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

        model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        component: str = Field(description="Component name")
        status: Literal["healthy", "degraded", "unhealthy"] = Field(default="healthy")
        details: dict[str, t.GeneralValueType] = Field(default_factory=dict)
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    class LogEntry(BaseModel):
        """Log entry entity."""

        model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)

        id: str = Field(default_factory=lambda: str(uuid4()))
        message: str = Field(description="Log message")
        level: Literal["debug", "info", "warning", "error", "critical"] = Field(
            default="info",
        )
        component: str = Field(default="application")
        timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
        context: dict[str, t.GeneralValueType] = Field(default_factory=dict)

    # ========================================================================
    # LAYER 2: APPLICATION SERVICES
    # ========================================================================

    class MetricsService:
        """Service for metrics collection and recording.

        Single Responsibility: Handle all metric operations
        Dependency Inversion: Uses FlextResult pattern for error handling
        """

        _container: FlextContainer
        _logger: p.Log.StructlogLogger
        _metrics: list[FlextObservability.Metric]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextContainer.get_global()
            self._logger = cast(
                "p.Log.StructlogLogger",
                FlextLogger.get_logger(__name__),
            )
            self._metrics = []

        def record_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            labels: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservability.Metric]:
            """Record a metric with validation."""
            try:
                if not name:
                    return FlextResult[FlextObservability.Metric].fail(
                        "Metric name must be non-empty string",
                    )
                if math.isnan(float(value)):
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
                self._logger.warning(f"Metric recording failed: {e}", exc_info=True)
                return FlextResult[FlextObservability.Metric].fail(
                    f"Metric recording failed: {e}",
                )

    class TracingService:
        """Service for distributed tracing."""

        _container: FlextContainer
        _logger: p.Log.StructlogLogger
        _traces: list[FlextObservability.Trace]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextContainer.get_global()
            self._logger = cast(
                "p.Log.StructlogLogger",
                FlextLogger.get_logger(__name__),
            )
            self._traces = []

        def start_trace(
            self,
            name: str,
            attributes: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservability.Trace]:
            """Start a distributed trace."""
            try:
                if not name:
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
                self._logger.warning(f"Trace creation failed: {e}", exc_info=True)
                return FlextResult[FlextObservability.Trace].fail(
                    f"Trace creation failed: {e}",
                )

    class AlertingService:
        """Service for alert management."""

        _container: FlextContainer
        _logger: p.Log.StructlogLogger
        _alerts: list[FlextObservability.Alert]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextContainer.get_global()
            self._logger = cast(
                "p.Log.StructlogLogger",
                FlextLogger.get_logger(__name__),
            )
            self._alerts = []

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
                if not title:
                    return FlextResult[FlextObservability.Alert].fail(
                        "Alert title cannot be empty",
                    )
                if not message:
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
                self._logger.warning(f"Alert creation failed: {e}", exc_info=True)
                return FlextResult[FlextObservability.Alert].fail(
                    f"Alert creation failed: {e}",
                )

    class HealthService:
        """Service for health check management."""

        _container: FlextContainer
        _logger: p.Log.StructlogLogger
        _checks: list[FlextObservability.HealthCheck]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextContainer.get_global()
            self._logger = cast(
                "p.Log.StructlogLogger",
                FlextLogger.get_logger(__name__),
            )
            self._checks = []

        def check_component(
            self,
            component: str,
            status: Literal["healthy", "degraded", "unhealthy"] = "healthy",
            details: dict[str, t.GeneralValueType] | None = None,
        ) -> FlextResult[FlextObservability.HealthCheck]:
            """Create a health check."""
            try:
                if not component:
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
                self._logger.warning(f"Health check failed: {e}", exc_info=True)
                return FlextResult[FlextObservability.HealthCheck].fail(
                    f"Health check failed: {e}",
                )

    class LoggingService:
        """Service for structured logging."""

        _container: FlextContainer
        _logger: p.Log.StructlogLogger
        _entries: list[FlextObservability.LogEntry]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextContainer.get_global()
            self._logger = cast(
                "p.Log.StructlogLogger",
                FlextLogger.get_logger(__name__),
            )
            self._entries = []

        def log_entry(
            self,
            message: str,
            level: Literal["debug", "info", "warning", "error", "critical"] = "info",
            component: str = "application",
            context: dict[str, t.GeneralValueType] | None = None,
        ) -> FlextResult[FlextObservability.LogEntry]:
            """Create a log entry."""
            try:
                if not message:
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
                self._logger.warning(f"Log entry creation failed: {e}", exc_info=True)
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
        if not name:
            return FlextResult[FlextObservability.Metric].fail(
                "Metric name must be non-empty string",
            )
        if math.isnan(float(value)):
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
        if not name:
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
    details: dict[str, t.GeneralValueType] | None = None,
) -> FlextResult[FlextObservability.HealthCheck]:
    """Create a health check entity directly."""
    # health_check_id parameter reserved for future use
    _ = health_check_id
    try:
        if not component:
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
    details: dict[str, t.GeneralValueType] | None = None,
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
    context: dict[str, t.GeneralValueType] | None = None,
) -> FlextResult[FlextObservability.LogEntry]:
    """Create a log entry entity directly."""
    try:
        if not message:
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


# ============================================================================
# FLEXT OBSERVABILITY CONSTANTS
# ============================================================================


class FlextObservabilityConstants(FlextConstants):
    """Constants for FLEXT Observability module."""

    # Metric unit constants
    DEFAULT_METRIC_UNIT: ClassVar[str] = "count"
    METRIC_UNIT_COUNT: ClassVar[str] = "count"
    METRIC_UNIT_PERCENT: ClassVar[str] = "percent"
    METRIC_UNIT_BYTES: ClassVar[str] = "bytes"
    METRIC_UNIT_SECONDS: ClassVar[str] = "seconds"

    # Alert level constants
    ALERT_LEVEL_INFO: ClassVar[str] = "info"
    ALERT_LEVEL_WARNING: ClassVar[str] = "warning"
    ALERT_LEVEL_ERROR: ClassVar[str] = "error"
    ALERT_LEVEL_CRITICAL: ClassVar[str] = "critical"

    # Trace status constants
    TRACE_STATUS_STARTED: ClassVar[str] = "started"
    TRACE_STATUS_RUNNING: ClassVar[str] = "running"
    TRACE_STATUS_COMPLETED: ClassVar[str] = "completed"
    TRACE_STATUS_FAILED: ClassVar[str] = "failed"

    # Health status constants
    HEALTH_STATUS_HEALTHY: ClassVar[str] = "healthy"
    HEALTH_STATUS_DEGRADED: ClassVar[str] = "degraded"
    HEALTH_STATUS_UNHEALTHY: ClassVar[str] = "unhealthy"

    # Log level constants
    LOG_LEVEL_DEBUG: ClassVar[str] = "debug"
    LOG_LEVEL_INFO: ClassVar[str] = "info"
    LOG_LEVEL_WARNING: ClassVar[str] = "warning"
    LOG_LEVEL_ERROR: ClassVar[str] = "error"
    LOG_LEVEL_CRITICAL: ClassVar[str] = "critical"

    # Validation constants
    MAX_METRIC_NAME_LENGTH: ClassVar[int] = 256
    MAX_TRACE_NAME_LENGTH: ClassVar[int] = 256
    MAX_ALERT_MESSAGE_LENGTH: ClassVar[int] = 4096
    MAX_LOG_MESSAGE_LENGTH: ClassVar[int] = 8192

    # Service constants
    DEFAULT_SERVICE_NAME: ClassVar[str] = "flext-observability"
    DEFAULT_ENVIRONMENT: ClassVar[str] = "development"
    DEFAULT_HEALTH_CHECK_INTERVAL: ClassVar[int] = 30


# ============================================================================
# FLEXT OBSERVABILITY MASTER FACTORY
# ============================================================================


class _GlobalFactoryState:
    factory: FlextObservabilityMasterFactory | None = None


# Global factory state container
_global_factory_state = _GlobalFactoryState()


class FlextObservabilityMasterFactory:
    """Master factory for creating observability entities."""

    _container: FlextContainer
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
    def container(self) -> FlextContainer:
        """Return the container."""
        return self._container

    def metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        tags: dict[str, str] | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextObservability.Metric]:
        """Create a metric."""
        _ = timestamp  # Reserved for future use
        return flext_metric(name, value, unit=unit, tags=tags)

    def log(
        self,
        message: str,
        level: str = "info",
        context: dict[str, t.GeneralValueType] | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextObservability.LogEntry]:
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
            message, level=valid_level, context=context, timestamp=timestamp
        )

    def alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        tags: dict[str, str] | None = None,
        status: str = "firing",
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextObservability.Alert]:
        """Create an alert."""
        _ = timestamp  # Reserved for future use
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

    def trace(
        self,
        trace_id: str,
        operation: str,
        span_id: str | None = None,
        span_attributes: dict[str, t.GeneralValueType] | None = None,
        duration_ms: float | None = None,
        status: str = "unset",
    ) -> FlextResult[FlextObservability.Trace]:
        """Create a trace span."""
        _ = span_id  # Reserved for future use
        _ = duration_ms  # Reserved for future use
        _ = status  # Reserved for future use
        str_attributes: dict[str, str] = {}
        if span_attributes:
            str_attributes = {k: str(v) for k, v in span_attributes.items()}
        return flext_trace(operation, attributes=str_attributes, trace_id=trace_id)

    def health_check(
        self,
        component: str,
        status: str = "healthy",
        message: str | None = None,
        metrics: dict[str, t.GeneralValueType] | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextObservability.HealthCheck]:
        """Create a health check."""
        _ = timestamp  # Reserved for future use
        _ = message  # Reserved for future use
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

    def health_status(self) -> FlextResult[FlextObservability.HealthCheck]:
        """Get overall health status."""
        return flext_health_check("system", status="healthy")

    def create_metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        tags: dict[str, str] | None = None,
    ) -> FlextResult[FlextObservability.Metric]:
        """Create a metric (alias)."""
        return self.metric(name, value, unit=unit, tags=tags)

    def create_log_entry(
        self,
        message: str,
        level: str = "info",
        context: dict[str, t.GeneralValueType] | None = None,
    ) -> FlextResult[FlextObservability.LogEntry]:
        """Create a log entry (alias)."""
        return self.log(message, level=level, context=context)

    def create_trace(
        self,
        operation: str,
        service: str = "default",
        tags: dict[str, str] | None = None,
    ) -> FlextResult[FlextObservability.Trace]:
        """Create a trace (alias)."""
        attrs: dict[str, t.GeneralValueType] | None = None
        if tags is not None:
            attrs = dict(tags.items())
        return self.trace(f"trace-{service}", operation, span_attributes=attrs)

    def create_alert(
        self,
        message: str,
        service: str = "default",
        severity: str = "warning",
        tags: dict[str, str] | None = None,
    ) -> FlextResult[FlextObservability.Alert]:
        """Create an alert (alias)."""
        return self.alert(f"Alert: {service}", message, severity=severity, tags=tags)

    def create_health_check(
        self,
        component: str,
        status: str = "healthy",
        details: dict[str, t.GeneralValueType] | None = None,
    ) -> FlextResult[FlextObservability.HealthCheck]:
        """Create a health check (alias)."""
        return self.health_check(component, status=status, metrics=details)


def get_global_factory() -> FlextObservabilityMasterFactory:
    """Get or create the global factory instance."""
    if _global_factory_state.factory is None:
        _global_factory_state.factory = FlextObservabilityMasterFactory()
    return _global_factory_state.factory


def reset_global_factory() -> None:
    """Reset the global factory instance."""
    _global_factory_state.factory = None
