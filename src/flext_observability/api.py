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
from datetime import datetime
from typing import ClassVar, TypeAlias
from uuid import uuid4

from flext_core import FlextContainer
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
    u,
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

    All operations come from mixin bases via MRO. Only factory methods
    and model aliases are defined locally.
    """

    _settings: FlextObservabilitySettings
    _container: p.Container
    _container_type: ClassVar[p.ContainerType] = FlextContainer
    logger: p.Logger = u.fetch_logger(__name__)
    _global_factory: ClassVar[
        FlextObservability.FlextObservabilityMasterFactory | None
    ] = None

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

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize metrics service."""
            self._container = container or FlextObservability._container_type.shared()
            self.logger = u.fetch_logger(__name__)
            self._metrics = list[FlextObservability.Metric]()

        @staticmethod
        def metric_type_for_name(name: str) -> c.Observability.MetricType:
            """Resolve metric type from a metric name suffix."""
            if name.endswith(("_total", "_count")):
                return c.Observability.MetricType.COUNTER
            if name.endswith(("_duration", "_seconds")):
                return c.Observability.MetricType.HISTOGRAM
            return c.Observability.MetricType.GAUGE

        def _record_metric_entity(
            self,
            name: str,
            value: float,
            unit: str,
            labels: t.ScalarMapping | None,
        ) -> p.Result[FlextObservability.Metric]:
            """Create and store a metric entity."""
            if not name:
                return r[FlextObservability.Metric].fail_op(
                    "record metric",
                    "Metric name must be non-empty string",
                )
            if math.isnan(value):
                return r[FlextObservability.Metric].fail_op(
                    "record metric",
                    "Metric value must be a valid number",
                )
            metric = FlextObservability.Metric(
                id=str(uuid4()),
                name=name,
                value=value,
                unit=unit,
                metric_type=FlextObservability.MetricsService.metric_type_for_name(
                    name,
                ),
                labels=dict(labels) if labels is not None else {},
                domain_events=[],
            )
            self._metrics.append(metric)
            return r[FlextObservability.Metric].ok(metric)

        def record_metric(
            self,
            name: str,
            value: float,
            unit: str = "count",
            labels: t.ScalarMapping | None = None,
        ) -> p.Result[FlextObservability.Metric]:
            """Record a metric with validation."""
            try:
                return self._record_metric_entity(name, value, unit, labels)
            except c.EXC_BASIC_TYPE as e:
                self.logger.warning(f"Metric recording failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Metric].fail_op("record metric", e)

    class TracingService:
        """Service for distributed tracing."""

        _container: p.Container
        logger: p.Logger
        _traces: MutableSequence[FlextObservability.Trace]

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize tracing service."""
            self._container = container or FlextObservability._container_type.shared()
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
                resolved_attrs: t.MutableScalarMapping = (
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
            except c.EXC_BASIC_TYPE as e:
                self.logger.warning(f"Trace creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Trace].fail_op("start trace", e)

    class AlertingService:
        """Service for alert management."""

        _container: p.Container
        logger: p.Logger
        _alerts: MutableSequence[FlextObservability.Alert]

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize alerting service."""
            self._container = container or FlextObservability._container_type.shared()
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
                resolved_labels: t.MutableScalarMapping = (
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
            except c.EXC_BASIC_TYPE as e:
                self.logger.warning(f"Alert creation failed: %s: {e}", exc_info=True)
                return r[FlextObservability.Alert].fail_op("create alert", e)

    class HealthService:
        """Service for health check management."""

        _container: p.Container
        logger: p.Logger
        _checks: MutableSequence[FlextObservability.HealthCheck]

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize health service."""
            self._container = container or FlextObservability._container_type.shared()
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
                if status not in c.Observability.HealthStatus:
                    return r[FlextObservability.HealthCheck].fail_op(
                        "create health check",
                        f"Invalid health status: {status}",
                    )
                resolved_details: t.MutableScalarMapping = (
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
            except c.EXC_BASIC_TYPE as e:
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

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize logging service."""
            self._container = container or FlextObservability._container_type.shared()
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
                resolved_context = t.scalar_mapping_adapter().validate_python(
                    context or {},
                )
                entry = FlextObservability.LogEntry(
                    id=str(uuid4()),
                    message=message,
                    level=level,
                    component=component,
                    timestamp=u.now(),
                    context=resolved_context,
                    domain_events=[],
                )
                self.entries.append(entry)
                return r[FlextObservability.LogEntry].ok(entry)
            except c.EXC_BASIC_TYPE as e:
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
            return FlextObservability._flext_metric_entity(name, value, unit, kwargs)
        except (c.ValidationError, ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.Metric].fail_op("create metric", e)

    @staticmethod
    def _flext_metric_entity(
        name: str,
        value: float,
        unit: str,
        kwargs: t.MappingKV[str, t.JsonPayload],
    ) -> p.Result[FlextObservability.Metric]:
        """Create a metric entity from validated direct-factory inputs."""
        if not name:
            return r[FlextObservability.Metric].fail_op(
                "create metric",
                "Metric name must be non-empty string",
            )
        if math.isnan(value):
            return r[FlextObservability.Metric].fail_op(
                "create metric",
                "Metric value must be a valid number",
            )
        metric_type_raw = kwargs.get("metric_type")
        metric_id_raw = kwargs.get("metric_id")
        metric = FlextObservability.Metric(
            id=FlextObservability._flext_metric_id(metric_id_raw),
            name=name,
            value=value,
            unit=unit,
            metric_type=FlextObservability._flext_metric_type(name, metric_type_raw),
            labels=FlextObservability._flext_metric_labels(kwargs),
            domain_events=[],
        )
        return r[FlextObservability.Metric].ok(metric)

    @staticmethod
    def _flext_metric_id(metric_id_raw: t.JsonPayload | None) -> str:
        """Resolve a direct-factory metric id."""
        if metric_id_raw is None:
            return str(uuid4())
        return t.str_adapter().validate_python(metric_id_raw)

    @staticmethod
    def _flext_metric_type(
        name: str,
        metric_type_raw: t.JsonPayload | None,
    ) -> c.Observability.MetricType:
        """Resolve a direct-factory metric type."""
        if metric_type_raw is not None:
            return m.Observability.MetricTypeInput.model_validate(
                {"metric_type": metric_type_raw},
            ).metric_type
        return FlextObservability.MetricsService.metric_type_for_name(name)

    @staticmethod
    def _flext_metric_labels(
        kwargs: t.MappingKV[str, t.JsonPayload],
    ) -> t.MutableScalarMapping:
        """Merge tags and labels into the metric labels payload."""
        all_labels_data: t.MutableScalarMapping = {}
        for source_key in ("tags", "labels"):
            source = kwargs.get(source_key)
            if isinstance(source, Mapping):
                all_labels_data.update({
                    key: t.scalar_adapter().validate_python(value)
                    for key, value in source.items()
                })
        return all_labels_data

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
            resolved_attrs: t.MutableScalarMapping = (
                dict(attributes) if attributes is not None else {}
            )
            trace = FlextObservability.Trace(
                name=name,
                trace_id=trace_id or str(uuid4()),
                attributes=resolved_attrs,
                domain_events=[],
            )
            return r[FlextObservability.Trace].ok(trace)
        except c.EXC_BASIC_TYPE as e:
            return r[FlextObservability.Trace].fail_op("create trace", e)

    @staticmethod
    def flext_alert(**kwargs: t.JsonValue) -> p.Result[FlextObservability.Alert]:
        """Create an alert entity directly."""
        try:
            payload = FlextObservability._alert_payload(kwargs)
            return r[FlextObservability.Alert].ok(
                FlextObservability.Alert.model_validate(payload),
            )
        except (c.ValidationError, ValueError, TypeError, AttributeError) as e:
            return r[FlextObservability.Alert].fail_op("create alert", e)

    @staticmethod
    def _alert_payload(kwargs: t.MappingKV[str, t.JsonValue]) -> t.MutableJsonMapping:
        """Normalize alert factory kwargs into the canonical model payload."""
        payload: t.MutableJsonMapping = dict(kwargs)
        _ = payload.pop("status", c.Observability.AlertStatus.FIRING)
        payload.setdefault("title", "")
        payload.setdefault("message", "")
        FlextObservability._apply_alert_id(payload)
        payload.setdefault("severity", c.Observability.AlertLevel.WARNING)
        payload.setdefault("source", "system")
        payload["labels"] = FlextObservability._alert_labels(payload)
        payload.setdefault("domain_events", [])
        return payload

    @staticmethod
    def _apply_alert_id(payload: t.MutableJsonMapping) -> None:
        """Apply the alert_id input to the canonical id field."""
        if "alert_id" not in payload:
            return
        alert_id_raw = payload.pop("alert_id")
        if "id" not in payload:
            payload.setdefault("id", t.str_adapter().validate_python(alert_id_raw))

    @staticmethod
    def _alert_labels(payload: t.MappingKV[str, t.JsonValue]) -> t.JsonDict:
        """Normalize alert labels into JSON primitives."""
        raw_labels = payload.get("labels")
        resolved_labels: t.JsonDict = {}
        if not u.mapping(raw_labels):
            return resolved_labels
        for label_key, label_value in raw_labels.items():
            resolved_labels[label_key] = (
                label_value
                if u.primitive(label_value) or label_value is None
                else str(label_value)
            )
        return resolved_labels

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
            if status not in c.Observability.HealthStatus:
                return r[FlextObservability.HealthCheck].fail_op(
                    "create health check",
                    f"Invalid health status: {status}",
                )
            resolved_details: t.MutableScalarMapping = (
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
        except c.EXC_BASIC_TYPE as e:
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
            resolved_context = t.scalar_mapping_adapter().validate_python(
                context or {},
            )
            entry = FlextObservability.LogEntry(
                id=str(uuid4()),
                message=message,
                level=level,
                component=component,
                timestamp=timestamp or u.now(),
                context=resolved_context,
                domain_events=[],
            )
            return r[FlextObservability.LogEntry].ok(entry)
        except c.EXC_BASIC_TYPE as e:
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

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize factory with optional container."""
            self._container = container or FlextObservability._container_type.shared()
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
            json_labels: t.JsonDict | None = (
                {k: str(v) for k, v in tags.items()} if tags is not None else None
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
                attrs = tags
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
