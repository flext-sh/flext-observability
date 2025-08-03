"""FLEXT Observability Platform - Unified Observability Orchestration.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Unified observability platform implementing comprehensive orchestration of
metrics collection, distributed tracing, alert management, health monitoring,
and structured logging for the FLEXT ecosystem. Provides high-level platform
abstraction coordinating multiple observability services through factory patterns
and dependency injection with enterprise-grade reliability and performance.

This module implements the Platform pattern, providing a unified interface to
the complex observability ecosystem while maintaining Clean Architecture
boundaries and enabling comprehensive observability across distributed services.
The platform coordinates factory patterns, service orchestration, and configuration
management for seamless observability integration.

Key Components:
    - FlextObservabilityPlatformV2: Main platform orchestrator class
    - create_simplified_observability_platform(): Platform factory function
    - Service coordination through FlextObservabilityMasterFactory
    - Configuration management with intelligent defaults and override support

Architecture:
    Interface Adapters layer in Clean Architecture, providing high-level platform
    abstraction over observability services. Coordinates multiple application
    services while maintaining clean boundaries and dependency inversion.

Integration:
    - Built on flext-core foundation patterns (FlextContainer, FlextResult)
    - Coordinates FlextObservabilityMasterFactory for entity creation
    - Integrates with all observability application services
    - Supports comprehensive observability across FLEXT ecosystem

Example:
    Platform-level observability orchestration:

    >>> from flext_observability.obs_platform import (
    ...     create_simplified_observability_platform
    ... )
    >>> from flext_core import FlextContainer
    >>>
    >>> # Create platform with custom configuration
    >>> config = {
    ...     "metrics_enabled": True,
    ...     "tracing_enabled": True,
    ...     "environment": "production",
    ... }
    >>> platform = create_simplified_observability_platform(config=config)
    >>>
    >>> # Use platform for unified observability operations
    >>> metric_result = platform.metric("api_requests", 42, unit="count")
    >>> trace_result = platform.trace("user_login", "auth-service")
    >>> alert_result = platform.alert("High CPU", "CPU usage above 80%", "warning")

FLEXT Integration:
    Provides the primary platform interface for observability integration across
    all 33 FLEXT ecosystem projects, enabling unified observability orchestration
    with consistent patterns and centralized configuration management.

"""

from __future__ import annotations

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.constants import (
    DEFAULT_OBSERVABILITY_CONFIG,
    ObservabilityConstants,
)
from flext_observability.factory import FlextObservabilityMasterFactory


class FlextObservabilityPlatformV2:
    """Unified Observability Platform for FLEXT Ecosystem Integration.

    Enterprise-grade observability platform implementing comprehensive orchestration
    of metrics collection, distributed tracing, alert management, health monitoring,
    and structured logging. Provides high-level abstraction layer coordinating
    multiple observability services through factory patterns and dependency injection.

    This platform serves as the primary entry point for observability operations
    across the FLEXT ecosystem, coordinating complex observability workflows while
    providing simple, consistent interfaces. Implements platform patterns with
    configuration management, service orchestration, and comprehensive error handling.

    Responsibilities:
        - Unified interface for all observability operations
        - Configuration management with intelligent defaults and overrides
        - Service orchestration through factory pattern coordination
        - Dependency injection container management and service registration
        - Performance optimization and resource management
        - Enterprise-grade error handling and logging

    Platform Services Integration:
        - Metrics: FlextMetricsService via FlextObservabilityMasterFactory
        - Tracing: FlextTracingService for distributed trace coordination
        - Alerting: FlextAlertService for alert processing and routing
        - Health: FlextHealthService for component health monitoring
        - Logging: FlextLoggingService for structured log management

    Attributes:
        name (str): Platform identifier for service discovery and configuration
        version (str): Platform version for compatibility and feature support
        config (Dict[str, object]): Merged platform configuration with defaults
        container (FlextContainer): Dependency injection container for services
        logger: Structured logger for platform operations and diagnostics
        _factory (FlextObservabilityMasterFactory): Central factory for entity creation

    Configuration:
        Platform accepts configuration dictionaries with the following structure:
        - metrics_enabled (bool): Enable metrics collection and export
        - tracing_enabled (bool): Enable distributed tracing capabilities
        - alerting_enabled (bool): Enable alert processing and routing
        - health_enabled (bool): Enable health monitoring and checks
        - environment (str): Deployment environment (development, staging, production)
        - service_name (str): Service identifier for observability correlation

    Example:
        Complete platform initialization and usage:

        >>> from flext_observability.obs_platform import FlextObservabilityPlatformV2
        >>> from flext_core import FlextContainer
        >>>
        >>> # Create platform with custom configuration
        >>> config = {
        ...     "metrics_enabled": True,
        ...     "tracing_enabled": True,
        ...     "environment": "production",
        ...     "service_name": "user-api",
        ... }
        >>> container = FlextContainer()
        >>> platform = FlextObservabilityPlatformV2(config=config, container=container)
        >>>
        >>> # Record business metrics
        >>> metric_result = platform.metric(
        ...     name="api_response_time",
        ...     value=150.5,
        ...     unit="milliseconds",
        ...     tags={"endpoint": "/users", "method": "GET"},
        ... )
        >>>
        >>> # Create distributed traces
        >>> trace_result = platform.trace(
        ...     trace_id="trace_abc123",
        ...     operation="user_authentication",
        ...     span_attributes={"user_id": "12345", "session_id": "sess_xyz"},
        ... )
        >>>
        >>> # Generate alerts for operational issues
        >>> alert_result = platform.alert(
        ...     title="High Response Time",
        ...     message="API response time exceeded 200ms threshold",
        ...     severity="warning",
        ...     tags={"service": "user-api", "environment": "production"},
        ... )

    Thread Safety:
        Platform operations are thread-safe through factory service coordination,
        supporting concurrent observability operations from multiple threads without
        data corruption or configuration inconsistencies.

    Architecture:
        Interface Adapters layer platform providing high-level abstraction over
        observability services. Maintains Clean Architecture boundaries while
        coordinating multiple application services and domain entities.

    """

    def __init__(
        self,
        config: dict[str, object] | None = None,
        container: FlextContainer | None = None,
    ) -> None:
        """Initialize unified observability platform with configuration and services.

        Args:
            config: Optional platform configuration dictionary with observability
                settings. Merged with intelligent defaults to provide comprehensive
                configuration. Supports metrics, tracing, alerting, health, and
                environment-specific settings.
            container: Optional dependency injection container for service coordination.
                Defaults to new FlextContainer if not provided. Used for service
                registration and dependency management across observability components.

        """
        merged_config = {**DEFAULT_OBSERVABILITY_CONFIG, **(config or {})}

        self.name = ObservabilityConstants.NAME
        self.version = ObservabilityConstants.VERSION
        self.config = merged_config
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

        # Use factory for all operations
        self._factory = FlextObservabilityMasterFactory(self.container)

    def metric(
        self,
        name: str,
        value: float,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create and record metric through platform factory coordination.

        Args:
            name: Metric identifier following observability naming conventions
            value: Numeric measurement value with high precision support
            **kwargs: Additional metric parameters including unit, tags, timestamp

        Returns:
            FlextResult[object]: Success with recorded metric entity or failure
            with detailed error message for debugging and monitoring

        """
        return self._factory.metric(name, value, **kwargs)

    def log(
        self,
        message: str,
        level: str = "info",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create structured log entry through platform factory coordination.

        Args:
            message: Log message content with descriptive information
            level: Log severity level (debug, info, warning, error, critical)
            **kwargs: Additional log parameters including context, timestamp

        Returns:
            FlextResult[object]: Success with log entry entity or failure
            with detailed error message for debugging and monitoring

        """
        return self._factory.log(message, level, **kwargs)

    def alert(
        self,
        title: str,
        message: str,
        severity: str = "low",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create alert through platform factory coordination.

        Args:
            title: Alert title summarizing the issue for identification
            message: Detailed alert description with diagnostic information
            severity: Alert severity (low, medium, high, critical, emergency)
            **kwargs: Additional alert parameters including tags, status, timestamp

        Returns:
            FlextResult[object]: Success with alert entity or failure
            with detailed error message for debugging and monitoring

        """
        return self._factory.alert(title, message, severity, **kwargs)

    def trace(
        self,
        trace_id: str,
        operation: str,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create distributed trace through platform factory coordination.

        Args:
            trace_id: Unique trace identifier for distributed correlation
            operation: Operation name describing the business logic being traced
            **kwargs: Additional trace parameters including span_id, attributes,
                duration

        Returns:
            FlextResult[object]: Success with trace entity or failure
            with detailed error message for debugging and monitoring

        """
        return self._factory.trace(trace_id, operation, **kwargs)

    def health_check(self) -> FlextResult[dict[str, object]]:
        """Get overall platform health status through factory coordination.

        Returns:
            FlextResult[Dict[str, object]]: Success with health status dictionary
            or failure with detailed error message for debugging and monitoring

        """
        return self._factory.health_status()


def create_simplified_observability_platform(
    config: dict[str, object] | None = None,
    container: FlextContainer | None = None,
) -> FlextObservabilityPlatformV2:
    """Create unified observability platform with intelligent configuration defaults.

    Convenient factory function for creating FlextObservabilityPlatformV2 instances
    with minimal parameters and intelligent configuration merging. Provides
    rapid platform setup for observability integration across FLEXT ecosystem
    components with enterprise-grade defaults.

    Args:
        config: Optional platform configuration dictionary with observability
            settings. Merged with intelligent defaults for comprehensive
            observability coverage. Supports environment-specific overrides.
        container: Optional dependency injection container for service coordination.
            Defaults to new FlextContainer with automatic service registration
            and dependency management.

    Returns:
        FlextObservabilityPlatformV2: Configured platform instance ready for
        observability operations with factory patterns and service coordination.

    Example:
        Quick platform creation for immediate observability:

        >>> platform = create_simplified_observability_platform({
        ...     "environment": "production",
        ...     "service_name": "user-api",
        ... })
        >>> metric_result = platform.metric("requests", 1, unit="count")

    """
    return FlextObservabilityPlatformV2(config=config, container=container)


# Compatibility alias
FlextObservabilityPlatformSimplified = FlextObservabilityPlatformV2
