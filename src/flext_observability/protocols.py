"""Observability protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextTypes as t


@runtime_checkable
class _SpanProtocol(Protocol):
    """Protocol for OpenTelemetry Span interface."""

    def set_attribute(self, key: str, *, value: t.ScalarValue) -> None:
        """Set span attribute."""
        ...

    def set_status(self, status: int) -> None:
        """Set span status."""
        ...


Span = _SpanProtocol


class FlextObservabilityProtocols(FlextProtocols):
    """Unified observability protocols following FLEXT domain extension pattern.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds observability-specific protocols in the Observability namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: Observability-specific protocols in Observability namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_observability import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Observability-specific protocols
    metrics: p.Observability.MetricsProtocol
    tracing: p.Observability.TracingProtocol
    """

    # =========================================================================
    # OBSERVABILITY-SPECIFIC PROTOCOLS
    # =========================================================================
    # Domain-specific protocols for metrics, tracing, alerting, health,
    # logging, and dashboard operations.

    class Observability:
        """Observability domain-specific protocols.

        Provides protocols for metrics collection, distributed tracing,
        alerting, health checks, logging, and dashboard visualization.
        """

        @runtime_checkable
        class MetricsProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for metrics collection and management operations."""

            def record_metric(
                self,
                name: str,
                value: float,
                *,
                unit: str = "count",
                tags: Mapping[str, t.ScalarValue] | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Record a metric value."""
                ...

            def get_metrics(
                self,
                name_pattern: t.ScalarValue | None = None,
                *,
                start_time: t.ScalarValue | None = None,
                end_time: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[list[Mapping[str, t.GeneralValueType]]]:
                """Get collected metrics."""
                ...

            def create_counter(
                self,
                name: str,
                description: str,
                *,
                unit: str = "count",
            ) -> FlextProtocols.Result[t.GeneralValueType]:
                """Create a counter metric."""
                ...

            def create_gauge(
                self,
                name: str,
                description: str,
                *,
                unit: str = "value",
            ) -> FlextProtocols.Result[t.GeneralValueType]:
                """Create a gauge metric."""
                ...

            def create_histogram(
                self,
                name: str,
                description: str,
                *,
                unit: str = "seconds",
                buckets: list[t.ScalarValue] | None = None,
            ) -> FlextProtocols.Result[t.GeneralValueType]:
                """Create a histogram metric."""
                ...

        @runtime_checkable
        class TracingProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for distributed tracing operations."""

            def start_span(
                self,
                operation_name: str,
                *,
                service_name: t.ScalarValue | None = None,
                parent_span_id: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[t.GeneralValueType]:
                """Start a new trace span."""
                ...

            def finish_span(
                self,
                span: Span,
                *,
                status: str = "ok",
                error: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Finish a trace span."""
                ...

            def add_span_tag(
                self,
                span: Span,
                key: str,
                value: t.ScalarValue,
            ) -> FlextProtocols.Result[bool]:
                """Add tag to trace span."""
                ...

            def get_trace(
                self,
                trace_id: str,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Get trace by ID."""
                ...

            def search_traces(
                self,
                *,
                service_name: t.ScalarValue | None = None,
                operation_name: t.ScalarValue | None = None,
                start_time: t.ScalarValue | None = None,
                end_time: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[list[Mapping[str, t.GeneralValueType]]]:
                """Search traces by criteria."""
                ...

        @runtime_checkable
        class AlertingProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for alerting and notification operations."""

            def create_alert(
                self,
                message: str,
                level: str,
                *,
                service: t.ScalarValue | None = None,
                tags: Mapping[str, t.ScalarValue] | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create an alert."""
                ...

            def resolve_alert(self, alert_id: str) -> FlextProtocols.Result[bool]:
                """Resolve an alert."""
                ...

            def get_alerts(
                self,
                *,
                level: t.ScalarValue | None = None,
                service: t.ScalarValue | None = None,
                resolved: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[list[Mapping[str, t.GeneralValueType]]]:
                """Get alerts by criteria."""
                ...

            def create_alert_rule(
                self,
                name: str,
                condition: str,
                *,
                threshold: t.ScalarValue | None = None,
                duration: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create an alert rule."""
                ...

        @runtime_checkable
        class HealthCheckProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for health check operations."""

            def check_health(
                self,
                service_name: str,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Perform health check for a service."""
                ...

            def register_health_check(
                self,
                service_name: str,
                check_function: Callable[[], bool],
                *,
                interval: int = 60,
            ) -> FlextProtocols.Result[bool]:
                """Register a health check."""
                ...

            def get_service_status(
                self,
                service_name: str,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Get service health status."""
                ...

            def get_all_services_status(
                self,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Get health status for all services."""
                ...

        @runtime_checkable
        class LoggingProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for logging operations."""

            def log_message(
                self,
                message: str,
                level: str,
                *,
                service: t.ScalarValue | None = None,
                correlation_id: t.ScalarValue | None = None,
                extra: Mapping[str, t.GeneralValueType] | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Log a message."""
                ...

            def get_logs(
                self,
                *,
                level: t.ScalarValue | None = None,
                service: t.ScalarValue | None = None,
                correlation_id: t.ScalarValue | None = None,
                start_time: t.ScalarValue | None = None,
                end_time: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[list[Mapping[str, t.GeneralValueType]]]:
                """Get logs by criteria."""
                ...

            def create_logger(
                self,
                name: str,
                *,
                level: str = "info",
                format_string: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[t.GeneralValueType]:
                """Create a logger instance."""
                ...

            def configure_logging(
                self,
                config: Mapping[str, t.GeneralValueType],
            ) -> FlextProtocols.Result[bool]:
                """Configure logging system."""
                ...

        @runtime_checkable
        class DashboardProtocol(FlextProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for dashboard and visualization operations."""

            def create_dashboard(
                self,
                name: str,
                description: str,
                *,
                widgets: list[Mapping[str, t.GeneralValueType]] | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create a dashboard."""
                ...

            def get_dashboard(
                self,
                dashboard_id: str,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Get dashboard by ID."""
                ...

            def add_widget(
                self,
                dashboard_id: str,
                widget_config: Mapping[str, t.GeneralValueType],
            ) -> FlextProtocols.Result[str]:
                """Add widget to dashboard."""
                ...

            def get_dashboard_data(
                self,
                dashboard_id: str,
                *,
                start_time: t.ScalarValue | None = None,
                end_time: t.ScalarValue | None = None,
            ) -> FlextProtocols.Result[Mapping[str, t.GeneralValueType]]:
                """Get dashboard data."""
                ...


# Runtime alias for simplified usage
p = FlextObservabilityProtocols

__all__ = [
    "FlextObservabilityProtocols",
    "p",
]
