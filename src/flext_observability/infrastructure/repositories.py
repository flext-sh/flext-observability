"""In-memory implementations of repositories for testing and development."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.config.base import injectable
from flext_observability.infrastructure.ports import AlertRepository
from flext_observability.infrastructure.ports import HealthRepository
from flext_observability.infrastructure.ports import LogRepository
from flext_observability.infrastructure.ports import MetricsRepository
from flext_observability.infrastructure.ports import TraceRepository

if TYPE_CHECKING:
    from datetime import datetime

    from flext_observability.domain.entities import Alert
    from flext_observability.domain.entities import HealthCheck
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace
    from flext_observability.domain.value_objects import AlertSeverity
    from flext_observability.domain.value_objects import ComponentName
    from flext_observability.domain.value_objects import HealthStatus
    from flext_observability.domain.value_objects import LogLevel
    from flext_observability.domain.value_objects import MetricType
    from flext_observability.domain.value_objects import TraceStatus

# Constants
MAX_METRICS_PER_NAME = 1000


@injectable()
class InMemoryMetricsRepository(MetricsRepository):
    """In-memory metrics repository for testing."""

    def __init__(self) -> None:
        self._metrics: list[Metric] = []
        self._metrics_by_name: dict[str, list[Metric]] = {}

    async def save(self, metric: Metric) -> Metric:
        """Save a metric."""
        self._metrics.append(metric)
        if metric.name not in self._metrics_by_name:
            self._metrics_by_name[metric.name] = []
        self._metrics_by_name[metric.name].append(metric)

        # Keep only last MAX_METRICS_PER_NAME metrics per name
        if len(self._metrics_by_name[metric.name]) > MAX_METRICS_PER_NAME:
            self._metrics_by_name[metric.name] = self._metrics_by_name[
                metric.name
            ][-MAX_METRICS_PER_NAME:]

        return metric

    async def get_by_id(self, metric_id: str) -> Metric | None:
        """Get metric by ID."""
        return next((m for m in self._metrics if str(m.id) == metric_id), None)

    async def find_by_name(self, name: str, limit: int = 100) -> list[Metric]:
        """Find metrics by name."""
        metrics = self._metrics_by_name.get(name, [])
        return sorted(metrics, key=lambda m: m.timestamp, reverse=True)[:limit]

    async def find_by_criteria(
        self,
        component_name: str | None = None,
        metric_type: MetricType | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> list[Metric]:
        """Find metrics by criteria."""
        filtered_metrics = []

        for metric in self._metrics:
            # Filter by component name
            if component_name and metric.component.name != component_name:
                continue

            # Filter by metric type
            if metric_type and metric.metric_type != metric_type:
                continue

            # Filter by time range
            if start_time and metric.timestamp < start_time:
                continue
            if end_time and metric.timestamp > end_time:
                continue

            filtered_metrics.append(metric)

        # Sort by timestamp (newest first) and limit
        filtered_metrics.sort(key=lambda m: m.timestamp, reverse=True)
        return filtered_metrics[:limit]

    async def delete_older_than(self, cutoff_time: datetime) -> int:
        """Delete metrics older than cutoff time."""
        to_delete = []
        for metric in self._metrics:
            if metric.timestamp < cutoff_time:
                to_delete.append(metric)

        for metric in to_delete:
            self._metrics.remove(metric)
            # Remove from name index
            if metric.name in self._metrics_by_name:
                self._metrics_by_name[metric.name] = [
                    m for m in self._metrics_by_name[metric.name]
                    if m.id != metric.id
                ]

        return len(to_delete)


@injectable(AlertRepository)
class InMemoryAlertRepository(AlertRepository):
    """In-memory implementation of alert repository."""

    def __init__(self) -> None:
        self._alerts: dict[str, Alert] = {}

    async def save(self, alert: Alert) -> Alert:
        """Save an alert."""
        self._alerts[str(alert.id)] = alert
        return alert

    async def get_by_id(self, alert_id: str) -> Alert | None:
        """Get alert by ID."""
        return self._alerts.get(alert_id)

    async def find_active(
        self,
        severity: AlertSeverity | None = None,
        component_name: str | None = None,
        limit: int = 50,
    ) -> list[Alert]:
        """Find active alerts."""
        filtered_alerts = []

        for alert in self._alerts.values():
            # Only active alerts
            if not alert.is_active:
                continue

            # Filter by severity
            if severity and alert.severity != severity:
                continue

            # Filter by component name
            if component_name and alert.metric.component.name != component_name:
                continue

            filtered_alerts.append(alert)

        # Sort by timestamp (newest first) and limit
        filtered_alerts.sort(key=lambda a: a.created_at, reverse=True)
        return filtered_alerts[:limit]

    async def find_by_criteria(
        self,
        severity: AlertSeverity | None = None,
        component_name: str | None = None,
        acknowledged: bool | None = None,
        resolved: bool | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> list[Alert]:
        """Find alerts by criteria."""
        filtered_alerts = []

        for alert in self._alerts.values():
            # Filter by severity
            if severity and alert.severity != severity:
                continue

            # Filter by component name
            if component_name and alert.metric.component.name != component_name:
                continue

            # Filter by acknowledged status
            if acknowledged is not None and alert.acknowledged != acknowledged:
                continue

            # Filter by resolved status
            if resolved is not None and alert.resolved != resolved:
                continue

            # Filter by time range
            if start_time and alert.created_at < start_time:
                continue
            if end_time and alert.created_at > end_time:
                continue

            filtered_alerts.append(alert)

        # Sort by timestamp (newest first) and limit
        filtered_alerts.sort(key=lambda a: a.created_at, reverse=True)
        return filtered_alerts[:limit]

    async def count_active(self) -> int:
        """Count active alerts."""
        return sum(1 for alert in self._alerts.values() if alert.is_active)


@injectable(HealthRepository)
class InMemoryHealthRepository(HealthRepository):
    """In-memory implementation of health repository."""

    def __init__(self) -> None:
        self._health_checks: dict[str, HealthCheck] = {}
        self._latest_by_component: dict[str, HealthCheck] = {}

    async def save(self, health_check: HealthCheck) -> HealthCheck:
        """Save a health check."""
        self._health_checks[str(health_check.id)] = health_check

        # Update latest by component
        component_key = health_check.component.full_name
        self._latest_by_component[component_key] = health_check

        return health_check

    async def get_by_id(self, health_check_id: str) -> HealthCheck | None:
        """Get health check by ID."""
        return self._health_checks.get(health_check_id)

    async def get_latest_by_component(
        self, component: ComponentName | None = None,
    ) -> list[HealthCheck]:
        """Get latest health check for each component."""
        if component:
            health_check = self._latest_by_component.get(component.full_name)
            return [health_check] if health_check else []

        return list(self._latest_by_component.values())

    async def find_by_criteria(
        self,
        component_name: str | None = None,
        status: HealthStatus | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> list[HealthCheck]:
        """Find health checks by criteria."""
        filtered_checks = []

        for health_check in self._health_checks.values():
            # Filter by component name
            if component_name and health_check.component.name != component_name:
                continue

            # Filter by status
            if status and health_check.status != status:
                continue

            # Filter by time range
            if start_time and health_check.created_at < start_time:
                continue
            if end_time and health_check.created_at > end_time:
                continue

            filtered_checks.append(health_check)

        # Sort by timestamp (newest first) and limit
        filtered_checks.sort(key=lambda h: h.created_at, reverse=True)
        return filtered_checks[:limit]

    async def delete_older_than(self, cutoff_time: datetime) -> int:
        """Delete health checks older than cutoff time."""
        to_delete = []
        for check_id, health_check in self._health_checks.items():
            if health_check.created_at < cutoff_time:
                to_delete.append(check_id)

        for check_id in to_delete:
            health_check = self._health_checks.pop(check_id)
            # Remove from latest index if this was the latest
            component_key = health_check.component.full_name
            if (component_key in self._latest_by_component and
                self._latest_by_component[component_key].id == health_check.id):
                del self._latest_by_component[component_key]

        return len(to_delete)


@injectable(LogRepository)
class InMemoryLogRepository(LogRepository):
    """In-memory implementation of log repository."""

    def __init__(self) -> None:
        self._logs: list[LogEntry] = []

    async def save(self, log_entry: LogEntry) -> LogEntry:
        """Save a log entry."""
        self._logs.append(log_entry)
        return log_entry

    async def get_by_id(self, log_id: str) -> LogEntry | None:
        """Get log entry by ID."""
        return next((log for log in self._logs if str(log.id) == log_id), None)

    async def find_by_criteria(
        self,
        level: LogLevel | None = None,
        component_name: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        search: str | None = None,
        limit: int = 100,
    ) -> list[LogEntry]:
        """Find log entries by criteria."""
        filtered_logs = []

        for log_entry in self._logs:
            # Filter by level
            if level and log_entry.level != level:
                continue

            # Filter by component name
            if component_name and log_entry.component.name != component_name:
                continue

            # Filter by time range
            if start_time and log_entry.created_at < start_time:
                continue
            if end_time and log_entry.created_at > end_time:
                continue

            # Filter by search term
            if search and search.lower() not in log_entry.message.lower():
                continue

            filtered_logs.append(log_entry)

        # Sort by timestamp (newest first) and limit
        filtered_logs.sort(key=lambda l: l.created_at, reverse=True)
        return filtered_logs[:limit]

    async def count_by_level(self, level: LogLevel) -> int:
        """Count log entries by level."""
        return sum(1 for log_entry in self._logs if log_entry.level == level)

    async def delete_older_than(self, cutoff_time: datetime) -> int:
        """Delete log entries older than cutoff time."""
        to_delete = []
        for log_entry in self._logs:
            if log_entry.created_at < cutoff_time:
                to_delete.append(log_entry)

        for log_entry in to_delete:
            self._logs.remove(log_entry)

        return len(to_delete)


@injectable(TraceRepository)
class InMemoryTraceRepository(TraceRepository):
    """In-memory implementation of trace repository."""

    def __init__(self) -> None:
        self._traces: dict[str, Trace] = {}
        self._traces_by_trace_id: dict[str, Trace] = {}

    async def save(self, trace: Trace) -> Trace:
        """Save a trace."""
        self._traces[str(trace.id)] = trace
        self._traces_by_trace_id[trace.trace_id.trace_id] = trace
        return trace

    async def get_by_id(self, trace_id: str) -> Trace | None:
        """Get trace by ID."""
        return self._traces.get(trace_id)

    async def get_by_trace_id(self, trace_id: str) -> Trace | None:
        """Get trace by trace ID."""
        return self._traces_by_trace_id.get(trace_id)

    async def find_by_criteria(
        self,
        operation_name: str | None = None,
        component_name: str | None = None,
        status: TraceStatus | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> list[Trace]:
        """Find traces by criteria."""
        filtered_traces = []

        for trace in self._traces.values():
            # Filter by operation name
            if operation_name and trace.operation_name != operation_name:
                continue

            # Filter by component name
            if component_name and trace.component.name != component_name:
                continue

            # Filter by status
            if status and trace.status != status:
                continue

            # Filter by time range
            if start_time and trace.start_time < start_time:
                continue
            if end_time and trace.start_time > end_time:
                continue

            filtered_traces.append(trace)

        # Sort by timestamp (newest first) and limit
        filtered_traces.sort(key=lambda t: t.start_time, reverse=True)
        return filtered_traces[:limit]

    async def get_operation_names(self) -> list[str]:
        """Get all operation names."""
        operation_names = set()
        operation_names.update(trace.operation_name for trace in self._traces.values())
        return sorted(operation_names)

    async def delete_older_than(self, cutoff_time: datetime) -> int:
        """Delete traces older than cutoff time."""
        to_delete = []
        for trace_id, trace in self._traces.items():
            if trace.start_time < cutoff_time:
                to_delete.append(trace_id)

        for trace_id in to_delete:
            trace = self._traces.pop(trace_id)
            # Remove from trace_id index
            self._traces_by_trace_id.pop(trace.trace_id.trace_id, None)

        return len(to_delete)
