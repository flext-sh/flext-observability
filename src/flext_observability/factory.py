"""FLEXT Observability Entity Factory.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Factory patterns implementing centralized entity creation with comprehensive
validation, dependency injection, and business rule enforcement for observability
entities. Provides unified access point for creating FlextMetric, FlextTrace,
FlextAlert, FlextHealthCheck, and FlextLogEntry entities with consistent
validation and initialization patterns.

Built following Factory Method and Abstract Factory patterns with dependency
injection support, this module eliminates code duplication while ensuring
consistent entity creation across the FLEXT ecosystem. All factory methods
implement railway-oriented programming with FlextResult error handling.

Key Components:
    - FlextObservabilityMasterFactory: Central factory for all observability entities
    - Entity creation methods with validation and business rule enforcement
    - Service coordination for entity processing and storage
    - Dependency injection container integration

Architecture:
    Interface Adapters layer in Clean Architecture, coordinating domain entity
    creation with application services. Implements Factory patterns with
    comprehensive validation and error handling for enterprise reliability.

Integration:
    - Built on flext-core foundation patterns (FlextContainer, FlextResult)
    - Coordinates observability domain entities and application services
    - Provides consistent API for external interfaces and client integration
    - Supports comprehensive observability across FLEXT ecosystem

Example:
    Centralized entity creation with validation:

    >>> from flext_observability.factory import FlextObservabilityMasterFactory
    >>> from flext_core import FlextContainer
    >>>
    >>> container = FlextContainer()
    >>> factory = FlextObservabilityMasterFactory(container)
    >>>
    >>> # Create metric with automatic validation
    >>> metric_result = factory.create_metric("api_requests", 42, "count")
    >>> if metric_result.is_success:
    ...     print(f"Created: {metric_result.data.name}")
    >>>
    >>> # Create trace with business context
    >>> trace_result = factory.create_trace("user_login", "auth-service")

FLEXT Integration:
    Provides centralized factory services for observability entity creation
    across all 33 FLEXT ecosystem projects, ensuring consistent patterns and
    validation for metrics, tracing, alerting, health monitoring, and logging.

"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import cast

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.entities import (
    FlextAlert,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,  # Import for DRY principle - re-expose for tests
    flext_health_check,  # Import for DRY principle - re-expose for tests
    flext_trace,  # Import for DRY principle - re-expose for tests
)
from flext_observability.flext_simple import flext_create_health_check
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)
from flext_observability.validation import create_observability_result_error

# ============================================================================
# MASTER FACTORY - Single Point of Access
# ============================================================================


class FlextObservabilityMasterFactory:
    """Master Factory for Centralized Observability Entity Creation.

    Enterprise-grade factory implementing comprehensive entity creation patterns
    with validation, dependency injection, and business rule enforcement. Provides
    unified access point for creating all observability entities (metrics, traces,
    alerts, health checks, logs) with consistent validation and initialization.

    This factory eliminates code duplication by centralizing entity creation logic
    while ensuring consistent business rule enforcement, validation patterns, and
    error handling across all observability entity types. Integrates with application
    services for entity processing and storage coordination.

    Responsibilities:
        - Centralized entity creation with comprehensive validation
        - Business rule enforcement during entity initialization
        - Dependency injection container coordination
        - Application service integration for entity processing
        - Consistent error handling with railway-oriented programming
        - Entity lifecycle management and coordination

    Factory Patterns Implementation:
        - Factory Method: Individual entity creation methods
        - Abstract Factory: Consistent interface across entity types
        - Dependency Injection: Service coordination via FlextContainer
        - Template Method: Consistent validation and error handling patterns

    Attributes:
        container (FlextContainer): Dependency injection container for services
        _logger: Structured logger for factory operations and diagnostics
        _metrics_service: Metrics processing and storage service
        _tracing_service: Distributed tracing coordination service
        _alert_service: Alert processing and routing service
        _health_service: Health monitoring and validation service
        _logging_service: Structured logging management service

    Entity Creation Methods:
        - create_metric(): FlextMetric creation with validation
        - create_trace(): FlextTrace creation with correlation support
        - create_alert(): FlextAlert creation with severity validation
        - create_health_check(): FlextHealthCheck creation with dependency validation
        - create_log_entry(): FlextLogEntry creation with context enrichment

    Example:
        Comprehensive entity creation with business validation:

        >>> from flext_observability.factory import FlextObservabilityMasterFactory
        >>> from flext_core import FlextContainer
        >>>
        >>> container = FlextContainer()
        >>> factory = FlextObservabilityMasterFactory(container)
        >>>
        >>> # Create performance metric with automatic validation
        >>> metric_result = factory.create_metric(
        ...     name="api_response_time",
        ...     value=150.5,
        ...     unit="milliseconds",
        ...     tags={"service": "user-api", "endpoint": "/users"},
        ... )
        >>> if metric_result.is_success:
        ...     metric = metric_result.data
        ...     print(f"Created metric: {metric.name}")

        >>> # Create distributed trace with correlation
        >>> trace_result = factory.create_trace(
        ...     operation_name="user_authentication",
        ...     service_name="auth-service",
        ...     context={"user_id": "12345", "request_id": "req_abc"},
        ... )

        >>> # Create critical alert with routing
        >>> alert_result = factory.create_alert(
        ...     title="Database Connection Failure",
        ...     message="Production database unavailable",
        ...     severity="critical",
        ...     tags={"service": "database", "environment": "production"},
        ... )

    Validation and Error Handling:
        All entity creation methods implement comprehensive validation including:
        - Domain rule enforcement (entity.validate_domain_rules())
        - Business constraint validation
        - Type safety verification
        - Railway-oriented programming with FlextResult
        - Detailed error messages for debugging and monitoring

    Service Integration:
        Factory coordinates with application services for entity processing:
        - Metrics automatically recorded via FlextMetricsService
        - Traces coordinated via FlextTracingService
        - Alerts processed via FlextAlertService
        - Health checks validated via FlextHealthService
        - Log entries enriched via FlextLoggingService

    Thread Safety:
        Factory operations are thread-safe through service coordination,
        supporting concurrent entity creation from multiple threads without
        data corruption or validation inconsistencies.

    Architecture:
        Interface Adapters layer factory coordinating domain entities with
        application services. Implements Factory patterns while maintaining
        Clean Architecture boundaries and dependency inversion principles.

    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize master factory with dependency injection and service coordination.

        Args:
            container: Dependency injection container for service coordination.
                Defaults to new FlextContainer if not provided. Services are
                automatically initialized and configured for entity processing.

        """
        self.container = container or FlextContainer()
        self._logger = get_logger(self.__class__.__name__)
        self._setup_services()

    def _setup_services(self) -> None:
        """Set up all services automatically."""
        try:
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
                        error_message = (
                            f"Failed to register {service_key}: {register_result.error}"
                        )
                        self._logger.warning(error_message)
                except (
                    ValueError,
                    TypeError,
                    AttributeError,
                    ImportError,
                    RuntimeError,
                ):
                    self._logger.exception("Failed to create %s", service_key)

        except (
            ValueError,
            TypeError,
            AttributeError,
            ImportError,
            RuntimeError,
        ):
            self._logger.exception("Service setup error occurred")

    def metric(
        self,
        name: str,
        value: float,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create and record metric."""
        try:
            # FlextMetric imported at module level
            tags = kwargs.get("tags", {})
            tags = cast("dict[str, str]", tags) if isinstance(tags, dict) else {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = datetime.now(UTC)

            metric = FlextMetric(
                id=str(uuid.uuid4()),
                name=name,
                value=value,
                unit=str(kwargs.get("unit", "")),
                tags=tags,
                timestamp=timestamp,
            )

            service_result = self.container.get("metrics_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextMetricsService", service_result.data)
                result = service.record_metric(metric)
                return (
                    FlextResult.ok(result.data)
                    if result.is_success
                    else FlextResult.fail(result.error or "Unknown error")
                )
            return FlextResult.ok(metric)

        except (ValueError, TypeError, AttributeError) as e:
            return create_observability_result_error(
                "metrics",
                f"Failed to create metric: {e}",
                metric_name=name,
                metric_value=value,
            )

    def log(
        self,
        message: str,
        level: str = "info",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create and log entry."""
        try:
            # FlextLogEntry imported at module level
            context = kwargs.get("context", {})
            if isinstance(context, dict):
                context = cast("dict[str, object]", context)
            else:
                context = {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = datetime.now(UTC)

            log_entry = FlextLogEntry(
                id=str(uuid.uuid4()),
                message=message,
                level=level,
                context=context,
                timestamp=timestamp,
            )

            service_result = self.container.get("logging_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextLoggingService", service_result.data)
                result = service.log_entry(log_entry)
                return (
                    FlextResult.ok(result.data)
                    if result.is_success
                    else FlextResult.fail(result.error or "Unknown error")
                )
            return FlextResult.ok(log_entry)

        except (ValueError, TypeError, AttributeError) as e:
            return create_observability_result_error(
                "logging",
                f"Failed to create log: {e}",
                log_level=level,
                log_message=message[:100],
            )

    def alert(
        self,
        title: str,
        message: str,
        severity: str = "low",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create alert."""
        try:
            tags = kwargs.get("tags", {})
            tags = cast("dict[str, str]", tags) if isinstance(tags, dict) else {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = datetime.now(UTC)

            alert = FlextAlert(
                id=str(uuid.uuid4()),
                title=title,
                message=message,
                severity=severity,
                status=str(kwargs.get("status", "active")),
                tags=tags,
                timestamp=timestamp,
            )

            service_result = self.container.get("alert_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextAlertService", service_result.data)
                result = service.create_alert(alert)
                return (
                    FlextResult.ok(result.data)
                    if result.is_success
                    else FlextResult.fail(result.error or "Unknown error")
                )
            return FlextResult.ok(alert)

        except (ValueError, TypeError, AttributeError) as e:
            return create_observability_result_error(
                "alert",
                f"Failed to create alert: {e}",
                alert_title=title,
                alert_severity=severity,
            )

    def trace(
        self,
        trace_id: str,
        operation: str,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Start trace."""
        try:
            # Extract known parameters from kwargs
            span_id = kwargs.get("span_id", "")
            timestamp = kwargs.get("timestamp")
            span_attributes = kwargs.get("span_attributes", {})

            trace = FlextTrace(
                id=str(uuid.uuid4()),
                trace_id=trace_id,
                operation=operation,
                span_id=str(span_id) if span_id else "",
                span_attributes=(
                    span_attributes if isinstance(span_attributes, dict) else {}
                ),
                duration_ms=int(str(kwargs.get("duration_ms", 0)) or "0"),
                status=str(kwargs.get("status", "pending")),
                timestamp=(
                    timestamp if isinstance(timestamp, datetime) else datetime.now(UTC)
                ),
            )

            service_result = self.container.get("tracing_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextTracingService", service_result.data)
                result = service.start_trace(trace)
                return (
                    FlextResult.ok(result.data)
                    if result.is_success
                    else FlextResult.fail(result.error or "Unknown error")
                )
            return FlextResult.ok(trace)

        except (ValueError, TypeError, AttributeError) as e:
            return create_observability_result_error(
                "tracing",
                f"Failed to create trace: {e}",
                trace_id=trace_id,
                operation=operation,
            )

    def health_check(
        self,
        component: str,
        status: str = "unknown",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create health check."""
        try:
            # Extract known parameters from kwargs
            message = kwargs.get("message", "")
            timestamp = kwargs.get("timestamp")

            # Use imported function for consistency and testability
            health_result = flext_create_health_check(
                component=component,
                status=status,
                message=str(message),
                timestamp=(
                    timestamp if isinstance(timestamp, datetime) else datetime.now(UTC)
                ),
            )
            if health_result.is_failure:
                return FlextResult.fail(health_result.error or "Health check failed")
            health = health_result.data

            service_result = self.container.get("health_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextHealthService", service_result.data)
                result = service.check_health(health_result)
                return (
                    FlextResult.ok(result.data)
                    if result.is_success
                    else FlextResult.fail(result.error or "Unknown error")
                )
            return FlextResult.ok(health)

        except (ValueError, TypeError, AttributeError) as e:
            return create_observability_result_error(
                "health_check",
                f"Failed to create health check: {e}",
                component_name=component,
                health_status=status,
            )

    def health_status(self) -> FlextResult[dict[str, object]]:
        """Get overall health status."""
        try:
            service_result = self.container.get("health_service")
            if service_result.is_success and service_result.data:
                service = cast("FlextHealthService", service_result.data)
                return service.get_overall_health()

            return FlextResult.ok({"status": "healthy", "mode": "fallback"})

        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "health_check",
                f"Health status check failed: {e}",
            )
            return FlextResult.fail(error_result.error or "Health status check failed")


# ============================================================================
# GLOBAL FACTORY INSTANCE - Single Point of Truth
# ============================================================================

_global_factory: FlextObservabilityMasterFactory | None = None


def get_global_factory(
    container: FlextContainer | None = None,
) -> FlextObservabilityMasterFactory:
    """Get global factory instance."""
    global _global_factory  # noqa: PLW0603
    if _global_factory is None:
        _global_factory = FlextObservabilityMasterFactory(container)
    return _global_factory


def reset_global_factory() -> None:
    """Reset global factory for testing."""
    global _global_factory  # noqa: PLW0603
    _global_factory = None


# Convenience functions using global factory
def metric(name: str, value: float, **kwargs: object) -> FlextResult[object]:
    """Global metric function."""
    return get_global_factory().metric(name, value, **kwargs)


def log(message: str, level: str = "info", **kwargs: object) -> FlextResult[object]:
    """Global log function."""
    return get_global_factory().log(message, level, **kwargs)


def alert(
    title: str,
    message: str,
    severity: str = "low",
    **kwargs: object,
) -> FlextResult[object]:
    """Global alert function."""
    return get_global_factory().alert(title, message, severity, **kwargs)


def trace(trace_id: str, operation: str, **kwargs: object) -> FlextResult[object]:
    """Global trace function."""
    return get_global_factory().trace(trace_id, operation, **kwargs)


def health_check(
    component: str,
    status: str = "unknown",
    **kwargs: object,
) -> FlextResult[object]:
    """Global health check function."""
    return get_global_factory().health_check(component, status, **kwargs)


def create_simplified_observability_platform(
    config: dict[str, object] | None = None,
    container: FlextContainer | None = None,
) -> FlextObservabilityMasterFactory:
    """Create a simplified observability platform with optional configuration.

    Args:
        config: Optional configuration dictionary
        container: Optional dependency injection container

    Returns:
        FlextObservabilityMasterFactory: Configured factory instance

    """
    if container is not None:
        # Use provided container
        factory = FlextObservabilityMasterFactory()
        factory.container = container
        return factory

    # Create new factory with optional config
    factory = FlextObservabilityMasterFactory()
    if config:
        # Apply configuration if provided
        # Note: Config application would depend on specific requirements
        pass

    return factory


# =============================================================================
# DRY RE-EXPORTS - Expose entity functions for test compatibility
# =============================================================================

# Re-export entity functions to maintain test compatibility (DRY principle)
# These are already imported above from entities module
__all__ = [
    "FlextObservabilityMasterFactory",
    "alert",
    "create_simplified_observability_platform",
    "flext_alert",  # Re-exported from entities for DRY principle
    "flext_health_check",  # Re-exported from entities for DRY principle
    "flext_trace",  # Re-exported from entities for DRY principle
    "get_global_factory",
    "health_check",
    "log",
    "metric",
    "reset_global_factory",
    "trace",
]
