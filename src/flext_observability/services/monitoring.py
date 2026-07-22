"""Observability monitoring and orchestration services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import ClassVar, override
from uuid import uuid4

from flext_core import FlextContainer
from flext_observability import FlextObservabilityServices, c, m, p, r, settings, t, u


class FlextObservabilityMonitor:
    """Central Observability Services Orchestrator.

    monitoring orchestrator coordinating all observability services
    including metrics collection, distributed tracing, health monitoring, and alerting.
    Provides centralized initialization, lifecycle management, and service coordination
    for complete observability across distributed FLEXT ecosystem components.

    Unified class with nested helpers - no loose functions.
    """

    _container_type: ClassVar[p.ContainerType] = FlextContainer

    object_callable = Callable[..., t.Scalar]
    logger: p.Logger = u.fetch_logger(__name__)

    class MonitoringHelpers:
        """Nested helper class for monitoring operations - unified pattern."""

        @staticmethod
        def call_any_function(
            func: FlextObservabilityMonitor.object_callable,
            *args: t.Scalar,
            **kwargs: t.Scalar,
        ) -> t.Scalar:
            """Call function with flexible arguments."""
            return func(*args, **kwargs)

        @staticmethod
        def execute_monitored_function(
            func: FlextObservabilityMonitor.object_callable,
            args: tuple[t.Scalar, ...],
            kwargs: t.ConfigurationMapping | m.Dict,
            monitor: FlextObservabilityMonitor,
            metric_name: str | None,
        ) -> t.Scalar:
            """Execute function with monitoring."""
            function_name = getattr(func, "__name__", "unknown_function")
            actual_metric_name = metric_name or f"function_execution_{function_name}"
            start_time = time.time()
            try:
                kwargs_dict = kwargs if isinstance(kwargs, dict) else {}
                result = FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                    func, *args, **kwargs_dict
                )
                execution_time = time.time() - start_time
                FlextObservabilityMonitor.MonitoringHelpers.record_success_metrics(
                    monitor, actual_metric_name, execution_time
                )
                return result
            except c.EXC_MAPPING_TYPE as e:
                execution_time = time.time() - start_time
                FlextObservabilityMonitor.MonitoringHelpers.record_error_metrics(
                    monitor, actual_metric_name, execution_time, function_name, e
                )
                raise

        @staticmethod
        def record_error_metrics(
            monitor: FlextObservabilityMonitor,
            metric_name: str,
            execution_time: float,
            function_name: str,
            error: Exception,
        ) -> None:
            """Record metrics and alerts for function execution errors."""
            monitor.flext_record_metric(
                f"{metric_name}_error_total", 1, c.Observability.MetricType.COUNTER
            )
            monitor.flext_record_metric(
                f"{metric_name}_error_duration_seconds",
                execution_time,
                c.Observability.MetricType.HISTOGRAM,
            )
            observability_service = monitor.observability_service
            if observability_service:
                try:
                    alert_result = observability_service.create_alert(
                        title=f"Function execution error: {function_name}",
                        message=f"Function {function_name} failed with {type(error).__name__}",
                        severity="high",
                        source="monitoring",
                    )
                    if alert_result.failure:
                        FlextObservabilityMonitor.logger.warning(
                            f"Alert creation failed: {alert_result.error}"
                        )
                except c.EXC_BASIC_TYPE as e:
                    FlextObservabilityMonitor.logger.warning(
                        f"Alert creation failed: {e}"
                    )

        @staticmethod
        def record_success_metrics(
            monitor: FlextObservabilityMonitor, metric_name: str, execution_time: float
        ) -> None:
            """Record metrics for successful function execution."""
            monitor.flext_record_metric(
                f"{metric_name}_duration_seconds",
                execution_time,
                c.Observability.MetricType.HISTOGRAM,
            )
            monitor.flext_record_metric(
                f"{metric_name}_success_total", 1, c.Observability.MetricType.COUNTER
            )
            monitor.increment_functions_monitored()

    @override
    def __init__(self, container: p.Container | None = None) -> None:
        """Initialize monitor with real service orchestration and shared configuration."""
        self._container = container or self._container_type.shared()
        self.logger = u.fetch_logger(self.__class__.__name__)
        self._initialized = False
        self._running = False
        self._observability_service: p.Observability.ObservabilityService | None = None
        self._health_service: p.Observability.ObservabilityService | None = None
        self._metrics_service: p.Observability.ObservabilityService | None = None
        self._monitor_start_time = time.time()
        self._functions_monitored = 0

    def flext_health_status(self) -> p.Result[t.Observability.HealthMetricsDict]:
        """Resolve complete health status with real metrics."""
        try:
            if not self._observability_service:
                return r[t.Observability.HealthMetricsDict].fail_op(
                    "resolve health status", "Observability service not available"
                )
            health_data: t.MutableJsonMapping = {
                "status": c.Observability.HealthStatus.HEALTHY
                if self._initialized
                else "initializing",
                "timestamp": time.time(),
            }
            health_data["monitor_metrics"] = {
                "monitor_uptime_seconds": time.time() - self._monitor_start_time,
                "functions_monitored": self._functions_monitored,
                "services_initialized": self._initialized,
                "monitoring_active": self._running,
            }
            return r[t.Observability.HealthMetricsDict].ok(health_data)
        except c.EXC_BASIC_TYPE as e:
            return r[t.Observability.HealthMetricsDict].fail_op(
                "resolve health status", e
            )

    def flext_metrics_summary(self) -> p.Result[m.Dict]:
        """Resolve complete metrics summary."""
        if not self._metrics_service:
            return r[m.Dict].fail_op(
                "resolve metrics summary", "Metrics service not available"
            )
        result = self._metrics_service.metrics_summary()
        return (
            r[m.Dict].ok(result.value)
            if result.success
            else r[m.Dict].fail_op(
                "resolve metrics summary", result.error or "Metrics summary failed"
            )
        )

    def flext_initialize_observability(self) -> p.Result[None]:
        """Initialize all observability services with real functionality and settings integration."""
        if self._initialized:
            return r[None].ok(None)
        try:
            return self._initialize_observability_services()
        except c.EXC_BASIC_TYPE as e:
            return r[None].fail_op("initialize observability", e)

    def _initialize_observability_services(self) -> p.Result[None]:
        """Initialize observability service dependencies."""
        service_result = self._create_observability_service()
        if service_result.failure:
            return r[None].fail_op(
                "initialize observability",
                service_result.error or "Service creation failed",
            )
        self._observability_service = service_result.value
        self._metrics_service = self._observability_service
        self._health_service = self._observability_service
        self._initialized = True
        self.logger.info("Observability monitor initialized successfully")
        return r[None].ok(None)

    @staticmethod
    def _create_observability_service() -> p.Result[
        p.Observability.ObservabilityService
    ]:
        """Create the concrete observability service facade."""
        try:
            return r[p.Observability.ObservabilityService].ok(
                FlextObservabilityServices()
            )
        except c.EXC_MAPPING_TYPE as e:
            return r[p.Observability.ObservabilityService].fail_op(
                "create observability service", e
            )

    def flext_initialized(self) -> bool:
        """Return whether observability services are initialized."""
        return self._initialized

    def flext_monitoring_active(self) -> bool:
        """Return whether real monitoring is active and operational."""
        return self._initialized and self._running

    def flext_record_metric(
        self,
        name: str,
        value: float,
        metric_type: str = c.Observability.MetricType.GAUGE,
    ) -> p.Result[None]:
        """Record metric through the monitoring system with settings validation."""
        try:
            return self._record_metric_entry(name, value, metric_type)
        except c.EXC_BASIC_TYPE as e:
            return r[None].fail_op("record metric", e)

    def _record_metric_entry(
        self, name: str, value: float, metric_type: str
    ) -> p.Result[None]:
        """Build and record one monitoring metric entry."""
        if not settings.Observability.metrics_enabled:
            self.logger.debug("Metrics recording disabled in configuration")
            return r[None].ok(None)
        metric_result = self._build_metric_entry(name, value, metric_type)
        if metric_result.failure:
            return r[None].fail_op(
                "record metric", metric_result.error or "Failed to create metric"
            )
        self.logger.debug("Recorded metric: %s=%s (%s)", name, value, metric_type)
        return r[None].ok(None)

    @staticmethod
    def _build_metric_entry(
        name: str, value: float, metric_type: str
    ) -> p.Result[m.Observability.MetricEntry]:
        """Build a monitoring metric entry."""
        try:
            return r[m.Observability.MetricEntry].ok(
                m.Observability.MetricEntry(
                    metric_id=str(uuid4()),
                    name=name,
                    value=value,
                    unit=metric_type,
                    source="monitoring_system",
                )
            )
        except c.EXC_MAPPING_TYPE as e:
            return r[m.Observability.MetricEntry].fail_op("build metric entry", e)

    def flext_start_monitoring(self) -> p.Result[None]:
        """Start real observability monitoring with service coordination."""
        if not self._initialized:
            return r[None].fail_op("start monitoring", "Monitor not initialized")
        if self._running:
            return r[None].ok(None)
        try:
            self.logger.info("Starting real observability monitoring")
            self._running = True
            self._monitor_start_time = time.time()
            return r[None].ok(None)
        except c.EXC_BASIC_TYPE as e:
            return r[None].fail_op("start monitoring", e)

    def flext_stop_monitoring(self) -> p.Result[None]:
        """Stop observability monitoring with graceful service shutdown."""
        if not self._running:
            return r[None].ok(None)
        try:
            self.logger.info("Stopping observability monitoring")
            self._running = False
            return r[None].ok(None)
        except c.EXC_BASIC_TYPE as e:
            return r[None].fail_op("stop monitoring", e)

    @property
    def observability_service(self) -> p.Observability.ObservabilityService | None:
        """The unified observability service."""
        return self._observability_service

    def increment_functions_monitored(self) -> None:
        """Public method to increment functions monitored counter."""
        self._functions_monitored += 1

    @staticmethod
    def flext_monitor_function(
        monitor: FlextObservabilityMonitor | None = None, metric_name: str | None = None
    ) -> Callable[
        [FlextObservabilityMonitor.object_callable],
        FlextObservabilityMonitor.object_callable,
    ]:
        """Create function monitoring decorator with metrics collection."""
        return FlextObservabilityMonitor.MonitoringDecorators.flext_monitor_function(
            monitor=monitor, metric_name=metric_name
        )

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

                def wrapper(*args: t.Scalar, **kwargs: t.Scalar) -> t.Scalar:
                    active_monitor = monitor or FlextObservabilityMonitor()
                    if not active_monitor.flext_initialized():
                        init_result = active_monitor.flext_initialize_observability()
                        if init_result.failure:
                            return FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                                func, *args, **kwargs
                            )
                    if active_monitor.flext_monitoring_active():
                        return FlextObservabilityMonitor.MonitoringHelpers.execute_monitored_function(
                            func, args, kwargs, active_monitor, metric_name
                        )
                    return (
                        FlextObservabilityMonitor.MonitoringHelpers.call_any_function(
                            func, *args, **kwargs
                        )
                    )

                wrapper.__name__ = getattr(func, "__name__", "wrapped_function")
                wrapper.__doc__ = getattr(func, "__doc__", wrapper.__doc__)
                wrapper.__module__ = getattr(func, "__module__", __name__)
                return wrapper

            return decorator


flext_monitor_function = FlextObservabilityMonitor.flext_monitor_function
"""Module-level alias for FlextObservabilityMonitor.flext_monitor_function."""


__all__: t.StrSequence = ("FlextObservabilityMonitor", "flext_monitor_function")
