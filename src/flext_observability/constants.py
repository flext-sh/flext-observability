"""FLEXT Observability Domain Constants.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain constants defining business rules, validation thresholds, and system
constraints for observability operations across the FLEXT ecosystem. Provides
centralized configuration constants supporting metrics collection, distributed
tracing, health monitoring, alerting, and structured logging with consistent
business rule enforcement.

This module implements the Constants pattern, providing immutable configuration
values that support domain validation, business rule enforcement, and system
constraints. All constants are organized by functional area and provide
clear separation between technical limits and business policies.

Key Components:
    - ObservabilityConstants: Core system constants and version information
    - Validation thresholds for entity creation and processing
    - Business rule constants for domain validation
    - System limits and performance constraints
    - Default values for optional parameters

Architecture:
    Domain layer constants supporting entity validation and business rule
    enforcement. Provides immutable configuration values while maintaining
    separation of concerns and supporting consistent validation patterns.

Integration:
    - Used by domain entities for validation thresholds
    - Referenced by application services for business rule enforcement
    - Supports validation logic with consistent constraint definitions
    - Provides system limits for performance and scalability

Example:
    Domain validation using observability constants:

    >>> from flext_observability.constants import ObservabilityConstants
    >>> # Check valid log levels
    >>> valid_levels = ObservabilityConstants.LOG_LEVELS
    >>> assert "info" in valid_levels
    >>> # Validate alert severity
    >>> valid_severities = ObservabilityConstants.ALERT_SEVERITIES
    >>> assert "critical" in valid_severities
    >>> # Check system version
    >>> version = ObservabilityConstants.VERSION
    >>> print(f"FLEXT Observability v{version}")

FLEXT Integration:
    Provides centralized constants for observability validation and business
    rules across all 33 FLEXT ecosystem projects, ensuring consistent behavior
    and constraint enforcement throughout the distributed data integration platform.

"""

from __future__ import annotations

from typing import ClassVar

# ============================================================================
# CORE OBSERVABILITY CONSTANTS
# ============================================================================


class ObservabilityConstants:
    """Centralized Domain Constants for Observability Business Rules.

    Immutable constants class defining business rules, validation thresholds,
    and system constraints for all observability operations. Provides centralized
    configuration supporting domain validation, business rule enforcement,
    and consistent behavior across distributed FLEXT ecosystem components.

    This class implements the Constants pattern with static class variables,
    ensuring immutable configuration values that support domain validation
    while maintaining clear separation between business policies and
    technical implementation details.

    Constant Categories:
        - System Information: Version, name, and identification constants
        - Validation Thresholds: Business rule enforcement limits
        - Enumeration Values: Valid states for domain entities
        - Performance Limits: System scalability and resource constraints
        - Default Values: Fallback configuration for optional parameters

    Architecture:
        Domain layer constants supporting entity validation and business
        rule enforcement. Provides configuration values that remain constant
        across service deployments while supporting domain-driven validation.

    Example:
        Business rule validation using domain constants:

        >>> # Validate log level against defined enum
        >>> log_level = "info"
        >>> assert log_level in ObservabilityConstants.LOG_LEVELS
        >>> # Check alert severity classification
        >>> severity = "critical"
        >>> assert severity in ObservabilityConstants.ALERT_SEVERITIES
        >>> # Validate health status enum
        >>> health_status = "healthy"
        >>> assert health_status in ObservabilityConstants.HEALTH_STATUSES
        >>> # Check system version for compatibility
        >>> version = ObservabilityConstants.VERSION
        >>> major_version = version.split(".")[0]
        >>> assert int(major_version) >= 0

    Integration:
        Constants are referenced throughout the observability domain:
        - Domain entities use constants for validation rules
        - Application services reference limits and thresholds
        - Interface adapters use defaults and configuration values
        - Infrastructure components respect system constraints

    Immutability:
        All constants are defined as ClassVar to ensure immutability
        and prevent accidental modification during runtime, supporting
        reliable business rule enforcement across service instances.

    """

    NAME = "flext-observability"
    VERSION = "0.9.0"

    # Log levels
    LOG_LEVELS: ClassVar[list[str]] = [
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ]

    # Metric types
    METRIC_TYPES: ClassVar[list[str]] = [
        "counter",
        "gauge",
        "histogram",
        "summary",
    ]

    # Alert severities
    ALERT_SEVERITIES: ClassVar[list[str]] = [
        "low",
        "medium",
        "high",
        "critical",
        "emergency",
    ]

    # Health statuses
    HEALTH_STATUSES: ClassVar[list[str]] = [
        "healthy",
        "unhealthy",
        "degraded",
        "unknown",
    ]

    # Alert statuses
    ALERT_STATUSES: ClassVar[list[str]] = [
        "active",
        "resolved",
        "escalated",
        "suppressed",
    ]


# Default configuration
DEFAULT_OBSERVABILITY_CONFIG: dict[str, object] = {
    "environment": "development",
    "log_level": "info",
    "metrics_enabled": True,
    "logging_enabled": True,
    "tracing_enabled": True,
    "alerts_enabled": True,
    "health_checks_enabled": True,
}


# Error codes for observability
OBSERVABILITY_ERROR_CODES = {
    "METRICS_VALIDATION": "OBSERVABILITY_METRICS_001",
    "LOGGING_ERROR": "OBSERVABILITY_LOGGING_002",
    "TRACING_ERROR": "OBSERVABILITY_TRACING_003",
    "ALERT_ERROR": "OBSERVABILITY_ALERT_004",
    "HEALTH_CHECK_ERROR": "OBSERVABILITY_HEALTH_005",
    "VALIDATION_ERROR": "OBSERVABILITY_VALIDATION_006",
    "CONFIG_ERROR": "OBSERVABILITY_CONFIG_007",
}


# Simplified enums as classes for compatibility
class MetricType:
    """Metric type constants for observability."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertStatus:
    """Alert status constants for observability."""

    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    SUPPRESSED = "suppressed"


class HealthStatus:
    """Health status constants for observability."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class TraceStatus:
    """Trace status constants for observability."""

    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
