"""FlextObservability MRO facade and master factory.

All service methods come from mixins via MRO. Only factory methods,
model aliases, and Constants are defined locally.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
from collections.abc import (
    Mapping,
    MutableSequence,
)
from datetime import UTC, datetime
from typing import ClassVar, TypeAlias
from uuid import uuid4

from flext_core import FlextContainer, u
from flext_observability import (
    FlextObservabilityAdvancedContext,
    FlextObservabilityContext,
    FlextObservabilityCustomMetrics,
    FlextObservabilityErrorHandling,
    FlextObservabilityFields,
    FlextObservabilityHealth,
    FlextObservabilityHTTP,
    FlextObservabilityHTTPClient,
    FlextObservabilityLogging,
    FlextObservabilityMonitor,
    FlextObservabilityPerformance,
    FlextObservabilitySampling,
    FlextObservabilityServices,
    FlextObservabilitySettings,
    c,
    m,
    p,
    r,
    t,
)


class FlextObservability(
    FlextObservabilityAdvancedContext,
    FlextObservabilityContext,
    FlextObservabilityCustomMetrics,
    FlextObservabilityErrorHandling,
    FlextObservabilityFields,
    FlextObservabilityHealth,
    FlextObservabilityHTTP,
    FlextObservabilityHTTPClient,
    FlextObservabilityLogging,
    FlextObservabilityMonitor,
    FlextObservabilityPerformance,
    FlextObservabilitySampling,
    FlextObservabilityServices,
):
    """MRO facade over all observability services.

    All operations come from mixin bases via MRO. Only factory methods,
    model aliases, and Constants are defined locally.
    """

    _settings: FlextObservabilitySettings
    _container: p.Container
    logger: p.Logger = u.fetch_logger(__name__)
    _global_factory: ClassVar[
        FlextObservability.FlextObservabilityMasterFactory | None
    ] = None

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
            c.Observability.ErrorSeverity.DEBUG,
            c.Observability.ErrorSeverity.INFO,
            c.Observability.ErrorSeverity.WARNING,
            c.Observability.ErrorSeverity.ERROR,
            c.Observability.ErrorSeverity.CRITICAL,
        }

    Metric: TypeAlias = m.Observability.Metric
    Trace: TypeAlias = m.Observability.Trace
    Alert: TypeAlias = m.Observability.Alert
    HealthCheck: TypeAlias = m.Observability.HealthCheck
    LogEntry: TypeAlias = m.Observability.LogEntry

    class MetricsService:
        """Service for metrics collection and recording."""

        _container: p.Container
        logger: p.Logger
        _metrics: MutableSequence[FlextObservability.Metric]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextContainer.shared()
            self.logger = u.fetch_logger(__name__)
            self._metrics = list[FlextObservability.Metric]()

        def record_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            labels: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Metric]:
            """Record a metric with validation."""
            try:
                if not name:
                    return r[FlextObservability.Metric].fail_op(
                        "record metric",
                        "Metric name must be non-empty string",
                    )
                if math.isnan(float(value)):
                    return r[FlextObservability.Metric].fail_op(
                        "record metric",
                        "Metric value must be a valid number",
                    )
                metric_type: c.Observability.MetricType = (
                    c.Observability.MetricType.GAUGE
                )
                if name.endswith(("_total", "_count")):
                    metric_type = c.Observability.MetricType.COUNTER
                elif name.endswith(("_duration", "_seconds")):
                    metric_type = c.Observability.MetricType.HISTOGRAM
                resolved_labels: dict[str, t.Scalar] = (
                    dict(labels) if labels is not None else {}
                )
                metric = FlextObservability.Metric(
                    id=str(uuid4()),
                    name=name,
                    value=float(value),
                    unit=unit,
                    metric_type=metric_type,
                    labels=resolved_labels,
                    domain_events=[],
                )
                self._metrics.append(metric)
                return r[FlextObservability.Metric].ok(metric)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.warning(f"Metric recording failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Metric].fail_op("record metric", e)

    class TracingService:
        """Service for distributed tracing."""

        _container: p.Container
        logger: p.Logger
        _traces: MutableSequence[FlextObservability.Trace]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextContainer.shared()
            self.logger = u.fetch_logger(__name__)
            self._traces = list[FlextObservability.Trace]()

        def start_trace(
            self,
            name: str,
            attributes: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Trace]:
            """Start a distributed trace."""
            try:
                if not name:
                    return r[FlextObservability.Trace].fail_op(
                        "start trace",
                        "Trace name must be non-empty string",
                    )
                resolved_attrs: dict[str, t.Scalar] = (
                    dict(attributes) if attributes is not None else {}
                )
                trace = FlextObservability.Trace(
                    trace_id=str(uuid4()),
                    name=name,
                    attributes=resolved_attrs,
                    domain_events=[],
                )
                self._traces.append(trace)
                return r[FlextObservability.Trace].ok(trace)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.warning(f"Trace creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Trace].fail_op("start trace", e)

    class AlertingService:
        """Service for alert management."""

        _container: p.Container
        logger: p.Logger
        _alerts: MutableSequence[FlextObservability.Alert]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextContainer.shared()
            self.logger = u.fetch_logger(__name__)
            self._alerts = list[FlextObservability.Alert]()

        def create_alert(
            self,
            title: str,
            message: str,
            severity: c.Observability.AlertLevel = c.Observability.AlertLevel.WARNING,
            source: str = "system",
            labels: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Alert]:
            """Create an alert with validation."""
            try:
                if not title:
                    return r[FlextObservability.Alert].fail_op(
                        "create alert",
                        "Alert title cannot be empty",
                    )
                if not message:
                    return r[FlextObservability.Alert].fail_op(
                        "create alert",
                        "Alert message cannot be empty",
                    )
                resolved_labels: dict[str, t.Scalar] = (
                    dict(labels) if labels is not None else {}
                )
                alert = FlextObservability.Alert(
                    id=str(uuid4()),
                    title=title,
                    message=message,
                    severity=severity,
                    source=source,
                    labels=resolved_labels,
                    domain_events=[],
                )
                self._alerts.append(alert)
                return r[FlextObservability.Alert].ok(alert)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.warning(f"Alert creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Alert].fail_op("create alert", e)

    class HealthService:
        """Service for health check management."""

        _container: p.Container
        logger: p.Logger
        _checks: MutableSequence[FlextObservability.HealthCheck]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextContainer.shared()
            self.logger = u.fetch_logger(__name__)
            self._checks = list[FlextObservability.HealthCheck]()

        def check_component(
            self,
            component: str,
            status: c.Observability.HealthStatus = c.Observability.HealthStatus.HEALTHY,
            details: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.HealthCheck]:
            """Create a health check."""
            try:
                if not component:
                    return r[FlextObservability.HealthCheck].fail_op(
                        "create health check",
                        "Component name cannot be empty",
                    )
                if status not in FlextObservability.Constants.HEALTH_STATUSES:
                    return r[FlextObservability.HealthCheck].fail_op(
                        "create health check",
                        f"Invalid health status: {status}",
                    )
                resolved_details: dict[str, t.Scalar] = (
                    dict(details) if details is not None else {}
                )
                health = FlextObservability.HealthCheck(
                    id=str(uuid4()),
                    component=component,
                    status=status,
                    details=resolved_details,
                    domain_events=[],
                )
                self._checks.append(health)
                return r[FlextObservability.HealthCheck].ok(health)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.warning(f"Health check failed: %s: {e}", exc_info=True)
                return r[FlextObservability.HealthCheck].fail_op(
                    "create health check",
                    e,
                )

    class LoggingService:
        """Service for structured logging."""

        _container: p.Container
        logger: p.Logger
        entries: MutableSequence[FlextObservability.LogEntry]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextContainer.shared()
            self.logger = u.fetch_logger(__name__)
            self.entries = list[FlextObservability.LogEntry]()

        def log_entry(
            self,
            message: str,
            level: c.Observability.ErrorSeverity = c.Observability.ErrorSeverity.INFO,
            component: str = "application",
            context: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.LogEntry]:
            """Create a log entry."""
            try:
                if not message:
                    return r[FlextObservability.LogEntry].fail_op(
                        "create log entry",
                        "Log message cannot be empty",
                    )
                resolved_context: dict[str, t.Scalar] = (
                    dict(context) if context is not None else {}
                )
                entry = FlextObservability.LogEntry(
                    id=str(uuid4()),
                    message=message,
                    level=level,
                    component=component,
                    timestamp=datetime.now(tz=UTC),
                    context=resolved_context,
                    domain_events=[],
                )
                self.entries.append(entry)
                return r[FlextObservability.LogEntry].ok(entry)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.warning(
                    f"Log entry creation failed: %s: {e}",
                    exc_info=True,
                )
                return r[FlextObservability.LogEntry].fail_op("create log entry", e)

    @staticmethod
    def flext_metric(
        name: str,
        value: float,
        unit: str = "count",
        **kwargs: t.JsonPayload,
    ) -> p.Result[FlextObservability.Metric]:
        """Create a metric entity directly."""
        try:
            if not name:
                return r[FlextObservability.Metric].fail_op(
                    "create metric",
                    "Metric name must be non-empty string",
                )
            if math.isnan(float(value)):
                return r[FlextObservability.Metric].fail_op(
                    "create metric",
                    "Metric value must be a valid number",
                )
            metric_type_raw = kwargs.get("metric_type")
            metric_id_raw = kwargs.get("metric_id")
            tags_raw = kwargs.get("tags")
            labels_raw = kwargs.get("labels")
            all_labels_data: t.MutableScalarMapping = {}
            if isinstance(tags_raw, Mapping):
                all_labels_data.update({
                    str(key): t.scalar_adapter().validate_python(value)
                    for key, value in tags_raw.items()
                })
            if isinstance(labels_raw, Mapping):
                all_labels_data.update({
                    str(key): t.scalar_adapter().validate_python(value)
                    for key, value in labels_raw.items()
                })
            detected_type: c.Observability.MetricType = (
                m.Observability.MetricTypeInput.model_validate(
                    {"metric_type": metric_type_raw},
                ).metric_type
                if metric_type_raw is not None
                else c.Observability.MetricType.GAUGE
            )
            if metric_type_raw is None:
                if name.endswith(("_total", "_count")):
                    detected_type = c.Observability.MetricType.COUNTER
                elif name.endswith(("_duration", "_seconds")):
                    detected_type = c.Observability.MetricType.HISTOGRAM
            metric = FlextObservability.Metric(
                id=(
                    t.str_adapter().validate_python(metric_id_raw)
                    if metric_id_raw is not None
                    else str(uuid4())
                ),
                name=name,
                value=float(value),
                unit=unit,
                metric_type=detected_type,
                labels=dict(all_labels_data),
                domain_events=[],
            )
            return r[FlextObservability.Metric].ok(metric)
        except (c.ValidationError, ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.Metric].fail_op("create metric", e)

    @staticmethod
    def flext_trace(
        name: str,
        attributes: t.ScalarMapping | None = None,
        trace_id: str | None = None,
    ) -> p.Result[FlextObservability.Trace]:
        """Create a trace entity directly."""
        try:
            if not name:
                return r[FlextObservability.Trace].fail_op(
                    "create trace",
                    "Trace name must be non-empty string",
                )
            resolved_attrs: dict[str, t.Scalar] = (
                dict(attributes) if attributes is not None else {}
            )
            trace = FlextObservability.Trace(
                name=name,
                trace_id=trace_id or str(uuid4()),
                attributes=resolved_attrs,
                domain_events=[],
            )
            return r[FlextObservability.Trace].ok(trace)
        except (ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.Trace].fail_op("create trace", e)

    @staticmethod
    def flext_alert(**kwargs: t.JsonValue) -> p.Result[FlextObservability.Alert]:
        """Create an alert entity directly."""
        try:
            payload: t.MutableJsonMapping = dict(kwargs)
            _ = payload.pop("status", c.Observability.AlertStatus.FIRING)
            payload.setdefault("title", "")
            payload.setdefault("message", "")
            if not payload["message"] and (not payload["title"]):
                return r[FlextObservability.Alert].fail_op(
                    "create alert",
                    "Alert message cannot be empty",
                )
            if not payload["title"] and payload["message"]:
                return r[FlextObservability.Alert].fail_op(
                    "create alert",
                    "Alert title cannot be empty",
                )
            alert_id = payload.pop("alert_id", None)
            if alert_id is not None and "id" not in payload:
                payload["id"] = alert_id
            payload.setdefault("severity", c.Observability.AlertLevel.WARNING)
            payload.setdefault("source", "system")
            labels_data = payload.get("labels")
            resolved_labels: dict[str, t.JsonValue] = {
                str(key): value
                if isinstance(value, (bool, int, float, str)) or value is None
                else str(value)
                for key, value in (
                    labels_data.items() if isinstance(labels_data, dict) else ()
                )
            }
            payload["labels"] = resolved_labels
            payload.setdefault("domain_events", [])
            return r[FlextObservability.Alert].ok(
                FlextObservability.Alert.model_validate(payload),
            )
        except (ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.Alert].fail_op("create alert", e)

    @staticmethod
    def flext_health_check(
        component: str,
        status: c.Observability.HealthStatus = c.Observability.HealthStatus.HEALTHY,
        health_check_id: str | None = None,
        details: t.ScalarMapping | None = None,
    ) -> p.Result[FlextObservability.HealthCheck]:
        """Create a health check entity directly."""
        _ = health_check_id
        try:
            if not component:
                return r[FlextObservability.HealthCheck].fail_op(
                    "create health check",
                    "Component name cannot be empty",
                )
            if status not in FlextObservability.Constants.HEALTH_STATUSES:
                return r[FlextObservability.HealthCheck].fail_op(
                    "create health check",
                    f"Invalid health status: {status}",
                )
            resolved_details: dict[str, t.Scalar] = (
                dict(details) if details is not None else {}
            )
            health = FlextObservability.HealthCheck(
                id=health_check_id or str(uuid4()),
                component=component,
                status=status,
                details=resolved_details,
                domain_events=[],
            )
            return r[FlextObservability.HealthCheck].ok(health)
        except (ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.HealthCheck].fail_op(
                "create health check",
                e,
            )

    @staticmethod
    def flext_log_entry(
        message: str,
        level: c.Observability.ErrorSeverity = c.Observability.ErrorSeverity.INFO,
        component: str = "application",
        timestamp: datetime | None = None,
        context: t.ScalarMapping | None = None,
    ) -> p.Result[FlextObservability.LogEntry]:
        """Create a log entry entity directly."""
        try:
            if not message:
                return r[FlextObservability.LogEntry].fail_op(
                    "create log entry",
                    "Log message cannot be empty",
                )
            resolved_context: dict[str, t.Scalar] = (
                dict(context) if context is not None else {}
            )
            entry = FlextObservability.LogEntry(
                id=str(uuid4()),
                message=message,
                level=level,
                component=component,
                timestamp=timestamp or datetime.now(tz=UTC),
                context=resolved_context,
                domain_events=[],
            )
            return r[FlextObservability.LogEntry].ok(entry)
        except (ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.LogEntry].fail_op("create log entry", e)

    @staticmethod
    def global_factory() -> FlextObservability.FlextObservabilityMasterFactory:
        """Return the global factory instance, creating it on first access."""
        if FlextObservability._global_factory is None:
            FlextObservability._global_factory = (
                FlextObservability.FlextObservabilityMasterFactory()
            )
        return FlextObservability._global_factory

    @staticmethod
    def clear_global_factory() -> None:
        """Clear the global factory instance."""
        FlextObservability._global_factory = None

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
            self._container = container or FlextContainer.shared()
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
            severity: str = c.Observability.AlertLevel.WARNING,
            tags: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Alert]:
            """Create an alert."""
            valid_severity: c.Observability.AlertLevel
            match severity:
                case c.Observability.AlertLevel.INFO | "low":
                    valid_severity = c.Observability.AlertLevel.INFO
                case c.Observability.AlertLevel.WARNING | "medium":
                    valid_severity = c.Observability.AlertLevel.WARNING
                case c.Observability.AlertLevel.ERROR | "high":
                    valid_severity = c.Observability.AlertLevel.ERROR
                case c.Observability.AlertLevel.CRITICAL:
                    valid_severity = c.Observability.AlertLevel.CRITICAL
                case _:
                    valid_severity = c.Observability.AlertLevel.WARNING
            json_labels: dict[str, t.JsonValue] | None = (
                {str(k): str(v) for k, v in tags.items()} if tags is not None else None
            )
            return FlextObservability.flext_alert(
                title=title,
                message=message,
                severity=valid_severity,
                labels=json_labels,
            )

        def create_alert(
            self,
            message: str,
            service: str = "default",
            severity: str = c.Observability.AlertLevel.WARNING,
            tags: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Alert]:
            """Create an alert (alias)."""
            return self.alert(
                f"Alert: {service}",
                message,
                severity=severity,
                tags=tags,
            )

        def create_health_check(
            self,
            component: str,
            status: str = c.Observability.HealthStatus.HEALTHY,
            details: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.HealthCheck]:
            """Create a health check (alias)."""
            return self.health_check(component, status=status, metrics=details)

        def create_log_entry(
            self,
            message: str,
            level: str = c.Observability.ErrorSeverity.INFO,
            context: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.LogEntry]:
            """Create a log entry (alias)."""
            return self.log(message, level=level, context=context)

        def create_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            tags: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Metric]:
            """Create a metric (alias)."""
            return self.metric(name, value, unit=unit, tags=tags)

        def create_trace(
            self,
            operation: str,
            service: str = "default",
            tags: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Trace]:
            """Create a trace (alias)."""
            attrs: t.ScalarMapping | None = None
            if tags is not None:
                attrs = dict(tags.items())
            return self.trace(f"trace-{service}", operation, span_attributes=attrs)

        def health_check(
            self,
            component: str,
            status: str = c.Observability.HealthStatus.HEALTHY,
            message: str | None = None,
            metrics: t.ScalarMapping | None = None,
            timestamp: datetime | None = None,
        ) -> p.Result[FlextObservability.HealthCheck]:
            """Create a health check."""
            _ = timestamp
            _ = message
            valid_status: c.Observability.HealthStatus
            match status:
                case c.Observability.HealthStatus.HEALTHY:
                    valid_status = c.Observability.HealthStatus.HEALTHY
                case c.Observability.HealthStatus.DEGRADED:
                    valid_status = c.Observability.HealthStatus.DEGRADED
                case c.Observability.HealthStatus.UNHEALTHY:
                    valid_status = c.Observability.HealthStatus.UNHEALTHY
                case _:
                    valid_status = c.Observability.HealthStatus.HEALTHY
            return FlextObservability.flext_health_check(
                component,
                status=valid_status,
                details=metrics,
            )

        def health_status(self) -> p.Result[FlextObservability.HealthCheck]:
            """Get overall health status."""
            return FlextObservability.flext_health_check(
                "system",
                status=c.Observability.HealthStatus.HEALTHY,
            )

        def log(
            self,
            message: str,
            level: str = c.Observability.ErrorSeverity.INFO,
            context: t.ScalarMapping | None = None,
            timestamp: datetime | None = None,
        ) -> p.Result[FlextObservability.LogEntry]:
            """Create a log entry."""
            valid_level: c.Observability.ErrorSeverity
            match level:
                case c.Observability.ErrorSeverity.DEBUG:
                    valid_level = c.Observability.ErrorSeverity.DEBUG
                case c.Observability.ErrorSeverity.INFO:
                    valid_level = c.Observability.ErrorSeverity.INFO
                case c.Observability.ErrorSeverity.WARNING:
                    valid_level = c.Observability.ErrorSeverity.WARNING
                case c.Observability.ErrorSeverity.ERROR:
                    valid_level = c.Observability.ErrorSeverity.ERROR
                case c.Observability.ErrorSeverity.CRITICAL:
                    valid_level = c.Observability.ErrorSeverity.CRITICAL
                case _:
                    valid_level = c.Observability.ErrorSeverity.INFO
            return FlextObservability.flext_log_entry(
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
            tags: t.ScalarMapping | None = None,
            timestamp: datetime | None = None,
        ) -> p.Result[FlextObservability.Metric]:
            """Create a metric."""
            _ = timestamp
            return FlextObservability.flext_metric(
                name,
                value,
                unit=unit,
                tags=tags,
            )

        def trace(
            self,
            trace_id: str,
            operation: str,
            span_attributes: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Trace]:
            """Create a trace span."""
            str_attributes: t.ScalarMapping = {}
            if span_attributes:
                str_attributes = {k: str(v) for k, v in span_attributes.items()}
            return FlextObservability.flext_trace(
                operation,
                attributes=str_attributes,
                trace_id=trace_id,
            )


observability = FlextObservability

__all__: list[str] = ["FlextObservability", "observability"]
