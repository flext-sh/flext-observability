"""FlextMonitor - Monitoring orchestration for observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides observability monitoring orchestration extending flext-core.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)

if TYPE_CHECKING:
    from collections.abc import Callable

# ============================================================================
# OBSERVABILITY MONITORING ORCHESTRATION
# ============================================================================


class FlextObservabilityMonitor:
    """Main observability monitor orchestrating all services."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize monitor with flext-core container."""
        self.container = container or FlextContainer()
        self._logger = get_logger(self.__class__.__name__)
        self._initialized = False
        self._running = False

        # Services
        self._metrics_service: FlextMetricsService | None = None
        self._logging_service: FlextLoggingService | None = None
        self._tracing_service: FlextTracingService | None = None
        self._alert_service: FlextAlertService | None = None
        self._health_service: FlextHealthService | None = None

    def flext_initialize_observability(self) -> FlextResult[None]:
        """Initialize all observability services."""
        if self._initialized:
            return FlextResult.ok(None)

        try:
            # Initialize services using flext-core patterns
            self._metrics_service = FlextMetricsService(self.container)
            self._logging_service = FlextLoggingService(self.container)
            self._tracing_service = FlextTracingService(self.container)
            self._alert_service = FlextAlertService(self.container)
            self._health_service = FlextHealthService(self.container)

            # Register services in container
            services = [
                ("flext_metrics_service", self._metrics_service),
                ("flext_logging_service", self._logging_service),
                ("flext_tracing_service", self._tracing_service),
                ("flext_alert_service", self._alert_service),
                ("flext_health_service", self._health_service),
            ]

            for service_name, service in services:
                register_result = self.container.register(service_name, service)
                if register_result.is_failure:
                    return FlextResult.fail(f"Failed to register {service_name}")

            self._initialized = True
            return FlextResult.ok(None)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Observability initialization failed: {e}")

    def flext_start_monitoring(self) -> FlextResult[None]:
        """Start observability monitoring."""
        if not self._initialized:
            return FlextResult.fail("Monitor not initialized")

        if self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Starting observability monitoring")
            self._running = True
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to start monitoring: {e}")

    def flext_stop_monitoring(self) -> FlextResult[None]:
        """Stop observability monitoring."""
        if not self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Stopping observability monitoring")
            self._running = False
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to stop monitoring: {e}")

    def flext_get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive health status."""
        try:
            if not self._health_service:
                return FlextResult.fail("Health service not available")

            return self._health_service.get_overall_health()
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Health status check failed: {e}")

    def flext_is_monitoring_active(self) -> bool:
        """Check if monitoring is active."""
        return self._initialized and self._running


def flext_monitor_function(  # type: ignore[explicit-any]
    monitor: FlextObservabilityMonitor | None = None,
) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Monitor function execution with observability."""
    def decorator(func: Callable[..., object]) -> Callable[..., object]:  # type: ignore[explicit-any]
        def wrapper(*args: object, **kwargs: object) -> object:
            # Simple monitoring passthrough
            if not (monitor and monitor.flext_is_monitoring_active()):
                return func(*args, **kwargs)

            # Execute with monitoring active
            return func(*args, **kwargs)

        return wrapper
    return decorator


__all__ = [
    "FlextObservabilityMonitor",
    "flext_monitor_function",
]
