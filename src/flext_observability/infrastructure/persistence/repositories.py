"""Repository implementations for FLEXT-OBSERVABILITY persistence.

Using flext-core repository patterns - NO duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from flext_observability.domain.entities import Alert
from flext_observability.domain.entities import Dashboard
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.entities import LogEntry
from flext_observability.domain.entities import Metric
from flext_observability.domain.entities import Trace
from flext_observability.infrastructure.persistence.base import InMemoryRepository

if TYPE_CHECKING:
    from uuid import UUID


class InMemoryLogRepository(InMemoryRepository[LogEntry]):
    """Repository for log entries."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, LogEntry] = {}

    async def save(self, log_entry: LogEntry) -> LogEntry:
        """Save log entry."""
        self.storage[log_entry.id] = log_entry
        return log_entry

    async def get_by_id(self, log_id: UUID) -> LogEntry | None:
        """Get log entry by ID."""
        return self.storage.get(log_id)

    async def get_all(self) -> list[LogEntry]:
        """Get all log entries."""
        return list(self.storage.values())

    async def find_by_filters(
        self, filters: dict[str, Any], limit: int = 100,
    ) -> list[LogEntry]:
        """Find log entries by filters."""
        results = []
        for log_entry in self.storage.values():
            if self._matches_filters(log_entry, filters):
                results.append(log_entry)
                if len(results) >= limit:
                    break
        return results

    async def count_by_level(self, level: str) -> int:
        """Count log entries by level."""
        return sum(1 for log_entry in self.storage.values() if log_entry.level == level)

    async def delete_by_id(self, log_id: UUID) -> bool:
        """Delete log entry by ID."""
        if log_id in self.storage:
            del self.storage[log_id]
            return True
        return False

    def _matches_filters(self, log_entry: LogEntry, filters: dict[str, Any]) -> bool:
        """Check if log entry matches filters."""
        for key, value in filters.items():
            if key == "level" and log_entry.level != value:
                return False
            if key == "logger_name" and log_entry.logger_name != value:
                return False
            if key == "message__contains" and value not in log_entry.message:
                return False
            if key == "correlation_id" and log_entry.correlation_id != value:
                return False
            if key == "user_id" and log_entry.user_id != value:
                return False
        return True


class InMemoryMetricsRepository(InMemoryRepository[Metric]):
    """Repository for metrics."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, Metric] = {}

    async def save(self, metric: Metric) -> Metric:
        """Save metric."""
        self.storage[metric.id] = metric
        return metric

    async def get_by_id(self, metric_id: UUID) -> Metric | None:
        """Get metric by ID."""
        return self.storage.get(metric_id)

    async def get_all(self) -> list[Metric]:
        """Get all metrics."""
        return list(self.storage.values())

    async def find_by_name(self, name: str) -> list[Metric]:
        """Find metrics by name."""
        return [metric for metric in self.storage.values() if metric.name == name]

    async def find_by_type(self, metric_type: str) -> list[Metric]:
        """Find metrics by type."""
        return [
            metric for metric in self.storage.values() if metric.type == metric_type
        ]

    async def find_by_labels(self, labels: dict[str, str]) -> list[Metric]:
        """Find metrics by labels."""
        results = []
        for metric in self.storage.values():
            if all(metric.labels.get(key) == value for key, value in labels.items()):
                results.append(metric)
        return results

    async def delete_by_id(self, metric_id: UUID) -> bool:
        """Delete metric by ID."""
        if metric_id in self.storage:
            del self.storage[metric_id]
            return True
        return False

    async def get_latest_by_name(self, name: str) -> Metric | None:
        """Get latest metric by name."""
        metrics = await self.find_by_name(name)
        if not metrics:
            return None
        return max(metrics, key=lambda m: m.timestamp)


class InMemoryTraceRepository(InMemoryRepository[Trace]):
    """Repository for traces."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, Trace] = {}

    async def save(self, trace: Trace) -> Trace:
        """Save trace."""
        self.storage[trace.id] = trace
        return trace

    async def get_by_id(self, trace_id: UUID) -> Trace | None:
        """Get trace by ID."""
        return self.storage.get(trace_id)

    async def get_all(self) -> list[Trace]:
        """Get all traces."""
        return list(self.storage.values())

    async def find_by_trace_id(self, trace_id: str) -> list[Trace]:
        """Find traces by trace ID."""
        return [trace for trace in self.storage.values() if trace.trace_id == trace_id]

    async def find_by_operation(self, operation_name: str) -> list[Trace]:
        """Find traces by operation name."""
        return [
            trace
            for trace in self.storage.values()
            if trace.operation_name == operation_name
        ]

    async def find_by_service(self, service_name: str) -> list[Trace]:
        """Find traces by service name."""
        return [
            trace
            for trace in self.storage.values()
            if trace.service_name == service_name
        ]

    async def find_by_status(self, status: str) -> list[Trace]:
        """Find traces by status."""
        return [trace for trace in self.storage.values() if trace.status == status]

    async def find_active_traces(self) -> list[Trace]:
        """Find active (unfinished) traces."""
        return [trace for trace in self.storage.values() if not trace.is_finished]

    async def delete_by_id(self, trace_id: UUID) -> bool:
        """Delete trace by ID."""
        if trace_id in self.storage:
            del self.storage[trace_id]
            return True
        return False

    async def get_operation_names(self) -> list[str]:
        """Get all unique operation names."""
        return list({trace.operation_name for trace in self.storage.values()})


class InMemoryAlertRepository(InMemoryRepository[Alert]):
    """Repository for alerts."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, Alert] = {}

    async def save(self, alert: Alert) -> Alert:
        """Save alert."""
        self.storage[alert.id] = alert
        return alert

    async def get_by_id(self, alert_id: UUID) -> Alert | None:
        """Get alert by ID."""
        return self.storage.get(alert_id)

    async def get_all(self) -> list[Alert]:
        """Get all alerts."""
        return list(self.storage.values())

    async def find_active(self) -> list[Alert]:
        """Find active alerts."""
        return [alert for alert in self.storage.values() if not alert.is_resolved]

    async def find_by_severity(self, severity: str) -> list[Alert]:
        """Find alerts by severity."""
        return [alert for alert in self.storage.values() if alert.severity == severity]

    async def find_by_source(self, source: str) -> list[Alert]:
        """Find alerts by source."""
        return [alert for alert in self.storage.values() if alert.source == source]

    async def find_critical_alerts(self) -> list[Alert]:
        """Find critical alerts."""
        return [alert for alert in self.storage.values() if alert.is_critical]

    async def find_high_priority_alerts(self) -> list[Alert]:
        """Find high priority alerts."""
        return [alert for alert in self.storage.values() if alert.is_high_priority]

    async def find_unacknowledged_alerts(self) -> list[Alert]:
        """Find unacknowledged alerts."""
        return [alert for alert in self.storage.values() if not alert.is_acknowledged]

    async def delete_by_id(self, alert_id: UUID) -> bool:
        """Delete alert by ID."""
        if alert_id in self.storage:
            del self.storage[alert_id]
            return True
        return False

    async def count_active(self) -> int:
        """Count active alerts."""
        return len(await self.find_active())

    async def count_by_severity(self, severity: str) -> int:
        """Count alerts by severity."""
        return len(await self.find_by_severity(severity))


class InMemoryHealthRepository(InMemoryRepository[HealthCheck]):
    """Repository for health checks."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, HealthCheck] = {}

    async def save(self, health_check: HealthCheck) -> HealthCheck:
        """Save health check."""
        self.storage[health_check.id] = health_check
        return health_check

    async def get_by_id(self, health_check_id: UUID) -> HealthCheck | None:
        """Get health check by ID."""
        return self.storage.get(health_check_id)

    async def get_all(self) -> list[HealthCheck]:
        """Get all health checks."""
        return list(self.storage.values())

    async def find_by_name(self, name: str) -> list[HealthCheck]:
        """Find health checks by name."""
        return [hc for hc in self.storage.values() if hc.name == name]

    async def find_by_type(self, check_type: str) -> list[HealthCheck]:
        """Find health checks by type."""
        return [hc for hc in self.storage.values() if hc.check_type == check_type]

    async def find_healthy(self) -> list[HealthCheck]:
        """Find healthy checks."""
        return [hc for hc in self.storage.values() if hc.is_healthy]

    async def find_failing(self) -> list[HealthCheck]:
        """Find failing checks."""
        return [hc for hc in self.storage.values() if hc.is_failing]

    async def find_critical(self) -> list[HealthCheck]:
        """Find critical health checks."""
        return [hc for hc in self.storage.values() if hc.is_critical]

    async def find_warning(self) -> list[HealthCheck]:
        """Find warning health checks."""
        return [hc for hc in self.storage.values() if hc.is_warning]

    async def get_latest_by_name(self, name: str) -> HealthCheck | None:
        """Get latest health check by name."""
        checks = await self.find_by_name(name)
        if not checks:
            return None
        return max(checks, key=lambda hc: hc.last_check_at or hc.created_at)

    async def delete_by_id(self, health_check_id: UUID) -> bool:
        """Delete health check by ID."""
        if health_check_id in self.storage:
            del self.storage[health_check_id]
            return True
        return False


class InMemoryDashboardRepository(InMemoryRepository[Dashboard]):
    """Repository for dashboards."""

    def __init__(self) -> None:
        super().__init__()
        self.storage: dict[UUID, Dashboard] = {}

    async def save(self, dashboard: Dashboard) -> Dashboard:
        """Save dashboard."""
        self.storage[dashboard.id] = dashboard
        return dashboard

    async def get_by_id(self, dashboard_id: UUID) -> Dashboard | None:
        """Get dashboard by ID."""
        return self.storage.get(dashboard_id)

    async def get_all(self) -> list[Dashboard]:
        """Get all dashboards."""
        return list(self.storage.values())

    async def find_by_title(self, title: str) -> list[Dashboard]:
        """Find dashboards by title."""
        return [
            dashboard for dashboard in self.storage.values() if dashboard.title == title
        ]

    async def find_by_category(self, category: str) -> list[Dashboard]:
        """Find dashboards by category."""
        return [
            dashboard
            for dashboard in self.storage.values()
            if dashboard.category == category
        ]

    async def find_public(self) -> list[Dashboard]:
        """Find public dashboards."""
        return [dashboard for dashboard in self.storage.values() if dashboard.is_public]

    async def find_shared(self) -> list[Dashboard]:
        """Find shared dashboards."""
        return [dashboard for dashboard in self.storage.values() if dashboard.is_shared]

    async def find_by_tags(self, tags: list[str]) -> list[Dashboard]:
        """Find dashboards by tags."""
        results = []
        for dashboard in self.storage.values():
            if any(tag in dashboard.tags for tag in tags):
                results.append(dashboard)
        return results

    async def find_auto_refreshing(self) -> list[Dashboard]:
        """Find auto-refreshing dashboards."""
        return [
            dashboard
            for dashboard in self.storage.values()
            if dashboard.is_auto_refreshing
        ]

    async def delete_by_id(self, dashboard_id: UUID) -> bool:
        """Delete dashboard by ID."""
        if dashboard_id in self.storage:
            del self.storage[dashboard_id]
            return True
        return False

    async def search_by_title(self, query: str) -> list[Dashboard]:
        """Search dashboards by title."""
        query_lower = query.lower()
        return [
            dashboard
            for dashboard in self.storage.values()
            if query_lower in dashboard.title.lower()
        ]

    async def get_widget_count(self, dashboard_id: UUID) -> int:
        """Get widget count for dashboard."""
        dashboard = await self.get_by_id(dashboard_id)
        return dashboard.widget_count if dashboard else 0
