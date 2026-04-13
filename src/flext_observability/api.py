"""FlextObservability MRO facade and master factory.

All service methods come from mixins via MRO. Only factory methods,
model aliases, and Constants are defined locally.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
from collections.abc import MutableSequence
from datetime import UTC, datetime
from typing import ClassVar, TypeAlias
from uuid import uuid4

from flext_core import FlextContainer, p, r, u
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
    _logger: p.Logger = u.fetch_logger(__name__)
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
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        }

    Metric: TypeAlias = m.Observability.Metric
    Trace: TypeAlias = m.Observability.Trace
    Alert: TypeAlias = m.Observability.Alert
    HealthCheck: TypeAlias = m.Observability.HealthCheck
    LogEntry: TypeAlias = m.Observability.LogEntry

    class MetricsService:
        """Service for metrics collection and recording."""

        _container: p.Container
        _logger: p.Logger
        _metrics: MutableSequence[FlextObservability.Metric]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextContainer.shared()
            self._logger = u.fetch_logger(__name__)
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
                self._logger.warning(f"Metric recording failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Metric].fail_op("record metric", e)

    class TracingService:
        """Service for distributed tracing."""

        _container: p.Container
        _logger: p.Logger
        _traces: MutableSequence[FlextObservability.Trace]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextContainer.shared()
            self._logger = u.fetch_logger(__name__)
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
                self._logger.warning(f"Trace creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Trace].fail_op("start trace", e)

    class AlertingService:
        """Service for alert management."""

        _container: p.Container
        _logger: p.Logger
        _alerts: MutableSequence[FlextObservability.Alert]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextContainer.shared()
            self._logger = u.fetch_logger(__name__)
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
                self._logger.warning(f"Alert creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Alert].fail_op("create alert", e)

    class HealthService:
        """Service for health check management."""

        _container: p.Container
        _logger: p.Logger
        _checks: MutableSequence[FlextObservability.HealthCheck]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextContainer.shared()
            self._logger = u.fetch_logger(__name__)
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
                self._logger.warning(f"Health check failed: %s: {e}", exc_info=True)
                return r[FlextObservability.HealthCheck].fail_op(
                    "create health check",
                    e,
                )

    class LoggingService:
        """Service for structured logging."""

        _container: p.Container
        _logger: p.Logger
        _entries: MutableSequence[FlextObservability.LogEntry]

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextContainer.shared()
            self._logger = u.fetch_logger(__name__)
            self._entries = list[FlextObservability.LogEntry]()

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
                self._entries.append(entry)
                return r[FlextObservability.LogEntry].ok(entry)
            except (ValueError, TypeError, AttributeError) as e:
                self._logger.warning(
                    f"Log entry creation failed: %s: {e}",
                    exc_info=True,
                )
                return r[FlextObservability.LogEntry].fail_op("create log entry", e)

    @staticmethod
    def flext_metric(
        name: str,
        value: float,
        unit: str = "count",
        metric_type: c.Observability.MetricType | None = None,
        metric_id: str | None = None,
        tags: t.ScalarMapping | None = None,
        labels: t.ScalarMapping | None = None,
    ) -> p.Result[FlextObservability.Metric]:
        """Create a metric entity directly."""
        _ = metric_id
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
            all_labels_data: t.MutableScalarMapping = {}
            if tags:
                all_labels_data.update(tags)
            if labels:
                all_labels_data.update(labels)
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
                labels=dict(all_labels_data),
                domain_events=[],
            )
            return r[FlextObservability.Metric].ok(metric)
        except (ValueError, TypeError, AttributeError) as e:
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
    def flext_alert(
        title: str = "",
        message: str = "",
        severity: c.Observability.AlertLevel = c.Observability.AlertLevel.WARNING,
        status: c.Observability.AlertStatus = c.Observability.AlertStatus.FIRING,
        alert_id: str | None = None,
        source: str = "system",
        labels: t.ScalarMapping | None = None,
    ) -> p.Result[FlextObservability.Alert]:
        """Create an alert entity directly."""
        _ = status
        try:
            if not message and (not title):
                return r[FlextObservability.Alert].fail_op(
                    "create alert",
                    "Alert message cannot be empty",
                )
            if not title and message:
                return r[FlextObservability.Alert].fail_op(
                    "create alert",
                    "Alert title cannot be empty",
                )
            resolved_labels: dict[str, t.Scalar] = (
                dict(labels) if labels is not None else {}
            )
            alert = FlextObservability.Alert(
                id=alert_id or str(uuid4()),
                title=title,
                message=message,
                severity=severity,
                source=source,
                labels=resolved_labels,
                domain_events=[],
            )
            return r[FlextObservability.Alert].ok(alert)
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
            severity: str = "warning",
            tags: t.ScalarMapping | None = None,
            status: str = c.Observability.AlertStatus.FIRING,
            timestamp: datetime | None = None,
        ) -> p.Result[FlextObservability.Alert]:
            """Create an alert."""
            _ = timestamp
            valid_severity: c.Observability.AlertLevel
            match severity:
                case "info" | "low":
                    valid_severity = c.Observability.AlertLevel.INFO
                case "warning" | "medium":
                    valid_severity = c.Observability.AlertLevel.WARNING
                case "error" | "high":
                    valid_severity = c.Observability.AlertLevel.ERROR
                case "critical":
                    valid_severity = c.Observability.AlertLevel.CRITICAL
                case _:
                    valid_severity = c.Observability.AlertLevel.WARNING
            valid_status: c.Observability.AlertStatus
            match status:
                case "firing" | "active":
                    valid_status = c.Observability.AlertStatus.FIRING
                case "resolved":
                    valid_status = c.Observability.AlertStatus.RESOLVED
                case _:
                    valid_status = c.Observability.AlertStatus.FIRING
            return FlextObservability.flext_alert(
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
            level: str = "info",
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
                case "healthy":
                    valid_status = c.Observability.HealthStatus.HEALTHY
                case "degraded":
                    valid_status = c.Observability.HealthStatus.DEGRADED
                case "unhealthy":
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
                case "debug":
                    valid_level = c.Observability.ErrorSeverity.DEBUG
                case "info":
                    valid_level = c.Observability.ErrorSeverity.INFO
                case "warning":
                    valid_level = c.Observability.ErrorSeverity.WARNING
                case "error":
                    valid_level = c.Observability.ErrorSeverity.ERROR
                case "critical":
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
            span_id: str | None = None,
            span_attributes: t.ScalarMapping | None = None,
            duration_ms: float | None = None,
            status: str = "unset",
        ) -> p.Result[FlextObservability.Trace]:
            """Create a trace span."""
            _ = span_id
            _ = duration_ms
            _ = status
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
