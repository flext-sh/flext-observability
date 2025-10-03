"""Observability protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextObservabilityProtocols:
    """Unified observability protocols following FLEXT domain extension pattern.

    This class consolidates observability and monitoring protocols while explicitly
    re-exporting foundation protocols for backward compatibility and clean access.

    Architecture:
        - RE-EXPORTS: Foundation protocols from flext-core for unified access
        - EXTENDS: Observability-specific protocols in Observability namespace
        - MAINTAINS: Zero breaking changes through explicit re-export pattern

    Usage:
        from flext_observability.protocols import FlextObservabilityProtocols

        # Foundation access (re-exported)
        FlextObservabilityProtocols.Foundation.ResultProtocol

        # Observability-specific access
        FlextObservabilityProtocols.Observability.MetricsProtocol
    """

    # =========================================================================
    # FOUNDATION PROTOCOL RE-EXPORTS (from flext-core)
    # =========================================================================
    # Explicitly re-export foundation protocols for unified access.
    # This maintains backward compatibility while providing clean namespace access.

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

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
        class MetricsProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for metrics collection and management operations."""

            def record_metric(
                self,
                name: str,
                value: float,
                *,
                unit: str = "count",
                tags: FlextTypes.StringDict | None = None,
            ) -> FlextResult[bool]:
                """Record a metric value."""

            def get_metrics(
                self,
                name_pattern: str | None = None,
                *,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> FlextResult[list[FlextTypes.Dict]]:
                """Get collected metrics."""

            def create_counter(
                self, name: str, description: str, *, unit: str = "count"
            ) -> FlextResult[object]:
                """Create a counter metric."""

            def create_gauge(
                self, name: str, description: str, *, unit: str = "value"
            ) -> FlextResult[object]:
                """Create a gauge metric."""

            def create_histogram(
                self,
                name: str,
                description: str,
                *,
                unit: str = "seconds",
                buckets: FlextTypes.FloatList | None = None,
            ) -> FlextResult[object]:
                """Create a histogram metric."""

        @runtime_checkable
        class TracingProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for distributed tracing operations."""

            def start_span(
                self,
                operation_name: str,
                *,
                service_name: str | None = None,
                parent_span_id: str | None = None,
            ) -> FlextResult[object]:
                """Start a new trace span."""

            def finish_span(
                self, span: object, *, status: str = "ok", error: str | None = None
            ) -> FlextResult[bool]:
                """Finish a trace span."""

            def add_span_tag(
                self, span: object, key: str, value: str | float
            ) -> FlextResult[bool]:
                """Add tag to trace span."""

            def get_trace(self, trace_id: str) -> FlextResult[FlextTypes.Dict]:
                """Get trace by ID."""

            def search_traces(
                self,
                *,
                service_name: str | None = None,
                operation_name: str | None = None,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> FlextResult[list[FlextTypes.Dict]]:
                """Search traces by criteria."""

        @runtime_checkable
        class AlertingProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for alerting and notification operations."""

            def create_alert(
                self,
                message: str,
                level: str,
                *,
                service: str | None = None,
                tags: FlextTypes.StringDict | None = None,
            ) -> FlextResult[str]:
                """Create an alert."""

            def resolve_alert(self, alert_id: str) -> FlextResult[bool]:
                """Resolve an alert."""

            def get_alerts(
                self,
                *,
                level: str | None = None,
                service: str | None = None,
                resolved: bool | None = None,
            ) -> FlextResult[list[FlextTypes.Dict]]:
                """Get alerts by criteria."""

            def create_alert_rule(
                self,
                name: str,
                condition: str,
                *,
                threshold: float | None = None,
                duration: int | None = None,
            ) -> FlextResult[str]:
                """Create an alert rule."""

        @runtime_checkable
        class HealthCheckProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for health check operations."""

            def check_health(self, service_name: str) -> FlextResult[FlextTypes.Dict]:
                """Perform health check for a service."""

            def register_health_check(
                self, service_name: str, check_function: object, *, interval: int = 60
            ) -> FlextResult[bool]:
                """Register a health check."""

            def get_service_status(
                self, service_name: str
            ) -> FlextResult[FlextTypes.Dict]:
                """Get service health status."""

            def get_all_services_status(self) -> FlextResult[FlextTypes.Dict]:
                """Get health status for all services."""

        @runtime_checkable
        class LoggingProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for logging operations."""

            def log_message(
                self,
                message: str,
                level: str,
                *,
                service: str | None = None,
                correlation_id: str | None = None,
                extra: FlextTypes.Dict | None = None,
            ) -> FlextResult[bool]:
                """Log a message."""

            def get_logs(
                self,
                *,
                level: str | None = None,
                service: str | None = None,
                correlation_id: str | None = None,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> FlextResult[list[FlextTypes.Dict]]:
                """Get logs by criteria."""

            def create_logger(
                self,
                name: str,
                *,
                level: str = "info",
                format_string: str | None = None,
            ) -> FlextResult[object]:
                """Create a logger instance."""

            def configure_logging(self, config: FlextTypes.Dict) -> FlextResult[bool]:
                """Configure logging system."""

        @runtime_checkable
        class DashboardProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for dashboard and visualization operations."""

            def create_dashboard(
                self,
                name: str,
                description: str,
                *,
                widgets: list[FlextTypes.Dict] | None = None,
            ) -> FlextResult[str]:
                """Create a dashboard."""

            def get_dashboard(self, dashboard_id: str) -> FlextResult[FlextTypes.Dict]:
                """Get dashboard by ID."""

            def add_widget(
                self, dashboard_id: str, widget_config: FlextTypes.Dict
            ) -> FlextResult[str]:
                """Add widget to dashboard."""

            def get_dashboard_data(
                self,
                dashboard_id: str,
                *,
                start_time: str | None = None,
                end_time: str | None = None,
            ) -> FlextResult[FlextTypes.Dict]:
                """Get dashboard data."""

    # =========================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =========================================================================
    # Maintain existing attribute names for zero breaking changes.

    MetricsProtocol = Observability.MetricsProtocol
    TracingProtocol = Observability.TracingProtocol
    AlertingProtocol = Observability.AlertingProtocol
    HealthCheckProtocol = Observability.HealthCheckProtocol
    LoggingProtocol = Observability.LoggingProtocol
    DashboardProtocol = Observability.DashboardProtocol

    # Additional convenience aliases
    ObservabilityMetricsProtocol = Observability.MetricsProtocol
    ObservabilityTracingProtocol = Observability.TracingProtocol
    ObservabilityAlertingProtocol = Observability.AlertingProtocol
    ObservabilityHealthProtocol = Observability.HealthCheckProtocol
    ObservabilityLoggingProtocol = Observability.LoggingProtocol
    ObservabilityDashboardProtocol = Observability.DashboardProtocol


__all__ = [
    "FlextObservabilityProtocols",
]
