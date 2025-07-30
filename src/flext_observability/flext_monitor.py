"""FlextMonitor - Real monitoring orchestration for observability with SOLID principles.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides real observability monitoring orchestration with metrics collection,
distributed tracing, health monitoring, and alerting capabilities.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.factory import get_global_factory
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)

if TYPE_CHECKING:
    from collections.abc import Callable

# Function type aliases - keeping simple for mypy strict compliance

# ============================================================================
# OBSERVABILITY MONITORING ORCHESTRATION - Real Implementation with SOLID
# ============================================================================


class FlextObservabilityMonitor:
    """Real observability monitor orchestrating all services with SOLID principles.

    Implements Single Responsibility (observability orchestration),
    Open/Closed (extensible service integration),
    Liskov Substitution (monitor interface),
    Interface Segregation (focused monitoring API), and Dependency Inversion
    (service abstractions).
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize monitor with real service orchestration and integration."""
        self.container = container or FlextContainer()
        self._logger = get_logger(self.__class__.__name__)
        self._initialized = False
        self._running = False

        # Real service instances (Dependency Inversion - depends on abstractions)
        self._metrics_service: FlextMetricsService | None = None
        self._logging_service: FlextLoggingService | None = None
        self._tracing_service: FlextTracingService | None = None
        self._alert_service: FlextAlertService | None = None
        self._health_service: FlextHealthService | None = None

        # Monitor metrics for self-monitoring
        self._monitor_start_time = time.time()
        self._functions_monitored = 0

    def flext_initialize_observability(self) -> FlextResult[None]:
        """Initialize all observability services with real functionality."""
        if self._initialized:
            return FlextResult.ok(None)

        try:
            # Initialize real services using SOLID principles (Single Responsibility)
            self._metrics_service = FlextMetricsService(self.container)
            self._logging_service = FlextLoggingService(self.container)
            self._tracing_service = FlextTracingService(self.container)
            self._alert_service = FlextAlertService(self.container)
            self._health_service = FlextHealthService(self.container)

            # Register services in container (Dependency Inversion)
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
            self._logger.info("Observability monitor initialized successfully")
            return FlextResult.ok(None)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Observability initialization failed: {e}")

    def flext_start_monitoring(self) -> FlextResult[None]:
        """Start real observability monitoring with service coordination."""
        if not self._initialized:
            return FlextResult.fail("Monitor not initialized")

        if self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Starting real observability monitoring")
            self._running = True
            self._monitor_start_time = time.time()
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to start monitoring: {e}")

    def flext_stop_monitoring(self) -> FlextResult[None]:
        """Stop observability monitoring with graceful service shutdown."""
        if not self._running:
            return FlextResult.ok(None)

        try:
            self._logger.info("Stopping observability monitoring")
            self._running = False
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to stop monitoring: {e}")

    def flext_get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive health status with real metrics."""
        try:
            if not self._health_service:
                return FlextResult.fail("Health service not available")

            # Get overall health and add monitor-specific metrics
            health_result = self._health_service.get_overall_health()
            if health_result.is_failure:
                return health_result

            health_data = health_result.data or {}

            # Add monitor-specific health information
            monitor_health = {
                "monitor_uptime_seconds": time.time() - self._monitor_start_time,
                "functions_monitored": self._functions_monitored,
                "services_initialized": self._initialized,
                "monitoring_active": self._running,
            }

            if isinstance(health_data, dict):
                health_data["monitor_metrics"] = monitor_health

            return FlextResult.ok(health_data)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Health status check failed: {e}")

    def flext_is_monitoring_active(self) -> bool:
        """Check if real monitoring is active and operational."""
        return self._initialized and self._running

    def flext_record_metric(
        self,
        name: str,
        value: float,
        metric_type: str = "gauge",
    ) -> FlextResult[None]:
        """Record metric through the monitoring system."""
        if not self._metrics_service:
            return FlextResult.fail("Metrics service not available")

        try:
            from flext_observability.entities import flext_metric  # noqa: PLC0415

            metric_result = flext_metric(name, value, metric_type=metric_type)
            if metric_result.is_failure:
                return FlextResult.fail(
                    metric_result.error or "Failed to create metric",
                )

            if metric_result.data is None:
                return FlextResult.fail("Metric creation returned None")
            return self._metrics_service.record_metric(metric_result.data).map(
                lambda _: None,
            )
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to record metric: {e}")

    def flext_get_metrics_summary(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive metrics summary."""
        if not self._metrics_service:
            return FlextResult.fail("Metrics service not available")

        return self._metrics_service.get_metrics_summary()


def flext_monitor_function(  # type: ignore[explicit-any]
    monitor: FlextObservabilityMonitor | None = None,
    metric_name: str | None = None,
) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Simple function monitoring decorator with real metrics collection.

    SOLID compliant with reduced complexity version that provides real functionality
    while maintaining code quality standards and SOLID principles.
    """

    def decorator(func: Callable[..., object]) -> Callable[..., object]:  # type: ignore[explicit-any]
        def wrapper(*args: object, **kwargs: object) -> object:
            # Get or create monitor instance
            active_monitor = monitor
            if not active_monitor:
                factory = get_global_factory()
                active_monitor = getattr(factory, "_monitor", None)

            # Execute function normally if no monitoring
            if not (active_monitor and active_monitor.flext_is_monitoring_active()):
                return func(*args, **kwargs)

            # Monitor function execution
            return _execute_monitored_function(
                func,
                args,
                kwargs,
                active_monitor,
                metric_name,
            )

        # Preserve function metadata
        wrapper.__name__ = getattr(func, "__name__", "wrapped_function")
        wrapper.__doc__ = getattr(func, "__doc__", wrapper.__doc__)
        wrapper.__module__ = getattr(func, "__module__", __name__)

        return wrapper

    return decorator


def _execute_monitored_function(  # type: ignore[explicit-any]
    func: Callable[..., object],
    args: tuple[object, ...],
    kwargs: dict[str, object],
    monitor: FlextObservabilityMonitor,
    metric_name: str | None,
) -> object:
    """Execute function with monitoring (extracted for complexity reduction)."""
    function_name = getattr(func, "__name__", "unknown_function")
    actual_metric_name = metric_name or f"function_execution_{function_name}"
    start_time = time.time()

    try:
        # Execute the function
        result = func(*args, **kwargs)

        # Record success metrics
        execution_time = time.time() - start_time
        monitor.flext_record_metric(
            f"{actual_metric_name}_duration_seconds",
            execution_time,
            "histogram",
        )
        monitor.flext_record_metric(
            f"{actual_metric_name}_success_total",
            1,
            "counter",
        )

        # Update monitor statistics
        monitor._functions_monitored += 1

        return result

    except Exception as e:
        # Record error metrics
        execution_time = time.time() - start_time
        monitor.flext_record_metric(
            f"{actual_metric_name}_error_total",
            1,
            "counter",
        )
        monitor.flext_record_metric(
            f"{actual_metric_name}_error_duration_seconds",
            execution_time,
            "histogram",
        )

        # Create alert if alert service is available
        if monitor._alert_service:
            try:
                from flext_observability.entities import flext_alert  # noqa: PLC0415

                alert = flext_alert(
                    title=f"Function execution error: {function_name}",
                    message=f"Function failed with {type(e).__name__}",
                    severity="error",
                    source="function_monitor",
                )
                monitor._alert_service.create_alert(alert)
            except (ValueError, TypeError, AttributeError):
                pass  # Alert creation failed, continue with exception propagation

        # Re-raise the original exception
        raise


__all__ = [
    "FlextObservabilityMonitor",
    "flext_monitor_function",
]
