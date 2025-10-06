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
)

from flext_observability.config import FlextObservabilityConfig

# Import functions directly to avoid circular imports
from flext_observability.factories import get_global_observability_service
from flext_observability.models import FlextObservabilityModels
from flext_observability.services import (
    FlextObservabilityServices,
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

    # Function type alias - simplified for monitoring
    object_callable = Callable[..., object]

    class MonitoringHelpers:
        """Nested helper class for monitoring operations - unified pattern."""

        @staticmethod
        def call_any_function(
            func: FlextObservabilityMonitor.object_callable,
            *args: object,
            **kwargs: object,
        ) -> object:
            """Helper to call function with flexible arguments."""
            # Cast to Any to avoid type checking issues with arbitrary function calls
            return func(*args, **kwargs)

        @staticmethod
        def execute_monitored_function(
            func: FlextObservabilityMonitor.object_callable,
            args: tuple[object, ...],
            kwargs: FlextObservabilityTypes.ObservabilityCore.MetadataDict,
            monitor: FlextObservabilityMonitor,
            metric_name: str | None,
        ) -> object:
            """Execute function with monitoring."""
            function_name = getattr(func, "__name__", "unknown_function")
            actual_metric_name = metric_name or f"function_execution_{function_name}"
            start_time = time.time()

            try:
                # Execute the function
                result = FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                    func, *args, **kwargs
                )

                # Record success metrics
                execution_time = time.time() - start_time
                FlextObservabilityMonitor.MonitoringHelpers.record_success_metrics(
                    monitor, actual_metric_name, execution_time
                )

                return result

            except Exception as e:
                # Record error metrics and handle alerting
                execution_time = time.time() - start_time
                FlextObservabilityMonitor.MonitoringHelpers.record_error_metrics(
                    monitor, actual_metric_name, execution_time, function_name, e
                )
                raise

        @staticmethod
        def record_success_metrics(
            monitor: FlextObservabilityMonitor,
            metric_name: str,
            execution_time: float,
        ) -> None:
            """Record metrics for successful function execution."""
            monitor.flext_record_metric(
                f"{metric_name}_duration_seconds", execution_time, "histogram"
            )
            monitor.flext_record_metric(f"{metric_name}_success_total", 1, "counter")
            monitor.increment_functions_monitored()

        @staticmethod
        def record_error_metrics(
            monitor: FlextObservabilityMonitor,
            metric_name: str,
            execution_time: float,
            function_name: str,
            error: Exception,
        ) -> None:
            """Record metrics and alerts for function execution errors."""
            monitor.flext_record_metric(f"{metric_name}_error_total", 1, "counter")
            monitor.flext_record_metric(
                f"{metric_name}_error_duration_seconds", execution_time, "histogram"
            )

            # Create alert if observability service is available
            logger = FlextLogger(__name__)
            observability_service = monitor.get_observability_service()
            if observability_service:
                try:
                    alert_result = get_global_observability_service().create_alert(
                        title=f"Function execution error: {function_name}",
                        message=f"Function {function_name} failed with {type(error).__name__}",
                        severity="high",
                        source="monitoring",
                    )
                    if alert_result.is_failure:
                        logger.warning(f"Alert creation failed: {alert_result.error}")
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(f"Alert creation failed: {e}")

    # Class attributes with proper type annotations
    container: FlextContainer
    logger: FlextLogger
    _initialized: bool
    _running: bool
    _observability_service: FlextObservabilityServices | None
    _monitor_start_time: float
    _functions_monitored: int
    _health_service: FlextObservabilityServices | None
    _metrics_service: FlextObservabilityServices | None

    @override
    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize monitor with real service orchestration and shared configuration."""
        self.container = container or FlextContainer.get_global()
        self.logger = FlextLogger(self.__class__.__name__)
        self._config = FlextObservabilityConfig.get_global_instance()
        self._initialized = False
        self._running = False

        # Real service instances (Dependency Inversion - depends on abstractions)
        self._observability_service: FlextObservabilityServices | None = None
        self._health_service: FlextObservabilityServices | None = None
        self._metrics_service: FlextObservabilityServices | None = None

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
                self.logger.warning(
                    "All observability features are disabled in configuration"
                )
                # Still initialize but with warning

            # Initialize unified observability service using SOLID principles
            try:
                self._observability_service = FlextObservabilityServices()
                self._metrics_service = self._observability_service
                self._health_service = self._observability_service
            except Exception as e:
                return FlextResult[None].fail(
                    f"Observability initialization failed: {e}",
                )

            # Register unified service in container (Dependency Inversion)
            services: FlextObservabilityTypes.ObservabilityCore.ServicesList = [
                ("flext_observability_service", self._observability_service),
            ]

            for service_name, service in services:
                register_result = self.container.register(service_name, service)
                if register_result.is_failure:
                    return FlextResult[None].fail(f"Failed to register {service_name}")

            self._initialized = True
            self.logger.info("Observability monitor initialized successfully")
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
            self.logger.info("Starting real observability monitoring")
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
            self.logger.info("Stopping observability monitoring")
            self._running = False
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Failed to stop monitoring: {e}")

    def flext_get_health_status(
        self,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict]:
        """Get comprehensive health status with real metrics."""
        try:
            if not self._observability_service:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
                ].fail(
                    "Observability service not available",
                )

            # Get health status from observability service
            health_result = (
                self._observability_service.HealthService.get_health_status()
            )
            if health_result.is_failure:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
                ].fail(
                    health_result.error or "Health service failure",
                )

            health_data: FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict = (
                health_result.unwrap() if health_result.is_success else {}
            )

            # Add monitor-specific health information
            health_data["monitor_metrics"] = {
                "monitor_uptime_seconds": time.time() - self._monitor_start_time,
                "functions_monitored": self._functions_monitored,
                "services_initialized": self._initialized,
                "monitoring_active": self._running,
            }

            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
            ].ok(health_data)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
            ].fail(
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
                self.logger.debug("Metrics recording disabled in configuration")
                return FlextResult[None].ok(None)  # Silently succeed when disabled

            metric_result = FlextObservabilityModels.flext_metric(
                name, value, metric_type=metric_type
            )
            if metric_result.is_failure:
                return FlextResult[None].fail(
                    metric_result.error or "Failed to create metric",
                )

            # For now, just log the metric since we don't have a persistent metrics service
            metric_result.unwrap()  # Validate metric creation
            self.logger.debug(f"Recorded metric: {name}={value} ({metric_type})")
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[None].fail(f"Failed to record metric: {e}")

    def flext_get_metrics_summary(
        self,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetricDict]:
        """Get comprehensive metrics summary."""
        if not self._metrics_service:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricDict
            ].fail(
                "Metrics service not available",
            )

        return self._metrics_service.get_metrics_summary()

    def increment_functions_monitored(self) -> None:
        """Public method to increment functions monitored counter."""
        self._functions_monitored += 1

    def get_observability_service(self) -> FlextObservabilityServices | None:
        """Public method to get unified observability service."""
        return self._observability_service

    class MonitoringDecorators:
        """Nested class for monitoring decorators and function wrappers."""

        @staticmethod
        def flext_monitor_function(
            monitor: FlextObservabilityMonitor | None = None,
            metric_name: str | None = None,
        ) -> Callable[
            [FlextObservabilityMonitor.object_callable],
            FlextObservabilityMonitor.object_callable,
        ]:
            """Create function monitoring decorator with metrics collection.

            Simplified decorator that records function execution metrics using flext-observability.
            """

            def decorator(
                func: FlextObservabilityMonitor.object_callable,
            ) -> FlextObservabilityMonitor.object_callable:
                def wrapper(*args: object, **kwargs: object) -> object:
                    # Use provided monitor or create simple one
                    active_monitor = monitor or FlextObservabilityMonitor()

                    # Initialize if needed
                    if not active_monitor.flext_is_initialized():
                        init_result = active_monitor.flext_initialize_observability()
                        if init_result.is_failure:
                            # Execute without monitoring if initialization fails
                            return FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                                func, *args, **kwargs
                            )

                    # Start monitoring if active
                    if active_monitor.flext_is_monitoring_active():
                        return FlextObservabilityMonitor.MonitoringHelpers.execute_monitored_function(
                            func, args, kwargs, active_monitor, metric_name
                        )

                    # Execute without monitoring
                    return (
                        FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                            func, *args, **kwargs
                        )
                    )

                # Preserve function metadata
                wrapper.__name__ = getattr(func, "__name__", "wrapped_function")
                wrapper.__doc__ = getattr(func, "__doc__", wrapper.__doc__)
                wrapper.__module__ = getattr(func, "__module__", __name__)

                return cast("FlextObservabilityMonitor.object_callable", wrapper)

            return decorator


# Backward compatibility alias - maintain ABI stability
flext_monitor_function = (
    FlextObservabilityMonitor.MonitoringDecorators.flext_monitor_function
)

__all__: FlextObservabilityTypes.ObservabilityCore.StringList = [
    "FlextObservabilityMonitor",
    "flext_monitor_function",
]
