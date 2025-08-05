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

from flext_core.constants import FlextSemanticConstants

# =============================================================================
# OBSERVABILITY-SPECIFIC SEMANTIC CONSTANTS - Modern Python 3.13 Structure
# =============================================================================


class FlextObservabilitySemanticConstants(FlextSemanticConstants):
    """Observability semantic constants extending FlextSemanticConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with observability-specific
    values while maintaining full backward compatibility.
    """

    class Core:
        """Core observability system constants."""

        NAME = "flext-observability"
        VERSION = "0.9.0"
        ECOSYSTEM_SIZE = 33

    class Logging:
        """Logging configuration constants."""

        LEVELS: ClassVar[list[str]] = [
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ]

        DEFAULT_LEVEL = "info"
        DEFAULT_FORMAT = "json"

    class Metrics:
        """Metrics collection constants."""

        TYPES: ClassVar[list[str]] = [
            "counter",
            "gauge",
            "histogram",
            "summary",
        ]

        DEFAULT_COLLECTION_INTERVAL = 60
        DEFAULT_RETENTION_DAYS = 30

    class Alerts:
        """Alerting system constants."""

        SEVERITIES: ClassVar[list[str]] = [
            "low",
            "medium",
            "high",
            "critical",
            "emergency",
        ]

        STATUSES: ClassVar[list[str]] = [
            "active",
            "resolved",
            "escalated",
            "suppressed",
        ]

        DEFAULT_TIMEOUT = 300
        MAX_RETRY_ATTEMPTS = 3

    class Health:
        """Health monitoring constants."""

        STATUSES: ClassVar[list[str]] = [
            "healthy",
            "unhealthy",
            "degraded",
            "unknown",
        ]

        DEFAULT_CHECK_INTERVAL = 30
        DEFAULT_TIMEOUT = 10

    class Tracing:
        """Distributed tracing constants."""

        STATUSES: ClassVar[list[str]] = [
            "started",
            "completed",
            "failed",
            "cancelled",
        ]

        DEFAULT_SAMPLING_RATE = 0.1
        MAX_SPAN_ATTRIBUTES = 100

    class Configuration:
        """Configuration management constants."""

        DEFAULT_CONFIG: ClassVar[dict[str, object]] = {
            "environment": "development",
            "log_level": "info",
            "metrics_enabled": True,
            "logging_enabled": True,
            "tracing_enabled": True,
            "alerts_enabled": True,
            "health_checks_enabled": True,
        }

    class ErrorCodes:
        """Error code constants for observability operations."""

        METRICS_VALIDATION = "OBSERVABILITY_METRICS_001"
        LOGGING_ERROR = "OBSERVABILITY_LOGGING_002"
        TRACING_ERROR = "OBSERVABILITY_TRACING_003"
        ALERT_ERROR = "OBSERVABILITY_ALERT_004"
        HEALTH_CHECK_ERROR = "OBSERVABILITY_HEALTH_005"
        VALIDATION_ERROR = "OBSERVABILITY_VALIDATION_006"
        CONFIG_ERROR = "OBSERVABILITY_CONFIG_007"


class FlextObservabilityConstants(FlextObservabilitySemanticConstants):
    """Observability constants with backward compatibility.

    Legacy compatibility layer providing both modern semantic access
    and traditional flat constant access patterns for smooth migration.
    """

    # Modern semantic access (Primary API) - direct references
    Core = FlextObservabilitySemanticConstants.Core
    Logging = FlextObservabilitySemanticConstants.Logging
    Metrics = FlextObservabilitySemanticConstants.Metrics
    Alerts = FlextObservabilitySemanticConstants.Alerts
    Health = FlextObservabilitySemanticConstants.Health
    Tracing = FlextObservabilitySemanticConstants.Tracing
    Configuration = FlextObservabilitySemanticConstants.Configuration
    ErrorCodes = FlextObservabilitySemanticConstants.ErrorCodes

    # Legacy compatibility - flat access patterns (DEPRECATED - use semantic access)
    NAME = FlextObservabilitySemanticConstants.Core.NAME
    VERSION = FlextObservabilitySemanticConstants.Core.VERSION

    LOG_LEVELS = FlextObservabilitySemanticConstants.Logging.LEVELS
    METRIC_TYPES = FlextObservabilitySemanticConstants.Metrics.TYPES
    ALERT_SEVERITIES = FlextObservabilitySemanticConstants.Alerts.SEVERITIES
    ALERT_STATUSES = FlextObservabilitySemanticConstants.Alerts.STATUSES
    HEALTH_STATUSES = FlextObservabilitySemanticConstants.Health.STATUSES


# Legacy class alias (DEPRECATED - use FlextObservabilityConstants)
ObservabilityConstants = FlextObservabilityConstants


# =============================================================================
# LEGACY CONSTANTS - Backward compatibility module-level aliases
# =============================================================================

# Default configuration (DEPRECATED - use FlextObservabilityConstants.Configuration.DEFAULT_CONFIG)
DEFAULT_OBSERVABILITY_CONFIG: dict[str, object] = FlextObservabilitySemanticConstants.Configuration.DEFAULT_CONFIG

# Error codes for observability (DEPRECATED - use FlextObservabilityConstants.ErrorCodes.*)
OBSERVABILITY_ERROR_CODES = {
    "METRICS_VALIDATION": FlextObservabilitySemanticConstants.ErrorCodes.METRICS_VALIDATION,
    "LOGGING_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.LOGGING_ERROR,
    "TRACING_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.TRACING_ERROR,
    "ALERT_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.ALERT_ERROR,
    "HEALTH_CHECK_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.HEALTH_CHECK_ERROR,
    "VALIDATION_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.VALIDATION_ERROR,
    "CONFIG_ERROR": FlextObservabilitySemanticConstants.ErrorCodes.CONFIG_ERROR,
}


# =============================================================================
# LEGACY ENUM CLASSES - Backward compatibility (DEPRECATED - use semantic access)
# =============================================================================


class MetricType:
    """Metric type constants for observability (DEPRECATED - use FlextObservabilityConstants.Metrics.TYPES)."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertStatus:
    """Alert status constants for observability (DEPRECATED - use FlextObservabilityConstants.Alerts.STATUSES)."""

    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    SUPPRESSED = "suppressed"


class HealthStatus:
    """Health status constants for observability (DEPRECATED - use FlextObservabilityConstants.Health.STATUSES)."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class TraceStatus:
    """Trace status constants for observability (DEPRECATED - use FlextObservabilityConstants.Tracing.STATUSES)."""

    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# =============================================================================
# EXPORTS - Observability constants API
# =============================================================================

__all__: list[str] = [
    # Module-level legacy constants
    "DEFAULT_OBSERVABILITY_CONFIG",
    "OBSERVABILITY_ERROR_CODES",
    # Legacy enum classes (deprecated)
    "AlertStatus",
    # Legacy Compatibility (Backward Compatibility)
    "FlextObservabilityConstants",
    # Modern Semantic Constants (Primary API)
    "FlextObservabilitySemanticConstants",
    "HealthStatus",
    "MetricType",
    # Legacy class alias (deprecated)
    "ObservabilityConstants",
    "TraceStatus",
]
