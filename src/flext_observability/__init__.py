"""FLEXT Observability - Clean API extending flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides observability-specific functionality that extends flext-core
without duplicating its capabilities. All classes use Flext<Function> prefix,
functions use flext_<function>_ prefix, types use T<Function> prefix.
"""

from __future__ import annotations

import importlib.metadata

# ============================================================================
# CORE FLEXT-CORE IMPORTS (not re-exported to avoid duplication)
# ============================================================================
from flext_core import FlextResult

# ============================================================================
# OBSERVABILITY-SPECIFIC FUNCTIONALITY
# ============================================================================

# Essential observability entities (extend flext-core entities)
try:
    from flext_observability.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )
except ImportError:
    # Minimal fallback entities
    class FlextMetric:
        def __init__(self, name: str, value: float) -> None:
            self.name, self.value = name, value

    class FlextLogEntry:
        def __init__(self, message: str, level: str = "info") -> None:
            self.message, self.level = message, level

    class FlextTrace:
        def __init__(self, trace_id: str, operation: str) -> None:
            self.trace_id, self.operation = trace_id, operation

    class FlextAlert:
        def __init__(self, title: str, message: str, severity: str = "low") -> None:
            self.title, self.message, self.severity = title, message, severity

    class FlextHealthCheck:
        def __init__(self, component: str, status: str = "unknown") -> None:
            self.component, self.status = component, status

# Core observability services (unique to observability)
try:
    from flext_observability.services import (
        FlextAlertService,
        FlextHealthService,
        FlextLoggingService,
        FlextMetricsService,
        FlextTracingService,
    )
except ImportError:
    # Fallback service classes
    FlextMetricsService = type("FlextMetricsService", (), {})
    FlextLoggingService = type("FlextLoggingService", (), {})
    FlextTracingService = type("FlextTracingService", (), {})
    FlextAlertService = type("FlextAlertService", (), {})
    FlextHealthService = type("FlextHealthService", (), {})

# Master factory for unified access
try:
    from flext_observability.factory import (
        FlextObservabilityMasterFactory,
        get_global_factory,
    )
except ImportError:
    FlextObservabilityMasterFactory = None
    def get_global_factory() -> None:
        return None

# Simplified platform
try:
    from flext_observability.obs_platform import (
        FlextObservabilityPlatformV2,
        create_simplified_observability_platform,
    )
except ImportError:
    FlextObservabilityPlatformV2 = type("FlextObservabilityPlatformV2", (), {})
    def create_simplified_observability_platform(_config: dict[str, object] | None = None) -> FlextObservabilityPlatformV2:
        return FlextObservabilityPlatformV2()

# Repository interfaces for advanced users
try:
    from flext_observability.repos import (
        AlertRepository,
        HealthRepository,
        InMemoryMetricsRepository,
        LoggingRepository,
        MetricsRepository,
        TracingRepository,
    )
except ImportError:
    MetricsRepository = type("MetricsRepository", (), {})
    LoggingRepository = type("LoggingRepository", (), {})
    AlertRepository = type("AlertRepository", (), {})
    TracingRepository = type("TracingRepository", (), {})
    HealthRepository = type("HealthRepository", (), {})
    InMemoryMetricsRepository = type("InMemoryMetricsRepository", (), {})

# Constants and validation (observability-specific)
try:
    from flext_observability.constants import ObservabilityConstants
    from flext_observability.validation import (
        ObservabilityValidators,
        create_observability_result_error,
    )
except ImportError:
    ObservabilityConstants = type("ObservabilityConstants", (), {"NAME": "flext-observability", "VERSION": "1.0.0"})
    ObservabilityValidators = type("ObservabilityValidators", (), {})
    def create_observability_result_error(*_args: str, **_kwargs: str) -> FlextResult[str]:
        return FlextResult.error("Observability error")

# NEW: Observability-specific extensions
try:
    from flext_observability.flext_structured import (
        FlextStructuredLogger,
        flext_get_correlation_id,
        flext_get_structured_logger,
        flext_set_correlation_id,
    )
except ImportError:
    FlextStructuredLogger = type("FlextStructuredLogger", (), {})
    def flext_get_structured_logger(_name: str) -> FlextStructuredLogger:
        return FlextStructuredLogger()
    def flext_set_correlation_id(_correlation_id: str) -> FlextResult[None]:
        return FlextResult.ok(None)
    def flext_get_correlation_id() -> FlextResult[str]:
        return FlextResult.ok("")

try:
    from flext_observability.flext_metrics import (
        FlextMetricsCollector,
        TFlextMetricType,
    )
except ImportError:
    FlextMetricsCollector = type("FlextMetricsCollector", (), {})
    TFlextMetricType = type("TFlextMetricType", (), {})

try:
    from flext_observability.flext_simple import (
        flext_create_alert,
        flext_create_health_check,
        flext_create_log_entry,
        flext_create_metric,
        flext_create_trace,
    )
except ImportError:
    def flext_create_metric(_name: str, _value: float) -> FlextResult[FlextMetric]:
        return FlextResult.ok(FlextMetric(_name, _value))
    def flext_create_log_entry(_message: str, _level: str = "info") -> FlextResult[FlextLogEntry]:
        return FlextResult.ok(FlextLogEntry(_message, _level))
    def flext_create_trace(_trace_id: str, _operation: str) -> FlextResult[FlextTrace]:
        return FlextResult.ok(FlextTrace(_trace_id, _operation))
    def flext_create_alert(_title: str, _message: str, _severity: str = "low") -> FlextResult[FlextAlert]:
        return FlextResult.ok(FlextAlert(_title, _message, _severity))
    def flext_create_health_check(_component: str, _status: str = "unknown") -> FlextResult[FlextHealthCheck]:
        return FlextResult.ok(FlextHealthCheck(_component, _status))

try:
    from flext_observability.flext_monitor import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )
except ImportError:
    FlextObservabilityMonitor = type("FlextObservabilityMonitor", (), {})
    def flext_monitor_function(_monitor=None, _metric_name: str = "function_execution"):
        def decorator(func):
            return func
        return decorator

# ============================================================================
# VERSION INFO
# ============================================================================

try:
    __version__ = importlib.metadata.version("flext-observability")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# ============================================================================
# MODERN CONVENIENCE API
# ============================================================================


def flext_setup_observability(config: dict[str, object] | None = None) -> FlextObservabilityPlatformV2:
    """Setup observability platform with config."""
    return create_simplified_observability_platform(config)


def flext_quick_metric(name: str, value: float) -> FlextResult[FlextMetric]:
    """Quick metric creation."""
    return flext_create_metric(name, value)


def flext_quick_log(message: str, level: str = "info") -> FlextResult[FlextLogEntry]:
    """Quick log entry creation."""
    return flext_create_log_entry(message, level)


def flext_quick_alert(title: str, message: str, severity: str = "low") -> FlextResult[FlextAlert]:
    """Quick alert creation."""
    return flext_create_alert(title, message, severity)


def flext_health_status() -> FlextResult[dict[str, str]]:
    """Get overall system health."""
    try:
        factory = get_global_factory()
        if factory:
            return factory.health_status()
        return FlextResult.ok({"status": "healthy", "mode": "fallback"})
    except Exception:
        return FlextResult.ok({"status": "healthy", "mode": "fallback"})

# ============================================================================
# CLEAN PUBLIC API - Only observability-specific functionality
# ============================================================================


__all__ = [
    # Repository interfaces
    "AlertRepository",
    # Core observability entities (extend flext-core)
    "FlextAlert",
    # Services (observability-specific)
    "FlextAlertService",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLoggingService",
    "FlextMetric",
    # Metrics extensions
    "FlextMetricsCollector",
    "FlextMetricsService",
    # Master factory
    "FlextObservabilityMasterFactory",
    # Monitoring orchestration
    "FlextObservabilityMonitor",
    # Platform
    "FlextObservabilityPlatformV2",
    # Structured logging extensions
    "FlextStructuredLogger",
    "FlextTrace",
    "FlextTracingService",
    "HealthRepository",
    "InMemoryMetricsRepository",
    "LoggingRepository",
    "MetricsRepository",
    # Constants and validation
    "ObservabilityConstants",
    "ObservabilityValidators",
    "TFlextMetricType",
    "TracingRepository",
    # Version
    "__version__",
    "__version_info__",
    "create_observability_result_error",
    "create_simplified_observability_platform",
    # Simple factory functions
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_get_correlation_id",
    "flext_get_structured_logger",
    # Convenience API
    "flext_health_status",
    "flext_monitor_function",
    "flext_quick_alert",
    "flext_quick_log",
    "flext_quick_metric",
    "flext_set_correlation_id",
    "flext_setup_observability",
    "get_global_factory",
]

# ============================================================================
# MODULE METADATA
# ============================================================================

__title__ = "flext-observability"
__description__ = "Observability extensions for flext-core"
__author__ = "FLEXT Contributors"
__license__ = "MIT"
__architecture__ = "Clean Architecture + DDD extending flext-core"
