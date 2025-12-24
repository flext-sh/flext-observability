"""Observability protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import p as p_base


class FlextObservabilityProtocols(p_base):
    """Unified observability protocols following FLEXT domain extension pattern.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds observability-specific protocols in the Observability namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: Observability-specific protocols in Observability namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_observability.protocols import p

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
        class MetricsProtocol(p_base.Service[object], Protocol):
            """Protocol for metrics collection and management operations."""

            def record_metric(
                self,
                name: str,
                value: float,
                *,
                unit: str = "count",
                tags: dict[str, str] | None = None,
            ) -> p_base.Result[bool]:
                """Record a metric value."""
                ...

            def get_metrics(
                self,
                name_pattern: str | None = None,
                *,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> p_base.Result[list[dict[str, object]]]:
                """Get collected metrics."""
                ...

            def create_counter(
                self,
                name: str,
                description: str,
                *,
                unit: str = "count",
            ) -> p_base.Result[object]:
                """Create a counter metric."""
                ...

            def create_gauge(
                self,
                name: str,
                description: str,
                *,
                unit: str = "value",
            ) -> p_base.Result[object]:
                """Create a gauge metric."""
                ...

            def create_histogram(
                self,
                name: str,
                description: str,
                *,
                unit: str = "seconds",
                buckets: list[float] | None = None,
            ) -> p_base.Result[object]:
                """Create a histogram metric."""
                ...

        @runtime_checkable
        class TracingProtocol(p_base.Service[object], Protocol):
            """Protocol for distributed tracing operations."""

            def start_span(
                self,
                operation_name: str,
                *,
                service_name: str | None = None,
                parent_span_id: str | None = None,
            ) -> p_base.Result[object]:
                """Start a new trace span."""
                ...

            def finish_span(
                self,
                span: object,
                *,
                status: str = "ok",
                error: str | None = None,
            ) -> p_base.Result[bool]:
                """Finish a trace span."""
                ...

            def add_span_tag(
                self,
                span: object,
                key: str,
                value: str | float,
            ) -> p_base.Result[bool]:
                """Add tag to trace span."""
                ...

            def get_trace(self, trace_id: str) -> p_base.Result[dict[str, object]]:
                """Get trace by ID."""
                ...

            def search_traces(
                self,
                *,
                service_name: str | None = None,
                operation_name: str | None = None,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> p_base.Result[list[dict[str, object]]]:
                """Search traces by criteria."""
                ...

        @runtime_checkable
        class AlertingProtocol(p_base.Service[object], Protocol):
            """Protocol for alerting and notification operations."""

            def create_alert(
                self,
                message: str,
                level: str,
                *,
                service: str | None = None,
                tags: dict[str, str] | None = None,
            ) -> p_base.Result[str]:
                """Create an alert."""
                ...

            def resolve_alert(self, alert_id: str) -> p_base.Result[bool]:
                """Resolve an alert."""
                ...

            def get_alerts(
                self,
                *,
                level: str | None = None,
                service: str | None = None,
                resolved: bool | None = None,
            ) -> p_base.Result[list[dict[str, object]]]:
                """Get alerts by criteria."""
                ...

            def create_alert_rule(
                self,
                name: str,
                condition: str,
                *,
                threshold: float | None = None,
                duration: int | None = None,
            ) -> p_base.Result[str]:
                """Create an alert rule."""
                ...

        @runtime_checkable
        class HealthCheckProtocol(p_base.Service[object], Protocol):
            """Protocol for health check operations."""

            def check_health(
                self,
                service_name: str,
            ) -> p_base.Result[dict[str, object]]:
                """Perform health check for a service."""
                ...

            def register_health_check(
                self,
                service_name: str,
                check_function: object,
                *,
                interval: int = 60,
            ) -> p_base.Result[bool]:
                """Register a health check."""
                ...

            def get_service_status(
                self,
                service_name: str,
            ) -> p_base.Result[dict[str, object]]:
                """Get service health status."""
                ...

            def get_all_services_status(
                self,
            ) -> p_base.Result[dict[str, object]]:
                """Get health status for all services."""
                ...

        @runtime_checkable
        class LoggingProtocol(p_base.Service[object], Protocol):
            """Protocol for logging operations."""

            def log_message(
                self,
                message: str,
                level: str,
                *,
                service: str | None = None,
                correlation_id: str | None = None,
                extra: dict[str, object] | None = None,
            ) -> p_base.Result[bool]:
                """Log a message."""
                ...

            def get_logs(
                self,
                *,
                level: str | None = None,
                service: str | None = None,
                correlation_id: str | None = None,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> p_base.Result[list[dict[str, object]]]:
                """Get logs by criteria."""
                ...

            def create_logger(
                self,
                name: str,
                *,
                level: str = "info",
                format_string: str | None = None,
            ) -> p_base.Result[object]:
                """Create a logger instance."""
                ...

            def configure_logging(
                self,
                config: dict[str, object],
            ) -> p_base.Result[bool]:
                """Configure logging system."""
                ...

        @runtime_checkable
        class DashboardProtocol(p_base.Service[object], Protocol):
            """Protocol for dashboard and visualization operations."""

            def create_dashboard(
                self,
                name: str,
                description: str,
                *,
                widgets: list[dict[str, object]] | None = None,
            ) -> p_base.Result[str]:
                """Create a dashboard."""
                ...

            def get_dashboard(
                self,
                dashboard_id: str,
            ) -> p_base.Result[dict[str, object]]:
                """Get dashboard by ID."""
                ...

            def add_widget(
                self,
                dashboard_id: str,
                widget_config: dict[str, object],
            ) -> p_base.Result[str]:
                """Add widget to dashboard."""
                ...

            def get_dashboard_data(
                self,
                dashboard_id: str,
                *,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> p_base.Result[dict[str, object]]:
                """Get dashboard data."""
                ...


# Runtime alias for simplified usage
p = FlextObservabilityProtocols

__all__ = [
    "FlextObservabilityProtocols",
    "p",
]
