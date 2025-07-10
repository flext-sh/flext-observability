"""Application handlers for FLEXT-OBSERVABILITY - v0.7.0.

REFACTORED: Using flext-core modern patterns - NO duplication.
Command/Query handlers with ServiceResult pattern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from flext_core.application.handlers import CommandHandler as BaseCommandHandler
from flext_core.domain.types import ServiceResult
from flext_observability.domain.entities import Alert
from flext_observability.domain.entities import Dashboard
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.entities import LogEntry
from flext_observability.domain.entities import Metric
from flext_observability.domain.entities import Trace

if TYPE_CHECKING:
    from uuid import UUID

    from flext_observability.domain.ports import AlertService
    from flext_observability.domain.ports import DashboardService
    from flext_observability.domain.ports import HealthService
    from flext_observability.domain.ports import LogService
    from flext_observability.domain.ports import MetricsService
    from flext_observability.domain.ports import TracingService
    from flext_observability.infrastructure.persistence.repositories import (
        AlertRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        DashboardRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        HealthRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        LogRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        MetricsRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        TracingRepository,
    )


class LogHandler(BaseCommandHandler):
    """Log entry command handler."""

    def __init__(
        self,
        log_repository: LogRepository,
        log_service: LogService,
    ) -> None:
        self.log_repository = log_repository
        self.log_service = log_service

    async def handle(self, *args, **kwargs) -> ServiceResult[Any]:
        """Base handle method."""
        return ServiceResult.success(None)

    async def create_log_entry(
        self,
        level: str,
        message: str,
        logger_name: str,
        module: str | None = None,
        function: str | None = None,
        line_number: int | None = None,
        extra: dict[str, Any] | None = None,
    ) -> ServiceResult[LogEntry]:
        """Create a new log entry."""
        try:
            log_entry = LogEntry(
                level=level,
                message=message,
                logger_name=logger_name,
                module=module,
                function=function,
                line_number=line_number,
                extra=extra or {},
            )

            # Save to repository
            saved_entry = await self.log_repository.save(log_entry)

            # Send to log service
            await self.log_service.write_log(saved_entry)

            return ServiceResult.success(saved_entry)
        except Exception as e:
            return ServiceResult.error(f"Failed to create log entry: {e}")

    async def get_log_entry(self, entry_id: UUID) -> ServiceResult[LogEntry]:
        """Get log entry by ID."""
        try:
            entry = await self.log_repository.get_by_id(entry_id)
            if not entry:
                return ServiceResult.error("Log entry not found")
            return ServiceResult.success(entry)
        except Exception as e:
            return ServiceResult.error(f"Failed to get log entry: {e}")

    async def search_logs(
        self,
        level: str | None = None,
        logger_name: str | None = None,
        message_contains: str | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[LogEntry]]:
        """Search log entries."""
        try:
            filters = {}
            if level:
                filters["level"] = level
            if logger_name:
                filters["logger_name"] = logger_name
            if message_contains:
                filters["message__contains"] = message_contains

            entries = await self.log_repository.find_by_filters(filters, limit=limit)
            return ServiceResult.success(entries)
        except Exception as e:
            return ServiceResult.error(f"Failed to search logs: {e}")


class MetricsHandler(BaseCommandHandler):
    """Metrics command handler."""

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_service: MetricsService,
    ) -> None:
        self.metrics_repository = metrics_repository
        self.metrics_service = metrics_service

    async def record_metric(
        self,
        name: str,
        value: float,
        metric_type: str = "gauge",
        unit: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> ServiceResult[Metric]:
        """Record a new metric."""
        try:
            metric = Metric(
                name=name,
                value=value,
                type=metric_type,
                unit=unit,
                labels=labels or {},
            )

            # Save to repository
            saved_metric = await self.metrics_repository.save(metric)

            # Send to metrics service
            await self.metrics_service.record_metric(saved_metric)

            return ServiceResult.success(saved_metric)
        except Exception as e:
            return ServiceResult.error(f"Failed to record metric: {e}")

    async def get_metric(self, metric_id: UUID) -> ServiceResult[Metric]:
        """Get metric by ID."""
        try:
            metric = await self.metrics_repository.get_by_id(metric_id)
            if not metric:
                return ServiceResult.error("Metric not found")
            return ServiceResult.success(metric)
        except Exception as e:
            return ServiceResult.error(f"Failed to get metric: {e}")

    async def get_metrics_by_name(self, name: str) -> ServiceResult[list[Metric]]:
        """Get metrics by name."""
        try:
            metrics = await self.metrics_repository.find_by_name(name)
            return ServiceResult.success(metrics)
        except Exception as e:
            return ServiceResult.error(f"Failed to get metrics: {e}")

    async def get_current_metrics(self) -> ServiceResult[dict[str, Any]]:
        """Get current metrics from service."""
        try:
            metrics = await self.metrics_service.get_current_metrics()
            return ServiceResult.success(metrics)
        except Exception as e:
            return ServiceResult.error(f"Failed to get current metrics: {e}")


class TracingHandler(BaseCommandHandler):
    """Tracing command handler."""

    def __init__(
        self,
        tracing_repository: TracingRepository,
        tracing_service: TracingService,
    ) -> None:
        self.tracing_repository = tracing_repository
        self.tracing_service = tracing_service

    async def start_trace(
        self,
        trace_id: str,
        span_id: str,
        operation_name: str,
        service_name: str,
        parent_span_id: str | None = None,
    ) -> ServiceResult[Trace]:
        """Start a new trace."""
        try:
            trace = Trace(
                trace_id=trace_id,
                span_id=span_id,
                operation_name=operation_name,
                service_name=service_name,
                parent_span_id=parent_span_id,
            )

            # Start trace
            trace.start()

            # Save to repository
            saved_trace = await self.tracing_repository.save(trace)

            # Send to tracing service
            await self.tracing_service.start_trace(saved_trace)

            return ServiceResult.success(saved_trace)
        except Exception as e:
            return ServiceResult.error(f"Failed to start trace: {e}")

    async def finish_trace(self, trace_id: UUID) -> ServiceResult[Trace]:
        """Finish a trace."""
        try:
            trace = await self.tracing_repository.get_by_id(trace_id)
            if not trace:
                return ServiceResult.error("Trace not found")

            # Finish trace
            trace.finish()

            # Update repository
            updated_trace = await self.tracing_repository.save(trace)

            # Send to tracing service
            await self.tracing_service.finish_trace(updated_trace)

            return ServiceResult.success(updated_trace)
        except Exception as e:
            return ServiceResult.error(f"Failed to finish trace: {e}")

    async def get_trace(self, trace_id: UUID) -> ServiceResult[Trace]:
        """Get trace by ID."""
        try:
            trace = await self.tracing_repository.get_by_id(trace_id)
            if not trace:
                return ServiceResult.error("Trace not found")
            return ServiceResult.success(trace)
        except Exception as e:
            return ServiceResult.error(f"Failed to get trace: {e}")


class AlertHandler(BaseCommandHandler):
    """Alert command handler."""

    def __init__(
        self,
        alert_repository: AlertRepository,
        alert_service: AlertService,
    ) -> None:
        self.alert_repository = alert_repository
        self.alert_service = alert_service

    async def create_alert(
        self,
        title: str,
        source: str,
        source_type: str,
        condition: str,
        severity: str = "medium",
        description: str | None = None,
        threshold: float | None = None,
    ) -> ServiceResult[Alert]:
        """Create a new alert."""
        try:
            alert = Alert(
                title=title,
                source=source,
                source_type=source_type,
                condition=condition,
                severity=severity,
                description=description,
                threshold=threshold,
            )

            # Save to repository
            saved_alert = await self.alert_repository.save(alert)

            # Send to alert service
            await self.alert_service.send_alert(saved_alert)

            return ServiceResult.success(saved_alert)
        except Exception as e:
            return ServiceResult.error(f"Failed to create alert: {e}")

    async def resolve_alert(self, alert_id: UUID) -> ServiceResult[Alert]:
        """Resolve an alert."""
        try:
            alert = await self.alert_repository.get_by_id(alert_id)
            if not alert:
                return ServiceResult.error("Alert not found")

            # Resolve alert
            alert.resolve()

            # Update repository
            updated_alert = await self.alert_repository.save(alert)

            # Send to alert service
            await self.alert_service.resolve_alert(updated_alert)

            return ServiceResult.success(updated_alert)
        except Exception as e:
            return ServiceResult.error(f"Failed to resolve alert: {e}")

    async def get_active_alerts(self) -> ServiceResult[list[Alert]]:
        """Get active alerts."""
        try:
            alerts = await self.alert_repository.find_active()
            return ServiceResult.success(alerts)
        except Exception as e:
            return ServiceResult.error(f"Failed to get active alerts: {e}")


class HealthHandler(BaseCommandHandler):
    """Health check command handler."""

    def __init__(
        self,
        health_repository: HealthRepository,
        health_service: HealthService,
    ) -> None:
        self.health_repository = health_repository
        self.health_service = health_service

    async def create_health_check(
        self,
        name: str,
        check_type: str,
        endpoint: str | None = None,
        timeout_seconds: int = 5,
    ) -> ServiceResult[HealthCheck]:
        """Create a new health check."""
        try:
            health_check = HealthCheck(
                name=name,
                check_type=check_type,
                endpoint=endpoint,
                timeout_seconds=timeout_seconds,
            )

            # Save to repository
            saved_check = await self.health_repository.save(health_check)

            return ServiceResult.success(saved_check)
        except Exception as e:
            return ServiceResult.error(f"Failed to create health check: {e}")

    async def run_health_check(self, check_id: UUID) -> ServiceResult[HealthCheck]:
        """Run a health check."""
        try:
            health_check = await self.health_repository.get_by_id(check_id)
            if not health_check:
                return ServiceResult.error("Health check not found")

            # Run check
            result = await self.health_service.run_check(health_check)

            # Update check with result
            if result.is_success:
                health_check.record_success(
                    result.data["response_time_ms"], result.data.get("response_data"),
                )
            else:
                health_check.record_failure(result.error)

            # Update repository
            updated_check = await self.health_repository.save(health_check)

            return ServiceResult.success(updated_check)
        except Exception as e:
            return ServiceResult.error(f"Failed to run health check: {e}")

    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health."""
        try:
            health = await self.health_service.get_system_health()
            return ServiceResult.success(health)
        except Exception as e:
            return ServiceResult.error(f"Failed to get system health: {e}")


class DashboardHandler(BaseCommandHandler):
    """Dashboard command handler."""

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        dashboard_service: DashboardService,
    ) -> None:
        self.dashboard_repository = dashboard_repository
        self.dashboard_service = dashboard_service

    async def create_dashboard(
        self,
        title: str,
        description: str | None = None,
        refresh_interval_seconds: int = 30,
    ) -> ServiceResult[Dashboard]:
        """Create a new dashboard."""
        try:
            dashboard = Dashboard(
                title=title,
                description=description,
                refresh_interval_seconds=refresh_interval_seconds,
            )

            # Save to repository
            saved_dashboard = await self.dashboard_repository.save(dashboard)

            return ServiceResult.success(saved_dashboard)
        except Exception as e:
            return ServiceResult.error(f"Failed to create dashboard: {e}")

    async def get_dashboard(self, dashboard_id: UUID) -> ServiceResult[Dashboard]:
        """Get dashboard by ID."""
        try:
            dashboard = await self.dashboard_repository.get_by_id(dashboard_id)
            if not dashboard:
                return ServiceResult.error("Dashboard not found")
            return ServiceResult.success(dashboard)
        except Exception as e:
            return ServiceResult.error(f"Failed to get dashboard: {e}")

    async def render_dashboard(
        self, dashboard_id: UUID,
    ) -> ServiceResult[dict[str, Any]]:
        """Render dashboard with current data."""
        try:
            dashboard = await self.dashboard_repository.get_by_id(dashboard_id)
            if not dashboard:
                return ServiceResult.error("Dashboard not found")

            # Render dashboard
            rendered = await self.dashboard_service.render_dashboard(dashboard)

            return ServiceResult.success(rendered)
        except Exception as e:
            return ServiceResult.error(f"Failed to render dashboard: {e}")

    async def get_all_dashboards(self) -> ServiceResult[list[Dashboard]]:
        """Get all dashboards."""
        try:
            dashboards = await self.dashboard_repository.get_all()
            return ServiceResult.success(dashboards)
        except Exception as e:
            return ServiceResult.error(f"Failed to get dashboards: {e}")
