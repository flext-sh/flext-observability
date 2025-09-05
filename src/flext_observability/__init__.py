"""Production-grade observability library for FLEXT ecosystem."""

from __future__ import annotations

# Remove unused TYPE_CHECKING - not needed

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Import FlextLogger from flext_core
from flext_core import FlextContainer, FlextLogger, FlextConstants

# Core entities from models module
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)

# Factory patterns from factories module
from flext_observability.factories import (
    FlextObservabilityMasterFactory,
    alert,
    get_global_factory,
    health_check,
    log,
    metric,
    reset_global_factory,
    trace,
)

# Monitor patterns from monitoring module
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Simple API from api module
from flext_observability.api import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

# Services from services module
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


def flext_health_status() -> dict[str, str]:
    """Return basic health status using flext-core patterns."""
    return {
        "status": "healthy",
        "service": "flext-observability",
        "version": "0.9.0",
    }


# Legacy facades removed - use direct imports from flext-core and factory classes

__all__: list[str] = [
    # Core entities
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextTrace",
    # Entity factory functions
    "flext_alert",
    "flext_health_check",
    "flext_metric",
    "flext_trace",
    # Services
    "FlextAlertService",
    "FlextHealthService",
    "FlextLoggingService",
    "FlextMetricsService",
    "FlextTracingService",
    # Factory
    "FlextObservabilityMasterFactory",
    "get_global_factory",
    "reset_global_factory",
    # Monitoring
    "FlextObservabilityMonitor",
    "flext_monitor_function",
    # Simple API
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    # Global convenience functions
    "alert",
    "health_check",
    "log",
    "metric",
    "trace",
    # Health check
    "flext_health_status",
    # Version info
    "__version__",
    "__version_info__",
    # flext-core re-exports
    "FlextContainer",
    "FlextConstants",
    "FlextLogger",
]
