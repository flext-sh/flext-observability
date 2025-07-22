"""Observability Core Abstractions - Fundamental Interface Definitions.

Provides the most basic abstractions for observability components,
building upon flext_core.foundation patterns.
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_core import ResultPattern


class ObservabilityError(Exception):
    """Base exception for observability operations."""


# Type variables for observability abstractions
TMetric = TypeVar("TMetric")
TTrace = TypeVar("TTrace")
TLog = TypeVar("TLog")
TAlert = TypeVar("TAlert")


class ObservabilityAbstraction(abc.ABC):
    """Base abstraction for all observability components.

    🎯 PRINCIPLES:
    - Technology-agnostic interfaces
    - Composable and extensible
    - Type-safe operations
    - Non-blocking by default
    """

    @abc.abstractmethod
    async def initialize(self) -> ResultPattern[None, ObservabilityError]:
        """Initialize the observability component."""

    @abc.abstractmethod
    async def shutdown(self) -> ResultPattern[None, ObservabilityError]:
        """Gracefully shutdown the component."""

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Check if the component is in a healthy state."""


class AbstractMetricCollector[TMetric](ObservabilityAbstraction):
    """Base abstraction for metric collection.

    Metrics collectors gather quantitative measurements
    about system behavior and performance.

    🎯 PRINCIPLES:
    - High-frequency, low-latency collection
    - Buffered and batched export
    - Configurable sampling
    - Memory-efficient storage
    """

    @abc.abstractmethod
    async def collect_metric(self, metric: TMetric) -> ResultPattern[None, ObservabilityError]:
        """Collect a single metric."""

    @abc.abstractmethod
    async def collect_batch(self, metrics: Sequence[TMetric]) -> ResultPattern[None, ObservabilityError]:
        """Collect a batch of metrics efficiently."""

    @abc.abstractmethod
    async def export_metrics(self) -> ResultPattern[int, ObservabilityError]:
        """Export collected metrics to backend. Returns count exported."""


class AbstractTraceExporter[TTrace](ObservabilityAbstraction):
    """Base abstraction for distributed tracing.

    Trace exporters handle the collection and export of
    distributed tracing spans and traces.

    🎯 PRINCIPLES:
    - Low-overhead instrumentation
    - Asynchronous export
    - Context propagation
    - Sampling strategies
    """

    @abc.abstractmethod
    async def start_trace(self, trace_id: str, operation_name: str) -> ResultPattern[TTrace, ObservabilityError]:
        """Start a new trace."""

    @abc.abstractmethod
    async def end_trace(self, trace: TTrace) -> ResultPattern[None, ObservabilityError]:
        """End a trace and prepare for export."""

    @abc.abstractmethod
    async def export_traces(self) -> ResultPattern[int, ObservabilityError]:
        """Export traces to backend. Returns count exported."""


class AbstractLogAggregator[TLog](ObservabilityAbstraction):
    """Base abstraction for log aggregation.

    Log aggregators collect, structure, and forward
    application logs to centralized storage.

    🎯 PRINCIPLES:
    - Structured logging support
    - Asynchronous processing
    - Configurable filtering
    - Correlation with traces
    """

    @abc.abstractmethod
    async def log_entry(self, log: TLog) -> ResultPattern[None, ObservabilityError]:
        """Process a single log entry."""

    @abc.abstractmethod
    async def log_batch(self, logs: Sequence[TLog]) -> ResultPattern[None, ObservabilityError]:
        """Process a batch of log entries."""

    @abc.abstractmethod
    async def flush_logs(self) -> ResultPattern[int, ObservabilityError]:
        """Flush buffered logs to backend. Returns count flushed."""


class AbstractAlertManager[TAlert](ObservabilityAbstraction):
    """Base abstraction for alert management.

    Alert managers evaluate metrics and traces against
    rules and trigger notifications when thresholds are exceeded.

    🎯 PRINCIPLES:
    - Rule-based evaluation
    - Multi-channel notifications
    - Alert suppression and grouping
    - Escalation policies
    """

    @abc.abstractmethod
    async def evaluate_alert(self, alert_rule: Any) -> ResultPattern[bool, ObservabilityError]:
        """Evaluate an alert rule. Returns True if alert should fire."""

    @abc.abstractmethod
    async def trigger_alert(self, alert: TAlert) -> ResultPattern[None, ObservabilityError]:
        """Trigger an alert notification."""

    @abc.abstractmethod
    async def suppress_alert(self, alert_id: str) -> ResultPattern[None, ObservabilityError]:
        """Suppress an active alert."""


class AbstractHealthMonitor(ObservabilityAbstraction):
    """Base abstraction for health monitoring.

    Health monitors perform periodic checks on system
    components and report overall system health status.

    🎯 PRINCIPLES:
    - Periodic health checks
    - Component dependency tracking
    - Cascading failure detection
    - Health status aggregation
    """

    @abc.abstractmethod
    async def check_component_health(self, component_name: str) -> ResultPattern[bool, ObservabilityError]:
        """Check health of a specific component."""

    @abc.abstractmethod
    async def get_overall_health(self) -> ResultPattern[dict[str, Any], ObservabilityError]:
        """Get overall system health status."""

    @abc.abstractmethod
    async def register_health_check(self, component_name: str, check_func: Any) -> ResultPattern[None, ObservabilityError]:
        """Register a health check function for a component."""
