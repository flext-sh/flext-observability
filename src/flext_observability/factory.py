"""FLEXT Observability Factory - Simplified using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simplified factory eliminating duplicação using flext-core patterns.
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.validation import create_observability_result_error

# ============================================================================
# MASTER FACTORY - Single Point of Access
# ============================================================================


class FlextObservabilityMasterFactory:
    """Master factory providing single point of access - simplified."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize master factory."""
        self.container = container or FlextContainer()
        self._logger = get_logger(self.__class__.__name__)
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup all services automatically."""
        try:
            from flext_observability.services import (
                FlextAlertService,
                FlextHealthService,
                FlextLoggingService,
                FlextMetricsService,
                FlextTracingService,
            )

            services = [
                ("metrics_service", FlextMetricsService),
                ("logging_service", FlextLoggingService),
                ("tracing_service", FlextTracingService),
                ("alert_service", FlextAlertService),
                ("health_service", FlextHealthService),
            ]

            for service_key, service_class in services:
                try:
                    service = service_class(self.container)
                    register_result = self.container.register(service_key, service)
                    if register_result.is_failure:
                        self._logger.warning(f"Failed to register {service_key}: {register_result.error}")
                except Exception as e:
                    self._logger.exception(f"Failed to create {service_key}: {e}")

        except Exception as e:
            self._logger.exception(f"Service setup error: {e}")

    def metric(self, name: str, value: float, **kwargs: Any) -> FlextResult[Any]:
        """Create and record metric."""
        try:
            from flext_observability.entities import FlextMetric
            metric = FlextMetric(name=name, value=value, **kwargs)

            service_result = self.container.get("metrics_service")
            if service_result.is_success and service_result.data:
                return service_result.data.record_metric(metric)
            return FlextResult.ok(metric)

        except Exception as e:
            return create_observability_result_error(
                "metrics",
                f"Failed to create metric: {e}",
                metric_name=name,
                metric_value=value,
            )

    def log(self, message: str, level: str = "info", **kwargs: Any) -> FlextResult[Any]:
        """Create and log entry."""
        try:
            from flext_observability.entities import FlextLogEntry
            log_entry = FlextLogEntry(message=message, level=level, **kwargs)

            service_result = self.container.get("logging_service")
            if service_result.is_success and service_result.data:
                return service_result.data.log_entry(log_entry)
            return FlextResult.ok(log_entry)

        except Exception as e:
            return create_observability_result_error(
                "logging",
                f"Failed to create log: {e}",
                log_level=level,
                log_message=message[:100],
            )

    def alert(self, title: str, message: str, severity: str = "low", **kwargs: Any) -> FlextResult[Any]:
        """Create alert."""
        try:
            from flext_observability.entities import FlextAlert
            alert = FlextAlert(title=title, message=message, severity=severity, **kwargs)

            service_result = self.container.get("alert_service")
            if service_result.is_success and service_result.data:
                return service_result.data.create_alert(alert)
            return FlextResult.ok(alert)

        except Exception as e:
            return create_observability_result_error(
                "alert",
                f"Failed to create alert: {e}",
                alert_title=title,
                alert_severity=severity,
            )

    def trace(self, trace_id: str, operation: str, **kwargs: Any) -> FlextResult[Any]:
        """Start trace."""
        try:
            from flext_observability.entities import FlextTrace
            trace = FlextTrace(trace_id=trace_id, operation=operation, **kwargs)

            service_result = self.container.get("tracing_service")
            if service_result.is_success and service_result.data:
                return service_result.data.start_trace(trace)
            return FlextResult.ok(trace)

        except Exception as e:
            return create_observability_result_error(
                "tracing",
                f"Failed to create trace: {e}",
                trace_id=trace_id,
                operation=operation,
            )

    def health_check(self, component: str, status: str = "unknown", **kwargs: Any) -> FlextResult[Any]:
        """Create health check."""
        try:
            from flext_observability.entities import FlextHealthCheck
            health = FlextHealthCheck(component=component, status=status, **kwargs)

            service_result = self.container.get("health_service")
            if service_result.is_success and service_result.data:
                return service_result.data.check_health(health)
            return FlextResult.ok(health)

        except Exception as e:
            return create_observability_result_error(
                "health_check",
                f"Failed to create health check: {e}",
                component_name=component,
                health_status=status,
            )

    def health_status(self) -> FlextResult[dict[str, Any]]:
        """Get overall health status."""
        try:
            service_result = self.container.get("health_service")
            if service_result.is_success and service_result.data:
                return service_result.data.get_overall_health()

            return FlextResult.ok({"status": "healthy", "mode": "fallback"})

        except Exception as e:
            return create_observability_result_error(
                "health_check",
                f"Health status check failed: {e}",
            )


# ============================================================================
# GLOBAL FACTORY INSTANCE - Single Point of Truth
# ============================================================================

_global_factory: FlextObservabilityMasterFactory | None = None


def get_global_factory(container: FlextContainer | None = None) -> FlextObservabilityMasterFactory:
    """Get global factory instance."""
    global _global_factory
    if _global_factory is None:
        _global_factory = FlextObservabilityMasterFactory(container)
    return _global_factory


def reset_global_factory() -> None:
    """Reset global factory for testing."""
    global _global_factory
    _global_factory = None


# Convenience functions using global factory
def metric(name: str, value: float, **kwargs: Any) -> FlextResult[Any]:
    """Global metric function."""
    return get_global_factory().metric(name, value, **kwargs)


def log(message: str, level: str = "info", **kwargs: Any) -> FlextResult[Any]:
    """Global log function."""
    return get_global_factory().log(message, level, **kwargs)


def alert(title: str, message: str, severity: str = "low", **kwargs: Any) -> FlextResult[Any]:
    """Global alert function."""
    return get_global_factory().alert(title, message, severity, **kwargs)


def trace(trace_id: str, operation: str, **kwargs: Any) -> FlextResult[Any]:
    """Global trace function."""
    return get_global_factory().trace(trace_id, operation, **kwargs)


def health_check(component: str, status: str = "unknown", **kwargs: Any) -> FlextResult[Any]:
    """Global health check function."""
    return get_global_factory().health_check(component, status, **kwargs)
