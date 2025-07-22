"""Observability Protocols - Extensibility Interfaces.

Protocols define the contracts for observability components
without requiring inheritance, enabling duck typing and composition.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_core.domain.shared_types import ServiceResult

@runtime_checkable
class ObservabilityProtocol(Protocol):
    """Core protocol for all observability components.

    Defines the minimal interface that all observability
    components must implement for integration.
    """

    async def initialize(self) -> ServiceResult[Any]:
        """Initialize the observability component."""
        ...

    async def shutdown(self) -> ServiceResult[Any]:
        """Gracefully shutdown the component."""
        ...

    def is_healthy(self) -> bool:
        """Check if the component is in a healthy state."""
        ...


@runtime_checkable
class MetricCollectorProtocol(ObservabilityProtocol, Protocol):
    """Protocol for metric collection components.

    Enables different metric collection backends to be
    used interchangeably through a common interface.
    """

    async def record_counter(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> ServiceResult[Any]:
        """Record a counter metric."""
        ...

    async def record_gauge(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> ServiceResult[Any]:
        """Record a gauge metric."""
        ...

    async def record_histogram(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> ServiceResult[Any]:
        """Record a histogram metric."""
        ...

    async def export_metrics(self) -> ServiceResult[Any]:
        """Export collected metrics. Returns count exported."""
        ...


@runtime_checkable
class TraceExporterProtocol(ObservabilityProtocol, Protocol):
    """Protocol for distributed tracing components.

    Enables different tracing backends (Jaeger, Zipkin, etc.)
    to be used through a unified interface.
    """

    async def start_span(
        self,
        name: str,
        parent_id: str | None = None,
    ) -> ServiceResult[Any]:
        """Start a new span. Returns span ID."""
        ...

    async def end_span(
        self,
        span_id: str,
        tags: dict[str, Any] | None = None,
    ) -> ServiceResult[Any]:
        """End a span with optional tags."""
        ...

    async def add_span_event(
        self,
        span_id: str,
        event_name: str,
        attributes: dict[str, Any] | None = None,
    ) -> ServiceResult[Any]:
        """Add an event to a span."""
        ...

    async def export_traces(self) -> ServiceResult[Any]:
        """Export traces. Returns count exported."""
        ...


@runtime_checkable
class LogAggregatorProtocol(ObservabilityProtocol, Protocol):
    """Protocol for log aggregation components.

    Enables different logging backends (Elasticsearch, Splunk, etc.)
    to be used through a common interface.
    """

    async def log_message(
        self,
        level: str,
        message: str,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> ServiceResult[Any]:
        """Log a structured message."""
        ...

    async def log_batch(self, log_entries: Sequence[dict[str, Any]]) -> ServiceResult[Any]:
        """Log a batch of entries efficiently."""
        ...

    async def flush_logs(self) -> ServiceResult[Any]:
        """Flush buffered logs. Returns count flushed."""
        ...


@runtime_checkable
class AlertManagerProtocol(ObservabilityProtocol, Protocol):
    """Protocol for alert management components.

    Enables different alerting systems (PagerDuty, Slack, etc.)
    to be integrated through a common interface.
    """

    async def create_alert_rule(
        self,
        rule_id: str,
        condition: str,
        threshold: float,
        notification_channels: Sequence[str],
    ) -> ServiceResult[Any]:
        """Create a new alert rule."""
        ...

    async def evaluate_rules(self) -> ServiceResult[Any]:
        """Evaluate all rules. Returns list of triggered rule IDs."""
        ...

    async def send_notification(
        self,
        rule_id: str,
        message: str,
        severity: str,
        channels: Sequence[str],
    ) -> ServiceResult[Any]:
        """Send alert notification."""
        ...

    async def acknowledge_alert(self, alert_id: str) -> ServiceResult[Any]:
        """Acknowledge an active alert."""
        ...


@runtime_checkable
class HealthMonitorProtocol(ObservabilityProtocol, Protocol):
    """Protocol for health monitoring components.

    Enables different health monitoring approaches to be
    used through a common interface.
    """

    async def register_check(
        self,
        component_name: str,
        check_func: Any,
    ) -> ServiceResult[Any]:
        """Register a health check function."""
        ...

    async def run_checks(self) -> ServiceResult[Any]:
        """Run all registered health checks."""
        ...

    async def get_health_status(self) -> ServiceResult[Any]:
        """Get overall health status with details."""
        ...


@runtime_checkable
class ObservabilityBackendProtocol(Protocol):
    """Protocol for observability backend integrations.

    Unifies different observability platforms (Datadog, New Relic, etc.)
    under a common interface for vendor-agnostic implementations.
    """

    metrics: MetricCollectorProtocol
    traces: TraceExporterProtocol
    logs: LogAggregatorProtocol
    alerts: AlertManagerProtocol
    health: HealthMonitorProtocol

    async def connect(self) -> ServiceResult[Any]:
        """Connect to the observability backend."""
        ...

    async def disconnect(self) -> ServiceResult[Any]:
        """Disconnect from the observability backend."""
        ...

    def is_connected(self) -> bool:
        """Check if connected to the backend."""
        ...
