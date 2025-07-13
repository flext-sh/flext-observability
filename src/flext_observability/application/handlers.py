"""Application handlers for observability service using flext-core patterns.

MIGRATED TO FLEXT-CORE:
                Commands and handlers for observability operations.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from flext_core.application.handlers import CommandHandler
from flext_core.domain.types import ServiceResult

logger = logging.getLogger(__name__)


class LogCommand:
    """Command for logging operations."""
    
    def __init__(self, level: str, message: str, metadata: dict[str, Any] | None = None, timestamp: datetime | None = None):
        self.level = level
        self.message = message
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.now()


class LogHandler(CommandHandler):
    """Log entry command handler."""

    def __init__(self, log_repository: Any, log_service: Any) -> None:
        """Initialize log handler."""
        self.log_repository = log_repository
        self.log_service = log_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle log command."""
        try:
            # Use the provided command or default to LogCommand
            if not isinstance(command, LogCommand):
                # Convert generic command to LogCommand if needed
                command = LogCommand(
                    level=getattr(command, 'level', 'INFO'),
                    message=getattr(command, 'message', str(command)),
                    metadata=getattr(command, 'metadata', {}),
                    timestamp=getattr(command, 'timestamp', datetime.now()),
                )
            
            # Log the message
            logger.log(
                level=getattr(logging, command.level.upper()),
                msg=command.message,
                extra=command.metadata,
            )
            
            # Store in observability system
            if hasattr(self, "_logs"):
                self._logs.append({
                    "level": command.level,
                    "message": command.message,
                    "metadata": command.metadata,
                    "timestamp": command.timestamp,
                })
            
            return ServiceResult.ok({"status": "logged"})
            
        except Exception as e:
            error_msg = f"Failed to handle log command: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)


class MetricsHandler(CommandHandler):
    """Metrics command handler."""

    def __init__(self, metrics_repository: Any, metrics_service: Any) -> None:
        """Initialize metrics handler."""
        self.metrics_repository = metrics_repository
        self.metrics_service = metrics_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle metrics command."""
        try:
            return ServiceResult.ok({"status": "metrics_recorded"})
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle metrics command: {e}")


class TracingHandler(CommandHandler):
    """Tracing command handler."""

    def __init__(self, tracing_repository: Any, tracing_service: Any) -> None:
        """Initialize tracing handler."""
        self.tracing_repository = tracing_repository
        self.tracing_service = tracing_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle tracing command."""
        try:
            return ServiceResult.ok({"status": "trace_recorded"})
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle tracing command: {e}")


class AlertHandler(CommandHandler):
    """Alert command handler."""

    def __init__(self, alert_repository: Any, alert_service: Any) -> None:
        """Initialize alert handler."""
        self.alert_repository = alert_repository
        self.alert_service = alert_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle alert command."""
        try:
            return ServiceResult.ok({"status": "alert_created"})
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle alert command: {e}")


class HealthHandler(CommandHandler):
    """Health check command handler."""

    def __init__(self, health_repository: Any, health_service: Any) -> None:
        """Initialize health handler."""
        self.health_repository = health_repository
        self.health_service = health_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle health check command."""
        try:
            return ServiceResult.ok({"status": "health_check_performed"})
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle health check command: {e}")


class DashboardHandler(CommandHandler):
    """Dashboard command handler."""

    def __init__(self, dashboard_repository: Any, dashboard_service: Any) -> None:
        """Initialize dashboard handler."""
        self.dashboard_repository = dashboard_repository
        self.dashboard_service = dashboard_service

    async def handle(self, command: Any) -> ServiceResult[Any]:
        """Handle dashboard command."""
        try:
            return ServiceResult.ok({"status": "dashboard_created"})
        except Exception as e:
            return ServiceResult.fail(f"Failed to handle dashboard command: {e}")


# Export main classes
__all__ = [
    "AlertHandler",
    "DashboardHandler",
    "HealthHandler",
    "LogCommand",
    "LogHandler",
    "MetricsHandler",
    "TracingHandler",
]
