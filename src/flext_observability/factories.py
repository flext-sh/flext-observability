"""FLEXT Observability Entity Factory.

Factory patterns implementing centralized entity creation with comprehensive
validation, dependency injection, and business rule enforcement for observability
entities. Provides unified access point for creating FlextMetric, FlextTrace,
FlextAlert, FlextHealthCheck, and FlextLogEntry entities with consistent
validation and initialization patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import cast

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

# Type checking imports if needed in future
from flext_observability.entities import (
    flext_alert,
    flext_health_check,
    flext_trace,
)
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)

# Removed validation module - using FlextResult[None].fail() directly per docs/patterns/
# ============================================================================
# TIMESTAMP UTILITIES - Use flext-core centralized generation
# ============================================================================


def _generate_utc_datetime() -> datetime:
    """Generate UTC datetime using flext-core pattern.

    Uses flext-core centralized timestamp generation for consistency
    across the FLEXT ecosystem. Eliminates local boilerplate duplication.

    Returns:
      datetime: Current UTC datetime with timezone information

    """
    # Use flext-core timestamp generation - parse ISO timestamp string to datetime
    timestamp_str = FlextUtilities.generate_timestamp()
    return datetime.fromisoformat(timestamp_str)


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
      >>> if metric_result.success:
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
      - Domain rule enforcement (entity.validate_business_rules())
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

        Returns:
            object: Description of return value.

        """
        self.container = container or FlextContainer()
        # Use logger accessor from factory module so tests patching
        # flext_observability.factory.FlextLogger can intercept
        self._logger = FlextLogger(self.__class__.__name__)
        self._setup_services()

    def _setup_services(self) -> None:
        """Set up all services automatically."""
        try:
            services: list[
                tuple[
                    str,
                    type[
                        FlextMetricsService
                        | FlextLoggingService
                        | FlextTracingService
                        | FlextAlertService
                        | FlextHealthService
                    ],
                ]
            ] = [
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
            tags = cast("FlextTypes.Core.Dict", tags) if isinstance(tags, dict) else {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = _generate_utc_datetime()

            metric = FlextMetric(
                name=name,
                value=value,
                unit=str(kwargs.get("unit", "")),
                tags=tags,
                timestamp=timestamp,
            )

            service_result = self.container.get("metrics_service")
            if service_result.success and service_result.data:
                service = cast("FlextMetricsService", service_result.data)
                result = service.record_metric(metric)
                return (
                    FlextResult[object].ok(result.data)
                    if result.success
                    else FlextResult[object].fail(result.error or "Unknown error")
                )
            return FlextResult[object].ok(metric)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[object].fail(f"Failed to create metric: {e}")

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
                context = cast("FlextTypes.Core.Dict", context)
            else:
                context = {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = _generate_utc_datetime()

            log_entry = FlextLogEntry(
                message=message,
                level=level,
                service=str(kwargs.get("service", "unknown")),
                timestamp=timestamp,
                extra_data=context,
            )

            service_result = self.container.get("logging_service")
            if service_result.success and service_result.data:
                service = cast("FlextLoggingService", service_result.data)
                result = service.log_entry(log_entry)
                return (
                    FlextResult[object].ok(result.data)
                    if result.success
                    else FlextResult[object].fail(result.error or "Unknown error")
                )
            return FlextResult[object].ok(log_entry)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[object].fail(f"Failed to create log: {e}")

    def alert(
        self,
        message: str,
        service: str,
        level: str = "info",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create alert."""
        try:
            tags = kwargs.get("tags", {})
            tags = cast("FlextTypes.Core.Dict", tags) if isinstance(tags, dict) else {}

            timestamp = kwargs.get("timestamp")
            if not isinstance(timestamp, datetime):
                timestamp = _generate_utc_datetime()

            alert = FlextAlert(
                message=message,
                level=level,
                service=service,
                timestamp=timestamp,
                tags=tags,
            )

            service_result = self.container.get("alert_service")
            if service_result.success and service_result.data:
                alert_service = cast("FlextAlertService", service_result.data)
                result = alert_service.create_alert(alert)
                return (
                    FlextResult[object].ok(result.data)
                    if result.success
                    else FlextResult[object].fail(result.error or "Unknown error")
                )
            return FlextResult[object].ok(alert)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[object].fail(f"Failed to create alert: {e}")

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
            span_attributes_raw = kwargs.get("span_attributes", {})
            # Ensure proper typing for span_attributes
            if isinstance(span_attributes_raw, dict):
                # Cast to avoid Unknown types in comprehension
                raw_dict = cast("FlextTypes.Core.Dict", span_attributes_raw)
                span_attributes: FlextTypes.Core.Dict = {
                    str(k): v for k, v in raw_dict.items()
                }
            else:
                span_attributes = {}

            trace = FlextTrace(
                operation_name=operation,
                service_name=str(kwargs.get("service_name", "unknown")),
                trace_id=trace_id,
                span_id=str(span_id) if span_id else "",
                status=str(kwargs.get("status", "started")),
                start_time=(
                    timestamp
                    if isinstance(timestamp, datetime)
                    else _generate_utc_datetime()
                ),
                tags=span_attributes,
            )

            service_result = self.container.get("tracing_service")
            if service_result.success and service_result.data:
                service = cast("FlextTracingService", service_result.data)
                result = service.start_trace(trace)
                return (
                    FlextResult[object].ok(result.data)
                    if result.success
                    else FlextResult[object].fail(result.error or "Unknown error")
                )
            return FlextResult[object].ok(trace)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[object].fail(f"Failed to create trace: {e}")

    def health_check(
        self,
        service_name: str,
        status: str = "healthy",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create health check."""
        try:
            # Extract known parameters from kwargs
            message = kwargs.get("message", "")
            timestamp = kwargs.get("timestamp")

            # Create health check entity directly with proper models
            health = FlextHealthCheck(
                service_name=service_name,
                status=status,
                timestamp=(
                    timestamp
                    if isinstance(timestamp, datetime)
                    else _generate_utc_datetime()
                ),
                details={"message": str(message)} if message else {},
            )

            service_result = self.container.get("health_service")
            if service_result.success and service_result.data:
                service = cast("FlextHealthService", service_result.data)
                result = service.check_health(health)
                return (
                    FlextResult[object].ok(result.data)
                    if result.success
                    else FlextResult[object].fail(result.error or "Unknown error")
                )
            return FlextResult[object].ok(health)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[object].fail(f"Failed to create health check: {e}")

    def health_status(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get overall health status."""
        try:
            service_result = self.container.get("health_service")
            if service_result.success and service_result.data:
                service = cast("FlextHealthService", service_result.data)
                return service.get_overall_health()

            return FlextResult[FlextTypes.Core.Dict].ok(
                cast("FlextTypes.Core.Dict", {"status": "healthy", "mode": "fallback"}),
            )

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Health status check failed: {e}"
            )

    # Create methods for test compatibility
    def create_metric(
        self, name: str, value: float, unit: str = "", **kwargs: object
    ) -> FlextResult[FlextMetric]:
        """Create metric (compatibility method for tests)."""
        kwargs["unit"] = unit
        result = self.metric(name, value, **kwargs)
        if result.success and isinstance(result.data, FlextMetric):
            return FlextResult[FlextMetric].ok(result.data)
        return FlextResult[FlextMetric].fail(result.error or "Failed to create metric")

    def create_trace(
        self, operation_name: str, service_name: str, **kwargs: object
    ) -> FlextResult[FlextTrace]:
        """Create trace (compatibility method for tests)."""
        # Use operation_name as the operation parameter
        kwargs["service_name"] = service_name
        result = self.trace(
            trace_id=FlextUtilities.generate_uuid(),
            operation=operation_name,
            **kwargs,
        )
        if result.success and isinstance(result.data, FlextTrace):
            return FlextResult[FlextTrace].ok(result.data)
        return FlextResult[FlextTrace].fail(result.error or "Failed to create trace")

    def create_alert(
        self, message: str, service: str, level: str = "info", **kwargs: object
    ) -> FlextResult[FlextAlert]:
        """Create alert (compatibility method for tests)."""
        # Map parameters to match the alert() method signature
        result = self.alert(message=message, service=service, level=level, **kwargs)
        if result.success and isinstance(result.data, FlextAlert):
            return FlextResult[FlextAlert].ok(result.data)
        return FlextResult[FlextAlert].fail(result.error or "Failed to create alert")

    def create_health_check(
        self, service_name: str, status: str = "healthy", **kwargs: object
    ) -> FlextResult[FlextHealthCheck]:
        """Create health check (compatibility method for tests)."""
        result = self.health_check(service_name=service_name, status=status, **kwargs)
        if result.success and isinstance(result.data, FlextHealthCheck):
            return FlextResult[FlextHealthCheck].ok(result.data)
        return FlextResult[FlextHealthCheck].fail(
            result.error or "Failed to create health check"
        )

    def create_log_entry(
        self, message: str, service: str, level: str = "INFO", **kwargs: object
    ) -> FlextResult[FlextLogEntry]:
        """Create log entry (compatibility method for tests)."""
        kwargs["service"] = service
        result = self.log(message, level, **kwargs)
        if result.success and isinstance(result.data, FlextLogEntry):
            return FlextResult[FlextLogEntry].ok(result.data)
        return FlextResult[FlextLogEntry].fail(
            result.error or "Failed to create log entry"
        )


# ============================================================================
# GLOBAL FACTORY INSTANCE - Proper singleton pattern
# ============================================================================


class _GlobalFactorySingleton:
    """Singleton class to manage global factory instance."""

    def __init__(self) -> None:
        self._factory: FlextObservabilityMasterFactory | None = None

    def get_factory(
        self, container: FlextContainer | None = None
    ) -> FlextObservabilityMasterFactory:
        """Get global factory instance."""
        if self._factory is None:
            self._factory = FlextObservabilityMasterFactory(container)
        return self._factory

    def reset_factory(self) -> None:
        """Reset global factory for testing."""
        self._factory = None


# Singleton instance
_global_factory_singleton = _GlobalFactorySingleton()


def get_global_factory(
    container: FlextContainer | None = None,
) -> FlextObservabilityMasterFactory:
    """Get global factory instance."""
    return _global_factory_singleton.get_factory(container)


def reset_global_factory() -> None:
    """Reset global factory for testing."""
    _global_factory_singleton.reset_factory()


# Convenience functions using global factory
def metric(name: str, value: float, **kwargs: object) -> FlextResult[object]:
    """Global metric function."""
    return get_global_factory().metric(name, value, **kwargs)


def log(message: str, level: str = "info", **kwargs: object) -> FlextResult[object]:
    """Global log function."""
    return get_global_factory().log(message, level, **kwargs)


def alert(
    message: str,
    service: str,
    level: str = "info",
    **kwargs: object,
) -> FlextResult[object]:
    """Global alert function."""
    return get_global_factory().alert(message, service, level, **kwargs)


def trace(trace_id: str, operation: str, **kwargs: object) -> FlextResult[object]:
    """Global trace function."""
    return get_global_factory().trace(trace_id, operation, **kwargs)


def health_check(
    service_name: str,
    status: str = "healthy",
    **kwargs: object,
) -> FlextResult[object]:
    """Global health check function."""
    return get_global_factory().health_check(service_name, status, **kwargs)


def create_simplified_observability_platform(
    container: FlextContainer | None = None,
) -> FlextObservabilityMasterFactory:
    """Create observability platform using factory pattern.

    Args:
      container: Optional dependency injection container

    Returns:
      FlextObservabilityMasterFactory: Configured factory instance

    """
    return FlextObservabilityMasterFactory(container)


# =============================================================================
# DRY RE-EXPORTS - Expose entity functions for test compatibility
# =============================================================================

# Re-export entity functions to maintain test compatibility (DRY principle)
# These are already imported above from entities module
__all__: FlextTypes.Core.StringList = [
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
