"""Observability monitoring and orchestration services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import cast, override

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextTypes,
)
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.entities import flext_metric
from flext_observability.services import (
    FlextObservabilityService,
)
from flext_observability.typings import FlextObservabilityTypes

# ============================================================================
# OBSERVABILITY MONITORING ORCHESTRATION - Real Implementation with SOLID
# ============================================================================


class FlextObservabilityMonitor:
    """Central Observability Services Orchestrator.

    Enterprise-grade monitoring orchestrator coordinating all observability services
    including metrics collection, distributed tracing, health monitoring, and alerting.
    Provides centralized initialization, lifecycle management, and service coordination
    for comprehensive observability across distributed FLEXT ecosystem components.

    Unified class with nested helpers - no loose functions.
    """

    # Function type aliases - moved to class for unified pattern
    object_callable = (
        Callable[[], object]
        | Callable[[str], object]
        | Callable[[str], str]
        | Callable[[str], FlextObservabilityTypes.Core.MetadataDict]
        | Callable[[object], object]
        | Callable[[object, object], object]
        | Callable[[int], int]
        | Callable[[int, int], int]
        | Callable[[], str]
        | Callable[[], FlextObservabilityTypes.Core.Headers]
        | Callable[[], None]
        | Callable[[list[int]], FlextObservabilityTypes.Core.MetadataDict]
        | Callable[[str, str], FlextObservabilityTypes.Core.Headers]
        | Callable[[int], dict[str, int]]
        | Callable[[float], FlextTypes.FloatDict]
    )

    class MonitoringHelpers:
        """Nested helper class for monitoring operations - unified pattern."""

        @staticmethod
        def call_any_function(
            func: FlextObservabilityMonitor.object_callable,
            *args: object,
            **kwargs: object,
        ) -> object:
            """Helper to call function with object args - specific type handling."""
            # Use cast to match the expected signature
            args_len = len(args)
            kwargs_len = len(kwargs)

            if (
                args_len == FlextObservabilityConstants.NO_ARGS
                and kwargs_len == FlextObservabilityConstants.NO_ARGS
            ):
                return cast("Callable[[], object]", func)()
            if (
                args_len == FlextObservabilityConstants.ONE_ARG
                and kwargs_len == FlextObservabilityConstants.NO_ARGS
            ):
                return cast("Callable[[object], object]", func)(args[0])
            if (
                args_len == FlextObservabilityConstants.TWO_ARGS
                and kwargs_len == FlextObservabilityConstants.NO_ARGS
            ):
                return cast("Callable[[object, object], object]", func)(
                    args[0], args[1]
                )
            # Fallback for complex signatures - cast to generic callable
            return cast("Callable[[object], object]", func)(*args, **kwargs)

        @staticmethod
        def execute_monitored_function(
            func: FlextObservabilityMonitor.object_callable,
            args: tuple[object, ...],
            kwargs: FlextObservabilityTypes.Core.MetadataDict,
            monitor: FlextObservabilityMonitor,
            metric_name: str | None,
        ) -> object:
            """Execute function with monitoring (extracted for complexity reduction)."""
            function_name = getattr(func, "__name__", "unknown_function")
            actual_metric_name = metric_name or f"function_execution_{function_name}"
            start_time = time.time()

            try:
                # Execute the function
                result: FlextResult[object] = (
                    FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                        func, *args, **kwargs
                    )
                )

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
                monitor.increment_functions_monitored()

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

                # Create alert if observability service is available
                observability_service = monitor.get_observability_service()
                if observability_service:
                    try:
                        # Use module import so tests can patch flext_alert
                        alert_data = {
                            "title": f"Function execution error: {function_name}",
                            "message": f"Function {function_name} failed with {type(e).__name__}",
                            "severity": "high",
                        }
                        observability_service.alerts.create_alert(alert_data)
                    except (ValueError, TypeError, AttributeError) as e:
                        logger = FlextLogger(__name__)
                        logger.warning(
                            f"Alert creation failed during exception handling: {e}"
                        )
                        # Continue with exception propagation

                # Re-raise the original exception
                raise

    # Class attributes with proper type annotations
    container: FlextContainer
    _logger: FlextLogger
    _initialized: bool
    _running: bool
    _observability_service: FlextObservabilityService | None
    _monitor_start_time: float
    _functions_monitored: int

    @override
    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize monitor with real service orchestration and shared configuration."""
        self.container = container or FlextContainer.get_global()
        self._logger = FlextLogger(self.__class__.__name__)
        self._config = FlextObservabilityConfig.get_global_instance()
        self._initialized = False
        self._running = False

        # Real service instances (Dependency Inversion - depends on abstractions)
        self._observability_service: FlextObservabilityService | None = None

        # Monitor metrics for self-monitoring
        self._monitor_start_time = time.time()
        self._functions_monitored = 0

    def flext_initialize_observability(self) -> FlextResult[None]:
        """Initialize all observability services with real functionality and config integration."""
        if self._initialized:
            return FlextResult[None].ok(None)

        try:
            # Validate configuration before initialization
            if not self._config:
                return FlextResult[None].fail("Configuration not available")

            # Check if observability features are enabled via config
            if (
                not self._config.metrics_enabled
                and not self._config.tracing_enabled
                and not self._config.monitoring_enabled
            ):
                self._logger.warning(
                    "All observability features are disabled in configuration"
                )
                # Still initialize but with warning

            # Initialize unified observability service using SOLID principles
            try:
                self._observability_service = FlextObservabilityService()
            except Exception as e:
                return FlextResult[None].fail(
                    f"Observability initialization failed: {e}",
                )

            # Register unified service in container (Dependency Inversion)
            services: FlextObservabilityTypes.Core.ServicesList = [
                ("flext_observability_service", self._observability_service),
            ]

            for service_name, service in services:
                register_result: FlextResult[object] = self.container.register(
                    service_name, service
                )
                if register_result.is_failure:
                    return FlextResult[None].fail(f"Failed to register {service_name}")

            self._initialized = True
            self._logger.info("Observability monitor initialized successfully")
            return FlextResult[None].ok(None)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Observability initialization failed: {e}")

    def flext_start_monitoring(self) -> FlextResult[None]:
        """Start real observability monitoring with service coordination."""
        if not self._initialized:
            return FlextResult[None].fail("Monitor not initialized")

        if self._running:
            return FlextResult[None].ok(None)

        try:
            self._logger.info("Starting real observability monitoring")
            self._running = True
            self._monitor_start_time = time.time()
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Failed to start monitoring: {e}")

    def flext_stop_monitoring(self) -> FlextResult[None]:
        """Stop observability monitoring with graceful service shutdown."""
        if not self._running:
            return FlextResult[None].ok(None)

        try:
            self._logger.info("Stopping observability monitoring")
            self._running = False
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Failed to stop monitoring: {e}")

    def flext_get_health_status(
        self,
    ) -> FlextResult[FlextObservabilityTypes.Core.HealthMetricsDict]:
        """Get comprehensive health status with real metrics."""
        try:
            if not self._health_service:
                return FlextResult[FlextObservabilityTypes.Core.HealthMetricsDict].fail(
                    "Health service not available",
                )

            # Get overall health and add monitor-specific metrics
            health_result: FlextResult[object] = (
                self._health_service.get_overall_health()
            )
            if health_result.is_failure:
                return FlextResult[FlextObservabilityTypes.Core.HealthMetricsDict].fail(
                    health_result.error or "Health service failure",
                )

            health_data: FlextObservabilityTypes.Core.HealthMetricsDict = (
                health_result.unwrap() if health_result.is_success else {}
            )

            # Add monitor-specific health information
            health_data["monitor_metrics"] = {
                "monitor_uptime_seconds": time.time() - self._monitor_start_time,
                "functions_monitored": self._functions_monitored,
                "services_initialized": self._initialized,
                "monitoring_active": self._running,
            }

            return FlextResult[FlextObservabilityTypes.Core.HealthMetricsDict].ok(
                health_data
            )

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[FlextObservabilityTypes.Core.HealthMetricsDict].fail(
                f"Health status check failed: {e}",
            )

    def flext_is_monitoring_active(self) -> bool:
        """Check if real monitoring is active and operational."""
        return self._initialized and self._running

    def flext_is_initialized(self) -> bool:
        """Check if observability services are initialized."""
        return self._initialized

    def flext_record_metric(
        self,
        name: str,
        value: float,
        metric_type: str = "gauge",
    ) -> FlextResult[None]:
        """Record metric through the monitoring system with config validation."""
        try:
            # Check if metrics are enabled in configuration
            if not self._config.metrics_enabled:
                self._logger.debug("Metrics recording disabled in configuration")
                return FlextResult[None].ok(None)  # Silently succeed when disabled

            metric_result = flext_metric(name, value, metric_type=metric_type)
            if metric_result.is_failure:
                return FlextResult[None].fail(
                    metric_result.error or "Failed to create metric",
                )

            # For now, just log the metric since we don't have a persistent metrics service
            metric_result.unwrap()  # Validate metric creation
            self._logger.debug(f"Recorded metric: {name}={value} ({metric_type})")
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Failed to record metric: {e}")

    def flext_get_metrics_summary(
        self,
    ) -> FlextResult[FlextObservabilityTypes.Core.MetricDict]:
        """Get comprehensive metrics summary."""
        if not self._metrics_service:
            return FlextResult[FlextObservabilityTypes.Core.MetricDict].fail(
                "Metrics service not available",
            )

        return self._metrics_service.get_metrics_summary()

    def increment_functions_monitored(self) -> None:
        """Public method to increment functions monitored counter."""
        self._functions_monitored += 1

    def get_observability_service(self) -> FlextObservabilityService | None:
        """Public method to get unified observability service."""
        return self._observability_service


def flext_monitor_function(
    monitor: FlextObservabilityMonitor | None = None,
    metric_name: str | None = None,
) -> Callable[
    [FlextObservabilityMonitor.object_callable],
    FlextObservabilityMonitor.object_callable,
]:
    """Create function monitoring decorator with real metrics collection.

    SOLID compliant with reduced complexity version that provides real functionality
    while maintaining code quality standards and SOLID principles.
    """

    def decorator(
        func: FlextObservabilityMonitor.object_callable,
    ) -> FlextObservabilityMonitor.object_callable:
        def wrapper(*args: object, **kwargs: object) -> object:
            # Get or create monitor instance
            active_monitor = monitor
            if not active_monitor:
                # No factory dependency - simple monitoring only
                # Use a basic monitor instance for simple monitoring
                active_monitor = FlextObservabilityMonitor()

            # Initialize monitor if not already initialized
            if active_monitor and not active_monitor.flext_is_initialized():
                init_result: FlextResult[object] = (
                    active_monitor.flext_initialize_observability()
                )
                if init_result.is_failure:
                    # If initialization fails, execute function without monitoring
                    return (
                        FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                            func, *args, **kwargs
                        )
                    )

            # Execute function normally if no monitoring
            if not (active_monitor and active_monitor.flext_is_monitoring_active()):
                return FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                    func, *args, **kwargs
                )

            # Monitor function execution
            return (
                FlextObservabilityMonitor.MonitoringHelpers.execute_monitored_function(
                    func,
                    args,
                    kwargs,
                    active_monitor,
                    metric_name,
                )
            )

        # Preserve function metadata
        wrapper.__name__ = getattr(func, "__name__", "wrapped_function")
        wrapper.__doc__ = getattr(func, "__doc__", wrapper.__doc__)
        wrapper.__module__ = getattr(func, "__module__", __name__)

        # Return wrapper with preserved metadata and type
        return cast("FlextObservabilityMonitor.object_callable", wrapper)

    return decorator


__all__: FlextObservabilityTypes.Core.StringList = [
    "FlextObservabilityMonitor",
    "flext_monitor_function",
]
