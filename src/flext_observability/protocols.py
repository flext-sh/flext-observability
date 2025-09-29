"""Observability protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextObservabilityProtocols(FlextProtocols):
    """Observability protocols extending FlextProtocols with observability-specific interfaces.

    This class provides protocol definitions for metrics collection, distributed tracing,
    alerting, health checks, and logging operations within the FLEXT observability platform.
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
            tags: dict[str, str] | None = None,
        ) -> FlextResult[bool]:
            """Record a metric value.

            Args:
                name: Metric name
                value: Metric value
                unit: Metric unit
                tags: Metric tags

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def get_metrics(
            self,
            name_pattern: str | None = None,
            *,
            start_time: str | None = None,
            end_time: str | None = None,
        ) -> FlextResult[list[dict[str, object]]]:
            """Get collected metrics.

            Args:
                name_pattern: Metric name pattern filter
                start_time: Start time filter
                end_time: End time filter

            Returns:
                FlextResult[list[dict[str, object]]]: Metrics data or error

            """
            ...

        def create_counter(
            self, name: str, description: str, *, unit: str = "count"
        ) -> FlextResult[object]:
            """Create a counter metric.

            Args:
                name: Counter name
                description: Counter description
                unit: Counter unit

            Returns:
                FlextResult[object]: Counter instance or error

            """
            ...

        def create_gauge(
            self, name: str, description: str, *, unit: str = "value"
        ) -> FlextResult[object]:
            """Create a gauge metric.

            Args:
                name: Gauge name
                description: Gauge description
                unit: Gauge unit

            Returns:
                FlextResult[object]: Gauge instance or error

            """
            ...

        def create_histogram(
            self,
            name: str,
            description: str,
            *,
            unit: str = "seconds",
            buckets: list[float] | None = None,
        ) -> FlextResult[object]:
            """Create a histogram metric.

            Args:
                name: Histogram name
                description: Histogram description
                unit: Histogram unit
                buckets: Histogram buckets

            Returns:
                FlextResult[object]: Histogram instance or error

            """
            ...

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
            """Start a new trace span.

            Args:
                operation_name: Operation name
                service_name: Service name
                parent_span_id: Parent span ID

            Returns:
                FlextResult[object]: Span instance or error

            """
            ...

        def finish_span(
            self, span: object, *, status: str = "ok", error: str | None = None
        ) -> FlextResult[bool]:
            """Finish a trace span.

            Args:
                span: Span instance
                status: Span status
                error: Error message if any

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def add_span_tag(
            self, span: object, key: str, value: str | float
        ) -> FlextResult[bool]:
            """Add tag to trace span.

            Args:
                span: Span instance
                key: Tag key
                value: Tag value

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def get_trace(self, trace_id: str) -> FlextResult[dict[str, object]]:
            """Get trace by ID.

            Args:
                trace_id: Trace ID

            Returns:
                FlextResult[dict[str, object]]: Trace data or error

            """
            ...

        def search_traces(
            self,
            *,
            service_name: str | None = None,
            operation_name: str | None = None,
            start_time: str | None = None,
            end_time: str | None = None,
        ) -> FlextResult[list[dict[str, object]]]:
            """Search traces by criteria.

            Args:
                service_name: Service name filter
                operation_name: Operation name filter
                start_time: Start time filter
                end_time: End time filter

            Returns:
                FlextResult[list[dict[str, object]]]: Traces data or error

            """
            ...

    @runtime_checkable
    class AlertingProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for alerting and notification operations."""

        def create_alert(
            self,
            message: str,
            level: str,
            *,
            service: str | None = None,
            tags: dict[str, str] | None = None,
        ) -> FlextResult[str]:
            """Create an alert.

            Args:
                message: Alert message
                level: Alert level (info, warning, error, critical)
                service: Service name
                tags: Alert tags

            Returns:
                FlextResult[str]: Alert ID or error

            """
            ...

        def resolve_alert(self, alert_id: str) -> FlextResult[bool]:
            """Resolve an alert.

            Args:
                alert_id: Alert ID

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def get_alerts(
            self,
            *,
            level: str | None = None,
            service: str | None = None,
            resolved: bool | None = None,
        ) -> FlextResult[list[dict[str, object]]]:
            """Get alerts by criteria.

            Args:
                level: Alert level filter
                service: Service name filter
                resolved: Resolved status filter

            Returns:
                FlextResult[list[dict[str, object]]]: Alerts data or error

            """
            ...

        def create_alert_rule(
            self,
            name: str,
            condition: str,
            *,
            threshold: float | None = None,
            duration: int | None = None,
        ) -> FlextResult[str]:
            """Create an alert rule.

            Args:
                name: Rule name
                condition: Alert condition
                threshold: Threshold value
                duration: Duration in seconds

            Returns:
                FlextResult[str]: Rule ID or error

            """
            ...

    @runtime_checkable
    class HealthCheckProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for health check operations."""

        def check_health(self, service_name: str) -> FlextResult[dict[str, object]]:
            """Perform health check for a service.

            Args:
                service_name: Service name

            Returns:
                FlextResult[dict[str, object]]: Health status or error

            """
            ...

        def register_health_check(
            self, service_name: str, check_function: object, *, interval: int = 60
        ) -> FlextResult[bool]:
            """Register a health check.

            Args:
                service_name: Service name
                check_function: Health check function
                interval: Check interval in seconds

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def get_service_status(
            self, service_name: str
        ) -> FlextResult[dict[str, object]]:
            """Get service health status.

            Args:
                service_name: Service name

            Returns:
                FlextResult[dict[str, object]]: Service status or error

            """
            ...

        def get_all_services_status(self) -> FlextResult[dict[str, object]]:
            """Get health status for all services.

            Returns:
                FlextResult[dict[str, object]]: All services status or error

            """
            ...

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
            extra: dict[str, object] | None = None,
        ) -> FlextResult[bool]:
            """Log a message.

            Args:
                message: Log message
                level: Log level (debug, info, warning, error, critical)
                service: Service name
                correlation_id: Correlation ID
                extra: Extra log data

            Returns:
                FlextResult[bool]: Success status

            """
            ...

        def get_logs(
            self,
            *,
            level: str | None = None,
            service: str | None = None,
            correlation_id: str | None = None,
            start_time: str | None = None,
            end_time: str | None = None,
        ) -> FlextResult[list[dict[str, object]]]:
            """Get logs by criteria.

            Args:
                level: Log level filter
                service: Service name filter
                correlation_id: Correlation ID filter
                start_time: Start time filter
                end_time: End time filter

            Returns:
                FlextResult[list[dict[str, object]]]: Logs data or error

            """
            ...

        def create_logger(
            self, name: str, *, level: str = "info", format_string: str | None = None
        ) -> FlextResult[object]:
            """Create a logger instance.

            Args:
                name: Logger name
                level: Log level
                format_string: Log format string

            Returns:
                FlextResult[object]: Logger instance or error

            """
            ...

        def configure_logging(self, config: dict[str, object]) -> FlextResult[bool]:
            """Configure logging system.

            Args:
                config: Logging configuration

            Returns:
                FlextResult[bool]: Success status

            """
            ...

    @runtime_checkable
    class DashboardProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for dashboard and visualization operations."""

        def create_dashboard(
            self,
            name: str,
            description: str,
            *,
            widgets: list[dict[str, object]] | None = None,
        ) -> FlextResult[str]:
            """Create a dashboard.

            Args:
                name: Dashboard name
                description: Dashboard description
                widgets: Dashboard widgets

            Returns:
                FlextResult[str]: Dashboard ID or error

            """
            ...

        def get_dashboard(self, dashboard_id: str) -> FlextResult[dict[str, object]]:
            """Get dashboard by ID.

            Args:
                dashboard_id: Dashboard ID

            Returns:
                FlextResult[dict[str, object]]: Dashboard data or error

            """
            ...

        def add_widget(
            self, dashboard_id: str, widget_config: dict[str, object]
        ) -> FlextResult[str]:
            """Add widget to dashboard.

            Args:
                dashboard_id: Dashboard ID
                widget_config: Widget configuration

            Returns:
                FlextResult[str]: Widget ID or error

            """
            ...

        def get_dashboard_data(
            self,
            dashboard_id: str,
            *,
            start_time: str | None = None,
            end_time: str | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Get dashboard data.

            Args:
                dashboard_id: Dashboard ID
                start_time: Start time filter
                end_time: End time filter

            Returns:
                FlextResult[dict[str, object]]: Dashboard data or error

            """
            ...

    # Convenience aliases for easier downstream usage
    ObservabilityMetricsProtocol = MetricsProtocol
    ObservabilityTracingProtocol = TracingProtocol
    ObservabilityAlertingProtocol = AlertingProtocol
    ObservabilityHealthProtocol = HealthCheckProtocol
    ObservabilityLoggingProtocol = LoggingProtocol
    ObservabilityDashboardProtocol = DashboardProtocol


__all__ = [
    "FlextObservabilityProtocols",
]
