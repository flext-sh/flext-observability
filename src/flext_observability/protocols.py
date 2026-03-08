"""Observability protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, t


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

    @runtime_checkable
    class _SpanProtocol(Protocol):
        """Protocol for OpenTelemetry Span interface."""

        def set_attribute(self, key: str, *, value: t.Scalar) -> None:
            """Set span attribute."""
            ...

        def set_status(self, status: int) -> None:
            """Set span status."""
            ...

    class Observability:
        """Observability domain-specific protocols.

        Provides protocols for metrics collection, distributed tracing,
        alerting, health checks, logging, and dashboard visualization.
        """

        @runtime_checkable
        class MetricsProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for metrics collection and management operations."""

            def create_counter(
                self, name: str, description: str, *, unit: str = "count"
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Create a counter metric."""
                ...

            def create_gauge(
                self, name: str, description: str, *, unit: str = "value"
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Create a gauge metric."""
                ...

            def create_histogram(
                self,
                name: str,
                description: str,
                *,
                unit: str = "seconds",
                buckets: list[t.Scalar] | None = None,
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Create a histogram metric."""
                ...

            def get_metrics(
                self,
                name_pattern: t.Scalar | None = None,
                *,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> FlextProtocols.Result[list[t.ConfigurationMapping]]:
                """Get collected metrics."""
                ...

            def record_metric(
                self,
                name: str,
                value: float,
                *,
                unit: str = "count",
                tags: Mapping[str, t.Scalar] | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Record a metric value."""
                ...

        @runtime_checkable
        class TracingProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for distributed tracing operations."""

            def add_span_tag(
                self,
                span: FlextObservabilityProtocols._SpanProtocol,
                key: str,
                value: t.Scalar,
            ) -> FlextProtocols.Result[bool]:
                """Add tag to trace span."""
                ...

            def finish_span(
                self,
                span: FlextObservabilityProtocols._SpanProtocol,
                *,
                status: str = "ok",
                error: t.Scalar | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Finish a trace span."""
                ...

            def get_trace(
                self, trace_id: str
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Get trace by ID."""
                ...

            def search_traces(
                self,
                *,
                service_name: t.Scalar | None = None,
                operation_name: t.Scalar | None = None,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> FlextProtocols.Result[list[t.ConfigurationMapping]]:
                """Search traces by criteria."""
                ...

            def start_span(
                self,
                operation_name: str,
                *,
                service_name: t.Scalar | None = None,
                parent_span_id: t.Scalar | None = None,
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Start a new trace span."""
                ...

        @runtime_checkable
        class AlertingProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for alerting and notification operations."""

            def create_alert(
                self,
                message: str,
                level: str,
                *,
                service: t.Scalar | None = None,
                tags: Mapping[str, t.Scalar] | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create an alert."""
                ...

            def create_alert_rule(
                self,
                name: str,
                condition: str,
                *,
                threshold: t.Scalar | None = None,
                duration: t.Scalar | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create an alert rule."""
                ...

            def get_alerts(
                self,
                *,
                level: t.Scalar | None = None,
                service: t.Scalar | None = None,
                resolved: t.Scalar | None = None,
            ) -> FlextProtocols.Result[list[t.ConfigurationMapping]]:
                """Get alerts by criteria."""
                ...

            def resolve_alert(self, alert_id: str) -> FlextProtocols.Result[bool]:
                """Resolve an alert."""
                ...

        @runtime_checkable
        class HealthCheckProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for health check operations."""

            def check_health(
                self, service_name: str
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Perform health check for a service."""
                ...

            def get_all_services_status(
                self,
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Get health status for all services."""
                ...

            def get_service_status(
                self, service_name: str
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Get service health status."""
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

        @runtime_checkable
        class LoggingProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for logging operations."""

            def configure_logging(
                self, config: Mapping[str, t.ContainerValue]
            ) -> FlextProtocols.Result[bool]:
                """Configure logging system."""
                ...

            def create_logger(
                self,
                name: str,
                *,
                level: str = "info",
                format_string: t.Scalar | None = None,
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Create a logger instance."""
                ...

            def get_logs(
                self,
                *,
                level: t.Scalar | None = None,
                service: t.Scalar | None = None,
                correlation_id: t.Scalar | None = None,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> FlextProtocols.Result[list[t.ConfigurationMapping]]:
                """Get logs by criteria."""
                ...

            def log_message(
                self,
                message: str,
                level: str,
                *,
                service: t.Scalar | None = None,
                correlation_id: t.Scalar | None = None,
                extra: Mapping[str, t.ContainerValue] | None = None,
            ) -> FlextProtocols.Result[bool]:
                """Log a message."""
                ...

        @runtime_checkable
        class DashboardProtocol(FlextProtocols.Service[t.ContainerValue], Protocol):
            """Protocol for dashboard and visualization operations."""

            def add_widget(
                self, dashboard_id: str, widget_config: Mapping[str, t.ContainerValue]
            ) -> FlextProtocols.Result[str]:
                """Add widget to dashboard."""
                ...

            def create_dashboard(
                self,
                name: str,
                description: str,
                *,
                widgets: list[Mapping[str, t.ContainerValue]] | None = None,
            ) -> FlextProtocols.Result[str]:
                """Create a dashboard."""
                ...

            def get_dashboard(
                self, dashboard_id: str
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Get dashboard by ID."""
                ...

            def get_dashboard_data(
                self,
                dashboard_id: str,
                *,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> FlextProtocols.Result[t.ConfigurationMapping]:
                """Get dashboard data."""
                ...


p = FlextObservabilityProtocols
__all__ = ["FlextObservabilityProtocols", "p"]
