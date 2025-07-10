"""Dependency injection container for FLEXT-OBSERVABILITY.

Using Lato DI framework - NO duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from lato import Container
from lato import DependencyProvider
from lato import Scope

from flext_observability.application.handlers import AlertHandler
from flext_observability.application.handlers import DashboardHandler
from flext_observability.application.handlers import HealthHandler
from flext_observability.application.handlers import LogHandler
from flext_observability.application.handlers import MetricsHandler
from flext_observability.application.handlers import TracingHandler
from flext_observability.infrastructure.config import ObservabilitySettings
from flext_observability.infrastructure.persistence.repositories import AlertRepository
from flext_observability.infrastructure.persistence.repositories import (
    DashboardRepository,
)
from flext_observability.infrastructure.persistence.repositories import HealthRepository
from flext_observability.infrastructure.persistence.repositories import LogRepository
from flext_observability.infrastructure.persistence.repositories import (
    MetricsRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    TracingRepository,
)
from flext_observability.infrastructure.ports import FileLogPort
from flext_observability.infrastructure.ports import JaegerTracingPort
from flext_observability.infrastructure.ports import MemoryDashboardPort
from flext_observability.infrastructure.ports import PrometheusMetricsPort
from flext_observability.infrastructure.ports import SimpleHealthPort
from flext_observability.infrastructure.ports import SlackAlertPort

if TYPE_CHECKING:
    from flext_observability.domain.ports import AlertService
    from flext_observability.domain.ports import DashboardService
    from flext_observability.domain.ports import HealthService
    from flext_observability.domain.ports import LogService
    from flext_observability.domain.ports import MetricsService
    from flext_observability.domain.ports import TracingService


class ObservabilityContainer(Container):
    """Dependency injection container for FLEXT-OBSERVABILITY."""

    # Configuration
    config: ObservabilitySettings = DependencyProvider(
        ObservabilitySettings,
        scope=Scope.SINGLETON,
    )

    # Repository Layer
    log_repository: LogRepository = DependencyProvider(
        LogRepository,
        scope=Scope.SINGLETON,
    )

    metrics_repository: MetricsRepository = DependencyProvider(
        MetricsRepository,
        scope=Scope.SINGLETON,
    )

    tracing_repository: TracingRepository = DependencyProvider(
        TracingRepository,
        scope=Scope.SINGLETON,
    )

    alert_repository: AlertRepository = DependencyProvider(
        AlertRepository,
        scope=Scope.SINGLETON,
    )

    health_repository: HealthRepository = DependencyProvider(
        HealthRepository,
        scope=Scope.SINGLETON,
    )

    dashboard_repository: DashboardRepository = DependencyProvider(
        DashboardRepository,
        scope=Scope.SINGLETON,
    )

    # Infrastructure Services
    log_service: LogService = DependencyProvider(
        FileLogPort,
        scope=Scope.SINGLETON,
    )

    metrics_service: MetricsService = DependencyProvider(
        PrometheusMetricsPort,
        scope=Scope.SINGLETON,
    )

    tracing_service: TracingService = DependencyProvider(
        JaegerTracingPort,
        scope=Scope.SINGLETON,
    )

    alert_service: AlertService = DependencyProvider(
        SlackAlertPort,
        scope=Scope.SINGLETON,
    )

    health_service: HealthService = DependencyProvider(
        SimpleHealthPort,
        scope=Scope.SINGLETON,
    )

    dashboard_service: DashboardService = DependencyProvider(
        MemoryDashboardPort,
        scope=Scope.SINGLETON,
    )

    # Application Handlers
    log_handler: LogHandler = DependencyProvider(
        LogHandler,
        scope=Scope.SINGLETON,
    )

    metrics_handler: MetricsHandler = DependencyProvider(
        MetricsHandler,
        scope=Scope.SINGLETON,
    )

    tracing_handler: TracingHandler = DependencyProvider(
        TracingHandler,
        scope=Scope.SINGLETON,
    )

    alert_handler: AlertHandler = DependencyProvider(
        AlertHandler,
        scope=Scope.SINGLETON,
    )

    health_handler: HealthHandler = DependencyProvider(
        HealthHandler,
        scope=Scope.SINGLETON,
    )

    dashboard_handler: DashboardHandler = DependencyProvider(
        DashboardHandler,
        scope=Scope.SINGLETON,
    )

    def configure(self) -> None:
        """Configure container dependencies."""
        # Configure log service
        self.log_service.config = self.config.logging

        # Configure metrics service
        self.metrics_service.config = self.config.metrics

        # Configure tracing service
        self.tracing_service.config = self.config.tracing

        # Configure alert service
        self.alert_service.config = self.config.alerting

        # Configure health service
        self.health_service.config = self.config.health

        # Configure dashboard service
        self.dashboard_service.config = self.config.alerting

    def get_log_handler(self) -> LogHandler:
        """Get log handler instance."""
        return self.log_handler

    def get_metrics_handler(self) -> MetricsHandler:
        """Get metrics handler instance."""
        return self.metrics_handler

    def get_tracing_handler(self) -> TracingHandler:
        """Get tracing handler instance."""
        return self.tracing_handler

    def get_alert_handler(self) -> AlertHandler:
        """Get alert handler instance."""
        return self.alert_handler

    def get_health_handler(self) -> HealthHandler:
        """Get health handler instance."""
        return self.health_handler

    def get_dashboard_handler(self) -> DashboardHandler:
        """Get dashboard handler instance."""
        return self.dashboard_handler

    def get_all_handlers(self) -> dict[str, Any]:
        """Get all application handlers."""
        return {
            "log": self.get_log_handler(),
            "metrics": self.get_metrics_handler(),
            "tracing": self.get_tracing_handler(),
            "alert": self.get_alert_handler(),
            "health": self.get_health_handler(),
            "dashboard": self.get_dashboard_handler(),
        }

    def validate_configuration(self) -> list[str]:
        """Validate container configuration."""
        errors = []

        # Validate config
        config_errors = self.config.validate_config()
        if config_errors:
            errors.extend(config_errors)

        # Validate dependencies
        try:
            self.configure()
        except Exception as e:
            errors.append(f"Container configuration error: {e}")

        return errors

    def get_container_info(self) -> dict[str, Any]:
        """Get container information."""
        return {
            "name": "ObservabilityContainer",
            "version": "0.7.0",
            "framework": "Lato",
            "dependencies": {
                "handlers": 6,
                "services": 6,
                "repositories": 6,
            },
            "config": {
                "service_name": self.config.service_name,
                "service_version": self.config.service_version,
                "environment": self.config.environment,
                "features": {
                    "metrics": self.config.metrics_enabled,
                    "tracing": self.config.tracing_enabled,
                    "logging": self.config.logging_enabled,
                    "health": self.config.health_enabled,
                    "alerting": self.config.alerting_enabled,
                },
            },
        }


# Global container instance
_container: ObservabilityContainer | None = None


def get_container() -> ObservabilityContainer:
    """Get the global observability container instance."""
    global _container
    if _container is None:
        _container = ObservabilityContainer()
        _container.configure()
    return _container


def reset_container() -> None:
    """Reset the global container instance."""
    global _container
    _container = None
