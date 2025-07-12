"""Repository implementations for FLEXT-OBSERVABILITY persistence.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from flext_core.domain.types import ServiceResult
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
        """Initialize the in-memory log repository."""
        super().__init__()
        self.storage: dict[UUID, LogEntry] = {}

    async def save(self, log_entry: LogEntry) -> ServiceResult[LogEntry]:
        """Save a log entry to the repository.

        Args:
            log_entry: The log entry to save.

        Returns:
            The saved log entry.

        """
        try:
            self.storage[log_entry.id] = log_entry
            return ServiceResult.ok(log_entry)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save log entry: {e}")

    async def get_by_id(self, log_id: UUID) -> ServiceResult[LogEntry | None]:
        """Get a log entry by ID.

        Args:
            log_id: The ID of the log entry to retrieve.

        Returns:
            The log entry if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(log_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get log entry: {e}")

    async def get_all(self) -> list[LogEntry]:
        """Get all log entries.

        Returns:
            List of all log entries.

        """
        return list(self.storage.values())

    async def find_by_filters(
        self,
        filters: dict[str, Any],
        limit: int = 100,
    ) -> list[LogEntry]:
        """Find log entries by filters.

        Args:
            filters: Dictionary of filters to apply.
            limit: Maximum number of entries to return.

        Returns:
            List of log entries matching the filters.

        """
        results = []
        for log_entry in self.storage.values():
            if self._matches_filters(log_entry, filters):
                results.append(log_entry)
                if len(results) >= limit:
                    break
        return results

    async def count_by_level(self, level: str) -> int:
        """Count log entries by level.

        Args:
            level: The log level to count.

        Returns:
            Number of log entries at the specified level.

        """
        return sum(1 for log_entry in self.storage.values() if log_entry.level == level)

    async def delete_by_id(self, log_id: UUID) -> bool:
        """Delete a log entry by ID.

        Args:
            log_id: The ID of the log entry to delete.

        Returns:
            True if the entry was deleted, False if not found.

        """
        if log_id in self.storage:
            del self.storage[log_id]
            return True
        return False

    def _matches_filters(self, log_entry: LogEntry, filters: dict[str, Any]) -> bool:
        """Check if a log entry matches the given filters.

        Args:
            log_entry: The log entry to check.
            filters: Dictionary of filters to apply.

        Returns:
            True if the entry matches all filters, False otherwise.

        """
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
        """Initialize the in-memory metrics repository."""
        super().__init__()
        self.storage: dict[UUID, Metric] = {}

    async def save(self, metric: Metric) -> ServiceResult[Metric]:
        """Save a metric to the repository.

        Args:
            metric: The metric to save.

        Returns:
            The saved metric.

        """
        try:
            self.storage[metric.id] = metric
            return ServiceResult.ok(metric)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save metric: {e}")

    async def get_by_id(self, metric_id: UUID) -> ServiceResult[Metric | None]:
        """Get a metric by ID.

        Args:
            metric_id: The ID of the metric to retrieve.

        Returns:
            The metric if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(metric_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get metric: {e}")

    async def get_all(self) -> list[Metric]:
        """Get all metrics.

        Returns:
            List of all metrics.

        """
        return list(self.storage.values())

    async def find_by_name(self, name: str) -> list[Metric]:
        """Find metrics by name.

        Args:
            name: The name of the metrics to find.

        Returns:
            List of metrics with the specified name.

        """
        return [metric for metric in self.storage.values() if metric.name == name]

    async def find_by_type(self, metric_type: str) -> list[Metric]:
        """Find metrics by type.

        Args:
            metric_type: The type of metrics to find.

        Returns:
            List of metrics with the specified type.

        """
        return [
            metric
            for metric in self.storage.values()
            if metric.metric_type == metric_type
        ]

    async def find_by_labels(self, labels: dict[str, str]) -> list[Metric]:
        """Find metrics by labels.

        Args:
            labels: Dictionary of labels to match.

        Returns:
            List of metrics matching all the specified labels.

        """
        return [
            metric
            for metric in self.storage.values()
            if all(metric.labels.get(key) == value for key, value in labels.items())
        ]

    async def delete_by_id(self, metric_id: UUID) -> bool:
        """Delete a metric by ID.

        Args:
            metric_id: The ID of the metric to delete.

        Returns:
            True if the metric was deleted, False if not found.

        """
        if metric_id in self.storage:
            del self.storage[metric_id]
            return True
        return False

    async def get_latest_by_name(self, name: str) -> Metric | None:
        """Get the latest metric by name.

        Args:
            name: The name of the metric to find.

        Returns:
            The most recent metric with the specified name, or None if not found.

        """
        metrics = await self.find_by_name(name)
        if not metrics:
            return None
        return max(metrics, key=lambda m: m.timestamp)


class InMemoryTraceRepository(InMemoryRepository[Trace]):
    """Repository for traces."""

    def __init__(self) -> None:
        """Initialize the in-memory trace repository."""
        super().__init__()
        self.storage: dict[UUID, Trace] = {}

    async def save(self, trace: Trace) -> ServiceResult[Trace]:
        """Save a trace to the repository.

        Args:
            trace: The trace to save.

        Returns:
            The saved trace.

        """
        try:
            self.storage[trace.id] = trace
            return ServiceResult.ok(trace)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save trace: {e}")

    async def get_by_id(self, trace_id: UUID) -> ServiceResult[Trace | None]:
        """Get a trace by ID.

        Args:
            trace_id: The ID of the trace to retrieve.

        Returns:
            The trace if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(trace_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get trace: {e}")

    async def get_all(self) -> list[Trace]:
        """Get all traces.

        Returns:
            List of all traces.

        """
        return list(self.storage.values())

    async def find_by_trace_id(self, trace_id: str) -> list[Trace]:
        """Find traces by trace ID.

        Args:
            trace_id: The trace ID to search for.

        Returns:
            List of traces with the specified trace ID.

        """
        return [trace for trace in self.storage.values() if trace.trace_id == trace_id]

    async def find_by_operation(self, operation_name: str) -> list[Trace]:
        """Find traces by operation name.

        Args:
            operation_name: The operation name to search for.

        Returns:
            List of traces with the specified operation name.

        """
        return [
            trace
            for trace in self.storage.values()
            if trace.operation_name == operation_name
        ]

    async def find_by_service(self, service_name: str) -> list[Trace]:
        """Find traces by service name.

        Args:
            service_name: The service name to search for.

        Returns:
            List of traces with the specified service name.

        """
        return [
            trace
            for trace in self.storage.values()
            if trace.service_name == service_name
        ]

    async def find_by_status(self, status: str) -> list[Trace]:
        """Find traces by status.

        Args:
            status: The status to search for.

        Returns:
            List of traces with the specified status.

        """
        return [
            trace for trace in self.storage.values() if trace.trace_status == status
        ]

    async def find_active_traces(self) -> list[Trace]:
        """Find active (unfinished) traces.

        Returns:
            List of traces that are still active.

        """
        return [trace for trace in self.storage.values() if not trace.is_finished]

    async def delete_by_id(self, trace_id: UUID) -> bool:
        """Delete a trace by ID.

        Args:
            trace_id: The ID of the trace to delete.

        Returns:
            True if the trace was deleted, False if not found.

        """
        if trace_id in self.storage:
            del self.storage[trace_id]
            return True
        return False

    async def get_operation_names(self) -> list[str]:
        """Get all unique operation names.

        Returns:
            Sorted list of unique operation names.

        """
        return list({trace.operation_name for trace in self.storage.values()})


class InMemoryAlertRepository(InMemoryRepository[Alert]):
    """Repository for alerts."""

    def __init__(self) -> None:
        """Initialize the in-memory alert repository."""
        super().__init__()
        self.storage: dict[UUID, Alert] = {}

    async def save(self, alert: Alert) -> ServiceResult[Alert]:
        """Save an alert to the repository.

        Args:
            alert: The alert to save.

        Returns:
            The saved alert.

        """
        try:
            self.storage[alert.id] = alert
            return ServiceResult.ok(alert)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save alert: {e}")

    async def get_by_id(self, alert_id: UUID) -> ServiceResult[Alert | None]:
        """Get an alert by ID.

        Args:
            alert_id: The ID of the alert to retrieve.

        Returns:
            The alert if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(alert_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get alert: {e}")

    async def get_all(self) -> list[Alert]:
        """Get all alerts.

        Returns:
            List of all alerts.

        """
        return list(self.storage.values())

    async def find_active(self) -> list[Alert]:
        """Find active (unresolved) alerts.

        Returns:
            List of alerts that are not resolved.

        """
        return [alert for alert in self.storage.values() if not alert.is_resolved]

    async def find_by_severity(self, severity: str) -> list[Alert]:
        """Find alerts by severity.

        Args:
            severity: The severity level to search for.

        Returns:
            List of alerts with the specified severity.

        """
        return [alert for alert in self.storage.values() if alert.severity == severity]

    async def find_by_source(self, source: str) -> list[Alert]:
        """Find alerts by source.

        Args:
            source: The source to search for.

        Returns:
            List of alerts from the specified source.

        """
        return [alert for alert in self.storage.values() if alert.source == source]

    async def find_critical_alerts(self) -> list[Alert]:
        """Find critical alerts.

        Returns:
            List of alerts marked as critical.

        """
        return [alert for alert in self.storage.values() if alert.is_critical]

    async def find_high_priority_alerts(self) -> list[Alert]:
        """Find high priority alerts.

        Returns:
            List of alerts marked as high priority.

        """
        return [alert for alert in self.storage.values() if alert.is_high_priority]

    async def find_unacknowledged_alerts(self) -> list[Alert]:
        """Find unacknowledged alerts.

        Returns:
            List of alerts that have not been acknowledged.

        """
        return [alert for alert in self.storage.values() if not alert.is_acknowledged]

    async def delete_by_id(self, alert_id: UUID) -> bool:
        """Delete an alert by ID.

        Args:
            alert_id: The ID of the alert to delete.

        Returns:
            True if the alert was deleted, False if not found.

        """
        if alert_id in self.storage:
            del self.storage[alert_id]
            return True
        return False

    async def count_active(self) -> int:
        """Count active alerts.

        Returns:
            Number of active alerts.

        """
        return len(await self.find_active())

    async def count_by_severity(self, severity: str) -> int:
        """Count alerts by severity.

        Args:
            severity: The severity level to count.

        Returns:
            Number of alerts with the specified severity.

        """
        return len(await self.find_by_severity(severity))


class InMemoryHealthRepository(InMemoryRepository[HealthCheck]):
    """Repository for health checks."""

    def __init__(self) -> None:
        """Initialize the in-memory health repository."""
        super().__init__()
        self.storage: dict[UUID, HealthCheck] = {}

    async def save(self, health_check: HealthCheck) -> ServiceResult[HealthCheck]:
        """Save a health check to the repository.

        Args:
            health_check: The health check to save.

        Returns:
            The saved health check.

        """
        try:
            self.storage[health_check.id] = health_check
            return ServiceResult.ok(health_check)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save health check: {e}")

    async def get_by_id(
        self, health_check_id: UUID
    ) -> ServiceResult[HealthCheck | None]:
        """Get a health check by ID.

        Args:
            health_check_id: The ID of the health check to retrieve.

        Returns:
            The health check if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(health_check_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get health check: {e}")

    async def get_all(self) -> list[HealthCheck]:
        """Get all health checks.

        Returns:
            List of all health checks.

        """
        return list(self.storage.values())

    async def find_by_name(self, name: str) -> list[HealthCheck]:
        """Find health checks by name.

        Args:
            name: The name to search for.

        Returns:
            List of health checks with the specified name.

        """
        return [hc for hc in self.storage.values() if hc.name == name]

    async def find_by_type(self, check_type: str) -> list[HealthCheck]:
        """Find health checks by type.

        Args:
            check_type: The check type to search for.

        Returns:
            List of health checks with the specified type.

        """
        return [hc for hc in self.storage.values() if hc.check_type == check_type]

    async def find_healthy(self) -> list[HealthCheck]:
        """Find healthy checks.

        Returns:
            List of health checks that are healthy.

        """
        return [hc for hc in self.storage.values() if hc.is_healthy]

    async def find_failing(self) -> list[HealthCheck]:
        """Find failing health checks.

        Returns:
            List of health checks that are failing.

        """
        return [hc for hc in self.storage.values() if hc.is_failing]

    async def find_critical(self) -> list[HealthCheck]:
        """Find critical health checks.

        Returns:
            List of health checks that are critical.

        """
        return [hc for hc in self.storage.values() if hc.is_critical]

    async def find_warning(self) -> list[HealthCheck]:
        """Find warning health checks.

        Returns:
            List of health checks that are in warning state.

        """
        return [hc for hc in self.storage.values() if hc.is_warning]

    async def get_latest_by_name(self, name: str) -> HealthCheck | None:
        """Get the latest health check by name.

        Args:
            name: The name of the health check to find.

        Returns:
            The most recent health check with the specified name, or None if not found.

        """
        checks = await self.find_by_name(name)
        if not checks:
            return None
        return max(checks, key=lambda hc: hc.last_check_at or hc.created_at)

    async def delete_by_id(self, health_check_id: UUID) -> bool:
        """Delete a health check by ID.

        Args:
            health_check_id: The ID of the health check to delete.

        Returns:
            True if the health check was deleted, False if not found.

        """
        if health_check_id in self.storage:
            del self.storage[health_check_id]
            return True
        return False


class InMemoryDashboardRepository(InMemoryRepository[Dashboard]):
    """Repository for dashboards."""

    def __init__(self) -> None:
        """Initialize the in-memory dashboard repository."""
        super().__init__()
        self.storage: dict[UUID, Dashboard] = {}

    async def save(self, dashboard: Dashboard) -> ServiceResult[Dashboard]:
        """Save a dashboard to the repository.

        Args:
            dashboard: The dashboard to save.

        Returns:
            The saved dashboard.

        """
        try:
            self.storage[dashboard.id] = dashboard
            return ServiceResult.ok(dashboard)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save dashboard: {e}")

    async def get_by_id(self, dashboard_id: UUID) -> ServiceResult[Dashboard | None]:
        """Get a dashboard by ID.

        Args:
            dashboard_id: The ID of the dashboard to retrieve.

        Returns:
            The dashboard if found, None otherwise.

        """
        try:
            return ServiceResult.ok(self.storage.get(dashboard_id))
        except Exception as e:
            return ServiceResult.fail(f"Failed to get dashboard: {e}")

    async def get_all(self) -> list[Dashboard]:
        """Get all dashboards.

        Returns:
            List of all dashboards.

        """
        return list(self.storage.values())

    async def find_by_title(self, title: str) -> list[Dashboard]:
        """Find dashboards by title.

        Args:
            title: The title to search for.

        Returns:
            List of dashboards with the specified title.

        """
        return [
            dashboard for dashboard in self.storage.values() if dashboard.title == title
        ]

    async def find_by_category(self, category: str) -> list[Dashboard]:
        """Find dashboards by category.

        Args:
            category: The category to search for.

        Returns:
            List of dashboards in the specified category.

        """
        return [
            dashboard
            for dashboard in self.storage.values()
            if dashboard.category == category
        ]

    async def find_public(self) -> list[Dashboard]:
        """Find public dashboards.

        Returns:
            List of dashboards that are public.

        """
        return [dashboard for dashboard in self.storage.values() if dashboard.is_public]

    async def find_shared(self) -> list[Dashboard]:
        """Find shared dashboards.

        Returns:
            List of dashboards that are shared.

        """
        return [dashboard for dashboard in self.storage.values() if dashboard.is_shared]

    async def find_by_tags(self, tags: list[str]) -> list[Dashboard]:
        """Find dashboards by tags.

        Args:
            tags: List of tags to search for.

        Returns:
            List of dashboards that have any of the specified tags.

        """
        return [
            dashboard
            for dashboard in self.storage.values()
            if any(tag in dashboard.tags for tag in tags)
        ]

    async def find_auto_refreshing(self) -> list[Dashboard]:
        """Find auto-refreshing dashboards.

        Returns:
            List of dashboards that are set to auto-refresh.

        """
        return [
            dashboard
            for dashboard in self.storage.values()
            if dashboard.is_auto_refreshing
        ]

    async def delete_by_id(self, dashboard_id: UUID) -> bool:
        """Delete a dashboard by ID.

        Args:
            dashboard_id: The ID of the dashboard to delete.

        Returns:
            True if the dashboard was deleted, False if not found.

        """
        if dashboard_id in self.storage:
            del self.storage[dashboard_id]
            return True
        return False

    async def search_by_title(self, query: str) -> list[Dashboard]:
        """Search dashboards by title.

        Args:
            query: The search query to match against titles.

        Returns:
            List of dashboards whose titles contain the query (case-insensitive).

        """
        query_lower = query.lower()
        return [
            dashboard
            for dashboard in self.storage.values()
            if query_lower in dashboard.title.lower()
        ]

    async def get_widget_count(self, dashboard_id: UUID) -> int:
        """Get the widget count for a dashboard.

        Args:
            dashboard_id: The ID of the dashboard.

        Returns:
            Number of widgets in the dashboard, or 0 if not found.

        """
        result = await self.get_by_id(dashboard_id)
        if result.is_success and result.data:
            return len(result.data.widgets) if hasattr(result.data, "widgets") else 0
        return 0
