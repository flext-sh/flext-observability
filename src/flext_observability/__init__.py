"""FLEXT Observability - Centralized observability patterns for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Main entry point for flext-observability package.
"""

from __future__ import annotations

__version__ = "0.9.0"

# Core entities and types
# Import get_logger from flext_core for convenience
from flext_core import get_logger

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_trace,
)

# Factory patterns
from flext_observability.factory import (
    FlextObservabilityMasterFactory,
    alert,
    create_simplified_observability_platform,
    get_global_factory,
    health_check,
    log,
    metric,
    reset_global_factory,
    trace,
)

# Monitor patterns
from flext_observability.flext_monitor import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Simple API
from flext_observability.flext_simple import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

# Platform
from flext_observability.obs_platform import FlextObservabilityPlatformV2

# Services
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


# Health check function
def flext_health_status() -> dict[str, str]:
    """Get basic health status."""
    return {
        "status": "healthy",
        "service": "flext-observability",
        "version": "0.9.0",
    }


__all__ = [
    # Entities
    "FlextAlert",
    # Services
    "FlextAlertService",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    # Factory
    "FlextObservabilityMasterFactory",
    # Monitor
    "FlextObservabilityMonitor",
    # Platform
    "FlextObservabilityPlatformV2",
    "FlextTrace",
    "FlextTracingService",
    # Global functions
    "alert",
    "create_simplified_observability_platform",
    # Entity factory functions
    "flext_alert",
    # Simple API
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    # Utils
    "flext_health_status",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "get_logger",
    "health_check",
    "log",
    "metric",
    "reset_global_factory",
    "trace",
]
