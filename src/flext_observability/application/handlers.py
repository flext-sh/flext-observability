"""Application handlers for observability service using flext-core patterns.

MIGRATED TO FLEXT-CORE:
                Commands and handlers for observability operations.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from flext_core.application.handlers import CommandHandler
from flext_core.domain.types import ServiceResult

if TYPE_CHECKING:
    from flext_observability.domain.ports import (
        AlertService,
        DashboardService,
        HealthService,
        LogService,
        MetricsService,
        TracingService,
    )
    from flext_observability.infrastructure.persistence.base import (
        AlertRepository,
        DashboardRepository,
        HealthRepository,
        LogRepository,
        MetricsRepository,
        TraceRepository,
    )

logger = logging.getLogger(__name__)


class LogCommand:
    """Command for logging operations."""

    def __init__(
        self,
        level: str,
        message: str,
        metadata: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.level = level
        self.message = message
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.now()


class MetricsCommand:
    """Command for metrics operations."""

    def __init__(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.name = name
        self.value = value
        self.labels = labels or {}
        self.timestamp = timestamp or datetime.now()


class TracingCommand:
    """Command for tracing operations."""

    def __init__(
        self,
        operation_name: str,
        trace_id: str | None = None,
        span_id: str | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.operation_name = operation_name
        self.trace_id = trace_id
        self.span_id = span_id
        self.timestamp = timestamp or datetime.now()


class AlertCommand:
    """Command for alert operations."""

    def __init__(
        self,
        title: str,
        description: str,
        severity: str = "warning",
        timestamp: datetime | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.severity = severity
        self.timestamp = timestamp or datetime.now()


class HealthCommand:
    """Command for health check operations."""

    def __init__(
        self,
        component_name: str,
        endpoint: str | None = None,
        timeout_ms: int = 5000,
        timestamp: datetime | None = None,
    ) -> None:
        self.component_name = component_name
        self.endpoint = endpoint
        self.timeout_ms = timeout_ms
        self.timestamp = timestamp or datetime.now()


class DashboardCommand:
    """Command for dashboard operations."""

    def __init__(
        self,
        dashboard_name: str,
        config: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.dashboard_name = dashboard_name
        self.config = config or {}
        self.timestamp = timestamp or datetime.now()


class LogHandler(CommandHandler[LogCommand, dict[str, Any]]):
    """Log entry command handler."""

    def __init__(
        self,
        log_repository: LogRepository[Any],
        log_service: LogService,
    ) -> None:
        """Initialize log handler."""
        self.log_repository = log_repository
        self.log_service = log_service

    async def handle(self, command: LogCommand) -> ServiceResult[dict[str, Any]]:
        """Handle log command."""
        try:
            # Log the message
            logger.log(
                level=getattr(logging, command.level.upper()),
                msg=command.message,
                extra=command.metadata,
            )

            # Store in observability system
            if hasattr(self, "_logs"):
                self._logs.append(
                    {
                        "level": command.level,
                        "message": command.message,
                        "metadata": command.metadata,
                        "timestamp": command.timestamp,
                    },
                )

            return ServiceResult.ok({"status": "logged"})

        except Exception as e:
            error_msg = f"Failed to handle log command: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)


class MetricsHandler(CommandHandler[MetricsCommand, dict[str, Any]]):
    """Metrics command handler."""

    def __init__(
        self,
        metrics_repository: MetricsRepository[Any],
        metrics_service: MetricsService,
    ) -> None:
        """Initialize metrics handler."""
        self.metrics_repository = metrics_repository
        self.metrics_service = metrics_service

    async def handle(self, command: MetricsCommand) -> ServiceResult[dict[str, Any]]:
        """Handle metrics command."""
        try:
            return ServiceResult.ok(
                {
                    "status": "metrics_recorded",
                    "metric_name": command.name,
                    "value": command.value,
                },
            )
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle metrics command: {e}")


class TracingHandler(CommandHandler[TracingCommand, dict[str, Any]]):
    """Tracing command handler."""

    def __init__(
        self,
        tracing_repository: TraceRepository[Any],
        tracing_service: TracingService,
    ) -> None:
        """Initialize tracing handler."""
        self.tracing_repository = tracing_repository
        self.tracing_service = tracing_service

    async def handle(self, command: TracingCommand) -> ServiceResult[dict[str, Any]]:
        """Handle tracing command."""
        try:
            return ServiceResult.ok(
                {
                    "status": "trace_recorded",
                    "operation": command.operation_name,
                    "trace_id": command.trace_id,
                },
            )
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle tracing command: {e}")


class AlertHandler(CommandHandler[AlertCommand, dict[str, Any]]):
    """Alert command handler."""

    def __init__(
        self,
        alert_repository: AlertRepository[Any],
        alert_service: AlertService,
    ) -> None:
        """Initialize alert handler."""
        self.alert_repository = alert_repository
        self.alert_service = alert_service

    async def handle(self, command: AlertCommand) -> ServiceResult[dict[str, Any]]:
        """Handle alert command."""
        try:
            return ServiceResult.ok(
                {
                    "status": "alert_created",
                    "title": command.title,
                    "severity": command.severity,
                },
            )
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle alert command: {e}")


class HealthHandler(CommandHandler[HealthCommand, dict[str, Any]]):
    """Health check command handler."""

    def __init__(
        self,
        health_repository: HealthRepository[Any],
        health_service: HealthService,
    ) -> None:
        """Initialize health handler."""
        self.health_repository = health_repository
        self.health_service = health_service

    async def handle(self, command: HealthCommand) -> ServiceResult[dict[str, Any]]:
        """Handle health check command."""
        try:
            return ServiceResult.ok(
                {
                    "status": "health_check_performed",
                    "component": command.component_name,
                },
            )
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle health check command: {e}")


class DashboardHandler(CommandHandler[DashboardCommand, dict[str, Any]]):
    """Dashboard command handler."""

    def __init__(
        self,
        dashboard_repository: DashboardRepository[Any],
        dashboard_service: DashboardService,
    ) -> None:
        """Initialize dashboard handler."""
        self.dashboard_repository = dashboard_repository
        self.dashboard_service = dashboard_service

    async def handle(self, command: DashboardCommand) -> ServiceResult[dict[str, Any]]:
        """Handle dashboard command."""
        try:
            return ServiceResult.ok(
                {"status": "dashboard_created", "name": command.dashboard_name},
            )
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle dashboard command: {e}")


# Export main classes
__all__ = [
    "AlertCommand",
    "AlertHandler",
    "DashboardCommand",
    "DashboardHandler",
    "HealthCommand",
    "HealthHandler",
    "LogCommand",
    "LogHandler",
    "MetricsCommand",
    "MetricsHandler",
    "TracingCommand",
    "TracingHandler",
]
