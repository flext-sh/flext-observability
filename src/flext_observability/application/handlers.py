"""Application handlers for observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
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
        InMemoryAlertRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        InMemoryDashboardRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        InMemoryHealthRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        InMemoryLogRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        InMemoryMetricsRepository,
    )
    from flext_observability.infrastructure.persistence.repositories import (
        InMemoryTraceRepository,
    )

    # Type aliases for cleaner code
    AlertRepository = InMemoryAlertRepository
    DashboardRepository = InMemoryDashboardRepository
    HealthRepository = InMemoryHealthRepository
    LogRepository = InMemoryLogRepository
    MetricsRepository = InMemoryMetricsRepository
    TracingRepository = InMemoryTraceRepository


class LogHandler(BaseCommandHandler):
    """Log entry command handler."""

    def __init__(self, log_repository: LogRepository, log_service: LogService) -> None:
        """Initialize log handler.

        Args:
            log_repository: Repository for storing log entries.
            log_service: Service for handling log operations.

        """
        self.log_repository = log_repository
        self.log_service = log_service

    async def handle(self) -> ServiceResult[Any]:
        """Handle generic command.

        Returns:
            Success result.

        """
        return ServiceResult.success(None)

    async def create_log_entry(
        self,
        level: str,
        message: str,
        logger_name: str,
        extra: dict[str, Any] | None = None,
    ) -> ServiceResult[LogEntry]:
        """Create a new log entry.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            message: Log message.
            logger_name: Name of the logger.
            extra: Additional data including module, function, line_number (optional).

        Returns:
            Service result containing the created log entry.

        """
        try:
            extra_data = extra or {}
            log_entry = LogEntry(
                level=level,
                message=message,
                logger_name=logger_name,
                module=extra_data.get("module"),
                function=extra_data.get("function"),
                line_number=extra_data.get("line_number"),
                extra=extra_data,
            )

            # Save to repository
            saved_entry = await self.log_repository.save(log_entry)

            # Send to log service
            await self.log_service.write_log(saved_entry)  # type: ignore[arg-type]

            return ServiceResult.success(saved_entry)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create log entry: {e}")

    async def get_log_entry(self, entry_id: UUID) -> ServiceResult[LogEntry]:
        """Get a log entry by ID.

        Args:
            entry_id: The ID of the log entry to retrieve.

        Returns:
            Service result containing the log entry.

        """
        try:
            entry = await self.log_repository.get_by_id(entry_id)
            if not entry:
                return ServiceResult.fail("Log entry not found")
            return ServiceResult.success(entry)  # type: ignore[arg-type]
        except (ValueError, TypeError, KeyError) as e:
            return ServiceResult.fail(f"Failed to get log entry: {e}")

    async def search_logs(
        self,
        level: str | None = None,
        logger_name: str | None = None,
        message_contains: str | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[LogEntry]]:
        """Search log entries by criteria.

        Args:
            level: Log level filter (optional).
            logger_name: Logger name filter (optional).
            message_contains: Message content filter (optional).
            limit: Maximum number of entries to return.

        Returns:
            Service result containing matching log entries.

        """
        try:
            # Use find_by_criteria method instead of find_by_filters
            entries = await self.log_repository.find_by_criteria(  # type: ignore[attr-defined]
                level=level,
                component_name=logger_name,
                search=message_contains,
                limit=limit,
            )
            return ServiceResult.success(entries)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to search logs: {e}")


class MetricsHandler(BaseCommandHandler):
    """Metrics command handler."""

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_service: MetricsService,
    ) -> None:
        """Initialize metrics handler.

        Args:
            metrics_repository: Repository for storing metrics.
            metrics_service: Service for handling metrics operations.

        """
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
        """Record a new metric.

        Args:
            name: The name of the metric.
            value: The metric value.
            metric_type: The type of metric (gauge, counter, histogram, etc.).
            unit: The unit of measurement (optional).
            labels: Additional labels for the metric (optional).

        Returns:
            Service result containing the recorded metric.

        """
        try:
            from flext_observability.domain.value_objects import ComponentName

            metric = Metric(
                name=name,
                value=value,
                metric_type=metric_type,
                unit=unit,
                labels=labels or {},
                component=ComponentName(name="default"),
            )

            # Save to repository
            saved_metric = await self.metrics_repository.save(metric)

            # Send to metrics service
            await self.metrics_service.record_metric(saved_metric)  # type: ignore[arg-type]

            return ServiceResult.success(saved_metric)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to record metric: {e}")

    async def get_metric(self, metric_id: UUID) -> ServiceResult[Metric]:
        """Get a metric by ID.

        Args:
            metric_id: The ID of the metric to retrieve.

        Returns:
            Service result containing the metric.

        """
        try:
            metric = await self.metrics_repository.get_by_id(metric_id)
            if not metric:
                return ServiceResult.fail("Metric not found")
            return ServiceResult.success(metric)  # type: ignore[arg-type]
        except (ValueError, TypeError, KeyError) as e:
            return ServiceResult.fail(f"Failed to get metric: {e}")

    async def get_metrics_by_name(self, name: str) -> ServiceResult[list[Metric]]:
        """Get all metrics with a specific name.

        Args:
            name: The name of the metrics to retrieve.

        Returns:
            Service result containing the list of metrics.

        """
        try:
            metrics = await self.metrics_repository.find_by_name(name)
            return ServiceResult.success(metrics)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get metrics: {e}")

    async def get_current_metrics(self) -> ServiceResult[dict[str, Any]]:
        """Get current metrics data.

        Returns:
            Service result containing current metrics data.

        """
        try:
            metrics = await self.metrics_service.get_current_metrics()
            return ServiceResult.success(metrics)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get current metrics: {e}")


class TracingHandler(BaseCommandHandler):
    """Tracing command handler."""

    def __init__(
        self,
        tracing_repository: TracingRepository,
        tracing_service: TracingService,
    ) -> None:
        """Initialize tracing handler.

        Args:
            tracing_repository: Repository for storing traces.
            tracing_service: Service for handling tracing operations.

        """
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
        """Start a new trace.

        Args:
            trace_id: The unique trace identifier.
            span_id: The unique span identifier.
            operation_name: The name of the operation being traced.
            service_name: The name of the service.
            parent_span_id: The parent span ID (optional for root spans).

        Returns:
            Service result containing the started trace.

        """
        try:
            from flext_observability.domain.value_objects import ComponentName

            trace = Trace(
                trace_id=trace_id,
                span_id=span_id,
                operation_name=operation_name,
                service_name=service_name,
                parent_span_id=parent_span_id,
                component=ComponentName(name=service_name),
            )

            # Start trace
            trace.start()

            # Save to repository
            saved_trace = await self.tracing_repository.save(trace)

            # Send to tracing service
            await self.tracing_service.start_trace(saved_trace)  # type: ignore[arg-type]

            return ServiceResult.success(saved_trace)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to start trace: {e}")

    async def finish_trace(self, trace_id: UUID) -> ServiceResult[Trace]:
        """Finish an existing trace.

        Args:
            trace_id: The ID of the trace to finish.

        Returns:
            Service result containing the finished trace.

        """
        try:
            trace = await self.tracing_repository.get_by_id(trace_id)
            if not trace:
                return ServiceResult.fail("Trace not found")

            # Finish trace
            trace.finish()  # type: ignore[attr-defined]

            # Update repository
            updated_trace = await self.tracing_repository.save(trace)  # type: ignore[arg-type]

            # Send to tracing service
            await self.tracing_service.finish_trace(updated_trace)  # type: ignore[arg-type]

            return ServiceResult.success(updated_trace)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to finish trace: {e}")

    async def get_trace(self, trace_id: UUID) -> ServiceResult[Trace]:
        """Get a trace by ID.

        Args:
            trace_id: The ID of the trace to retrieve.

        Returns:
            Service result containing the trace.

        """
        try:
            trace = await self.tracing_repository.get_by_id(trace_id)
            if not trace:
                return ServiceResult.fail("Trace not found")
            return ServiceResult.success(trace)  # type: ignore[arg-type]
        except (ValueError, TypeError, KeyError) as e:
            return ServiceResult.fail(f"Failed to get trace: {e}")


class AlertHandler(BaseCommandHandler):
    """Alert command handler."""

    def __init__(
        self,
        alert_repository: AlertRepository,
        alert_service: AlertService,
    ) -> None:
        """Initialize alert handler.

        Args:
            alert_repository: Repository for storing alerts.
            alert_service: Service for handling alert operations.

        """
        self.alert_repository = alert_repository
        self.alert_service = alert_service

    async def create_alert(
        self,
        title: str,
        condition: str,
        severity: str = "medium",
        alert_data: dict[str, Any] | None = None,
    ) -> ServiceResult[Alert]:
        """Create a new alert.

        Args:
            title: The alert title.
            condition: The alert condition.
            severity: The severity level (low, medium, high, critical).
            alert_data: Additional alert data including source, source_type, description, threshold (optional).

        Returns:
            Service result containing the created alert.

        """
        try:
            data = alert_data or {}
            alert = Alert(
                title=title,
                source=data.get("source", "manual"),
                source_type=data.get("source_type", "user"),
                condition=condition,
                severity=severity,
                description=data.get("description"),
                threshold=data.get("threshold"),
            )

            # Save to repository
            saved_alert = await self.alert_repository.save(alert)

            # Send to alert service
            await self.alert_service.trigger_alert(saved_alert)  # type: ignore[arg-type]

            return ServiceResult.success(saved_alert)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create alert: {e}")

    async def resolve_alert(self, alert_id: UUID) -> ServiceResult[Alert]:
        """Resolve an existing alert.

        Args:
            alert_id: The ID of the alert to resolve.

        Returns:
            Service result containing the resolved alert.

        """
        try:
            alert = await self.alert_repository.get_by_id(alert_id)
            if not alert:
                return ServiceResult.fail("Alert not found")

            # Resolve alert
            alert.resolve()  # type: ignore[attr-defined]

            # Update repository
            updated_alert = await self.alert_repository.save(alert)  # type: ignore[arg-type]

            # Send to alert service (using alert ID)
            await self.alert_service.resolve_alert(str(alert.id))  # type: ignore[attr-defined]

            return ServiceResult.success(updated_alert)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to resolve alert: {e}")

    async def get_active_alerts(self) -> ServiceResult[list[Alert]]:
        """Get all active alerts.

        Returns:
            Service result containing the list of active alerts.

        """
        try:
            alerts = await self.alert_repository.find_active()
            return ServiceResult.success(alerts)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get active alerts: {e}")


class HealthHandler(BaseCommandHandler):
    """Health check command handler."""

    def __init__(
        self,
        health_repository: HealthRepository,
        health_service: HealthService,
    ) -> None:
        """Initialize health handler.

        Args:
            health_repository: Repository for storing health checks.
            health_service: Service for handling health operations.

        """
        self.health_repository = health_repository
        self.health_service = health_service

    async def create_health_check(
        self,
        name: str,
        check_type: str,
        endpoint: str | None = None,
        timeout_seconds: int = 5,
    ) -> ServiceResult[HealthCheck]:
        """Create a new health check.

        Args:
            name: The name of the health check.
            check_type: The type of health check (http, tcp, custom).
            endpoint: The endpoint to check (optional for non-endpoint checks).
            timeout_seconds: Timeout for the check in seconds.

        Returns:
            Service result containing the created health check.

        """
        try:
            from flext_observability.domain.value_objects import ComponentName

            health_check = HealthCheck(
                name=name,
                check_type=check_type,
                endpoint=endpoint,
                timeout_seconds=timeout_seconds,
                component=ComponentName(name="default"),
            )

            # Save to repository
            saved_check = await self.health_repository.save(health_check)

            return ServiceResult.success(saved_check)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create health check: {e}")

    async def run_health_check(self, check_id: UUID) -> ServiceResult[HealthCheck]:
        """Run a specific health check.

        Args:
            check_id: The ID of the health check to run.

        Returns:
            Service result containing the updated health check with results.

        """
        try:
            health_check = await self.health_repository.get_by_id(check_id)
            if not health_check:
                return ServiceResult.fail("Health check not found")

            # Run check using perform_health_check
            result = await self.health_service.perform_health_check(health_check)  # type: ignore[arg-type]

            # Update check with result
            if result.is_success:
                health_check.record_success(  # type: ignore[attr-defined]
                    30.0,  # Default response time
                    {},  # Default response data
                )
            else:
                health_check.record_failure(result.error or "Health check failed")  # type: ignore[attr-defined]

            # Update repository
            updated_check = await self.health_repository.save(health_check)  # type: ignore[arg-type]

            return ServiceResult.success(updated_check)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to run health check: {e}")

    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health status.

        Returns:
            Service result containing the system health data.

        """
        try:
            health = await self.health_service.get_system_health()
            return ServiceResult.success(health)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")


class DashboardHandler(BaseCommandHandler):
    """Dashboard command handler."""

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        dashboard_service: DashboardService,
    ) -> None:
        """Initialize dashboard handler.

        Args:
            dashboard_repository: Repository for storing dashboards.
            dashboard_service: Service for handling dashboard operations.

        """
        self.dashboard_repository = dashboard_repository
        self.dashboard_service = dashboard_service

    async def create_dashboard(
        self,
        title: str,
        description: str | None = None,
        refresh_interval_seconds: int = 30,
    ) -> ServiceResult[Dashboard]:
        """Create a new dashboard.

        Args:
            title: The dashboard title.
            description: Dashboard description (optional).
            refresh_interval_seconds: Auto-refresh interval in seconds.

        Returns:
            Service result containing the created dashboard.

        """
        try:
            dashboard = Dashboard(
                title=title,
                description=description,
                refresh_interval_seconds=refresh_interval_seconds,
            )

            # Save to repository
            saved_dashboard = await self.dashboard_repository.save(dashboard)

            return ServiceResult.success(saved_dashboard)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create dashboard: {e}")

    async def get_dashboard(self, dashboard_id: UUID) -> ServiceResult[Dashboard]:
        """Get a dashboard by ID.

        Args:
            dashboard_id: The ID of the dashboard to retrieve.

        Returns:
            Service result containing the dashboard.

        """
        try:
            dashboard = await self.dashboard_repository.get_by_id(dashboard_id)
            if not dashboard:
                return ServiceResult.fail("Dashboard not found")
            return ServiceResult.success(dashboard)  # type: ignore[arg-type]
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get dashboard: {e}")

    async def render_dashboard(
        self,
        dashboard_id: UUID,
    ) -> ServiceResult[dict[str, Any]]:
        """Render a dashboard with its data and widgets.

        Args:
            dashboard_id: The ID of the dashboard to render.

        Returns:
            Service result containing the rendered dashboard data.

        """
        try:
            dashboard = await self.dashboard_repository.get_by_id(dashboard_id)
            if not dashboard:
                return ServiceResult.fail("Dashboard not found")

            # Get dashboard data (no render_dashboard method available)
            dashboard_data = {
                "id": str(dashboard.id),  # type: ignore[attr-defined]
                "title": dashboard.title,  # type: ignore[attr-defined]
                "description": dashboard.description,  # type: ignore[attr-defined]
                "refresh_interval_seconds": dashboard.refresh_interval_seconds,  # type: ignore[attr-defined]
                "created_at": dashboard.created_at.isoformat(),  # type: ignore[attr-defined]
                "updated_at": dashboard.updated_at.isoformat(),  # type: ignore[attr-defined]
            }

            return ServiceResult.success(dashboard_data)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to render dashboard: {e}")

    async def get_all_dashboards(self) -> ServiceResult[list[Dashboard]]:
        """Get all dashboards in the system.

        Returns:
            Service result containing the list of all dashboards.

        """
        try:
            dashboards = await self.dashboard_repository.get_all()
            return ServiceResult.success(dashboards)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get dashboards: {e}")
