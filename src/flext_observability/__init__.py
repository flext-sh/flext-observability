"""FLEXT Observability - Centralized observability patterns for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Main entry point for flext-observability package.
"""

from __future__ import annotations

__version__ = "1.0.0"

# Core entities and types
from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)

# Factory patterns
from flext_observability.factory import FlextObservabilityMasterFactory

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
        "version": "1.0.0",
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
    # Simple API
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    # Utils
    "flext_health_status",
    "flext_monitor_function",
]
