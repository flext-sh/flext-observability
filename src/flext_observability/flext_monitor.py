"""FlextMonitor - Monitoring orchestration for observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides observability monitoring orchestration extending flext-core.
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any

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
                    return FlextResult.error(f"Failed to register {service_name}")

            self._initialized = True
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.error(f"Observability initialization failed: {e}")

    def flext_start_monitoring(self) -> FlextResult[None]:
        """Start observability monitoring."""
        if not self._initialized:
            return FlextResult.error("Monitor not initialized")

        if self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Starting observability monitoring")
            self._running = True
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.error(f"Failed to start monitoring: {e}")

    def flext_stop_monitoring(self) -> FlextResult[None]:
        """Stop observability monitoring."""
        if not self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Stopping observability monitoring")
            self._running = False
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.error(f"Failed to stop monitoring: {e}")

    def flext_get_health_status(self) -> FlextResult[dict[str, Any]]:
        """Get comprehensive health status."""
        try:
            if not self._health_service:
                return FlextResult.error("Health service not available")

            return self._health_service.get_overall_health()
        except Exception as e:
            return FlextResult.error(f"Health status check failed: {e}")

    def flext_is_monitoring_active(self) -> bool:
        """Check if monitoring is active."""
        return self._initialized and self._running


def flext_monitor_function(
    monitor: FlextObservabilityMonitor | None = None,
    metric_name: str = "function_execution",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to monitor function execution with observability."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if monitor and monitor.flext_is_monitoring_active():
                # Record function execution start
                if monitor._metrics_service:
                    start_metric_result = monitor._metrics_service.record_metric(
                        type("FlextMetric", (), {
                            "name": f"{metric_name}_started",
                            "value": 1.0,
                        })(),
                    )
                    if start_metric_result.is_failure:
                        monitor._logger.warning(f"Failed to record start metric: {start_metric_result.error}")

                # Execute function
                try:
                    result = func(*args, **kwargs)

                    # Record successful execution
                    if monitor._metrics_service:
                        success_metric_result = monitor._metrics_service.record_metric(
                            type("FlextMetric", (), {
                                "name": f"{metric_name}_success",
                                "value": 1.0,
                            })(),
                        )
                        if success_metric_result.is_failure:
                            monitor._logger.warning(f"Failed to record success metric: {success_metric_result.error}")

                    return result

                except Exception:
                    # Record failed execution
                    if monitor._metrics_service:
                        error_metric_result = monitor._metrics_service.record_metric(
                            type("FlextMetric", (), {
                                "name": f"{metric_name}_error",
                                "value": 1.0,
                            })(),
                        )
                        if error_metric_result.is_failure:
                            monitor._logger.warning(f"Failed to record error metric: {error_metric_result.error}")

                    raise
            else:
                # Execute without monitoring
                return func(*args, **kwargs)

        return wrapper
    return decorator


__all__ = [
    "FlextObservabilityMonitor",
    "flext_monitor_function",
]
