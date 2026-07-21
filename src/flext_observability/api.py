"""FlextObservability MRO facade and master factory.

All service methods come from mixins via MRO. Only factory methods,
model aliases, and Constants are defined locally.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import TYPE_CHECKING, ClassVar
from uuid import uuid4

from flext_core import FlextContainer
from flext_observability import c, m, p, r, t, u
from flext_observability.services.advanced_context import (
    FlextObservabilityAdvancedContext,
)
from flext_observability.services.context import FlextObservabilityContext
from flext_observability.services.custom_metrics import FlextObservabilityCustomMetrics
from flext_observability.services.error_handling import FlextObservabilityErrorHandling
from flext_observability.services.health import FlextObservabilityHealth
from flext_observability.services.http_client_instrumentation import (
    FlextObservabilityHTTPClient,
)
from flext_observability.services.http_instrumentation import FlextObservabilityHTTP
from flext_observability.services.logging_integration import FlextObservabilityLogging
from flext_observability.services.monitoring import FlextObservabilityMonitor
from flext_observability.services.performance import FlextObservabilityPerformance
from flext_observability.services.sampling import FlextObservabilitySampling
from flext_observability.services.services import FlextObservabilityServices

if TYPE_CHECKING:
    from datetime import datetime

    from flext_observability._settings import FlextObservabilitySettings


class FlextObservability(
    FlextObservabilityAdvancedContext,
    FlextObservabilityContext,
    FlextObservabilityCustomMetrics,
    FlextObservabilityErrorHandling,
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

    class Metric(m.Observability.Metric):
        """Observability metric entity."""

    class Trace(m.Observability.Trace):
        """Observability trace entity."""

    class Alert(m.Observability.Alert):
        """Observability alert entity."""

    class HealthCheck(m.Observability.HealthCheck):
        """Observability health check entity."""

    class LogEntry(m.Observability.LogEntry):
        """Observability log entry entity."""

    # mro-ktv9 (kimi-c): metric_type_for_name relocated from the removed
    # MetricsService shell (dead MasterFactory island); sole live caller is
    # _flext_metric_type below.
    @staticmethod
    def _metric_type_for_name(name: str) -> c.Observability.MetricType:
        """Resolve metric type from a metric name suffix."""
        if name.endswith(("_total", "_count")):
            return c.Observability.MetricType.COUNTER
        if name.endswith(("_duration", "_seconds")):
            return c.Observability.MetricType.HISTOGRAM
        return c.Observability.MetricType.GAUGE

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
        metric_id: str = t.str_adapter().validate_python(metric_id_raw)
        return metric_id

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
        return FlextObservability._metric_type_for_name(name)

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
        if u.mapping(raw_labels):
            resolved_labels = {
                key: value if value is None or u.primitive(value) else str(value)
                for key, value in raw_labels.items()
            }
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


observability = FlextObservability

__all__: list[str] = ["FlextObservability", "observability"]
