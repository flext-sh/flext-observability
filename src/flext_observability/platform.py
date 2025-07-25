"""FLEXT Observability Platform - Unified platform for observability services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform factory for creating observability services with unified configuration.
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextProcessingError, FlextResult

from flext_observability.application.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


class FlextObservabilityPlatform:
    """FLEXT Observability Platform."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize observability platform.

        Args:
            container: Optional FLEXT container instance.

        """
        self.container = container or FlextContainer()
        self._setup_services()

    def _setup_services(self) -> None:
        """Register observability services in the container."""
        self.container.register("metrics_service", FlextMetricsService(self.container))
        self.container.register("logging_service", FlextLoggingService(self.container))
        self.container.register("tracing_service", FlextTracingService(self.container))
        self.container.register("alert_service", FlextAlertService(self.container))
        self.container.register("health_service", FlextHealthService(self.container))

    @property
    def metrics_service(self) -> FlextMetricsService:
        """Get metrics service from the platform.

        Returns:
            FlextMetricsService instance

        """
        result = self.container.get("metrics_service")
        if result.is_success:
            return result.data
        msg = f"Failed to get metrics service: {result.error}"
        raise FlextProcessingError(msg)

    def get_metrics_service(self) -> FlextMetricsService:
        """Get metrics service from the platform.

        Returns:
            FlextMetricsService instance

        """
        return self.metrics_service

    @property
    def logging_service(self) -> FlextLoggingService:
        """Get logging service from the platform.

        Returns:
            FlextLoggingService instance

        """
        result = self.container.get("logging_service")
        if result.is_success:
            return result.data
        msg = f"Failed to get logging service: {result.error}"
        raise FlextProcessingError(msg)

    def get_logging_service(self) -> FlextLoggingService:
        """Get logging service from the platform.

        Returns:
            FlextLoggingService instance

        """
        return self.logging_service

    @property
    def tracing_service(self) -> FlextTracingService:
        """Get tracing service from the platform.

        Returns:
            FlextTracingService instance

        """
        result = self.container.get("tracing_service")
        if result.is_success:
            return result.data
        msg = f"Failed to get tracing service: {result.error}"
        raise FlextProcessingError(msg)

    def get_tracing_service(self) -> FlextTracingService:
        """Get tracing service from the platform.

        Returns:
            FlextTracingService instance

        """
        return self.tracing_service

    @property
    def alert_service(self) -> FlextAlertService:
        """Get alert service from the platform.

        Returns:
            FlextAlertService instance

        """
        result = self.container.get("alert_service")
        if result.is_success:
            return result.data
        msg = f"Failed to get alert service: {result.error}"
        raise FlextProcessingError(msg)

    def get_alert_service(self) -> FlextAlertService:
        """Get alert service from the platform.

        Returns:
            FlextAlertService instance

        """
        return self.alert_service

    @property
    def health_service(self) -> FlextHealthService:
        """Get health service from the platform.

        Returns:
            FlextHealthService instance

        """
        result = self.container.get("health_service")
        if result.is_success:
            return result.data
        msg = f"Failed to get health service: {result.error}"
        raise FlextProcessingError(msg)

    def get_health_service(self) -> FlextHealthService:
        """Get health service from the platform.

        Returns:
            FlextHealthService instance

        """
        return self.health_service

    def configure(self, new_config: dict[str, object]) -> FlextResult[bool]:
        """Configure the platform with new settings.

        Args:
            new_config: New configuration dictionary

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self.config.update(new_config)
            # Reconfigure services if needed
            self._setup_services()
            return FlextResult.ok(True)
        except Exception as e:  # noqa: BLE001
            return FlextResult.fail(f"Failed to configure platform: {e}")

    def health_check(self) -> FlextResult[dict[str, str]]:
        """Perform platform health check.

        Returns:
            FlextResult with health status

        """
        try:
            health_service = self.get_health_service()
            overall_health = health_service.get_overall_health()

            return FlextResult.ok(
                {
                    "platform": "healthy",
                    "services": "available",
                    "overall": overall_health.data
                    if overall_health.is_success
                    else "unknown",
                },
            )
        except Exception as e:  # noqa: BLE001
            return FlextResult.fail(f"Health check failed: {e}")
