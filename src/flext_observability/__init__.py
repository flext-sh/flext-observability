"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

"""Production-grade observability library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


# Remove unused TYPE_CHECKING - not needed

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Import FlextLogger from flext_core
from flext_core import FlextConstants, FlextContainer, FlextLogger

# Simple API from api module
from flext_observability.api import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
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

# Monitor patterns from monitoring module
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Services from services module
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


def flext_health_status() -> FlextTypes.Core.Headers:
    """Return basic health status using flext-core patterns."""
    return {
        "status": "healthy",
        "service": "flext-observability",
        "version": "0.9.0",
    }


# Legacy facades removed - use direct imports from flext-core and factory classes

__all__: FlextTypes.Core.StringList = [
    # Core entities
    "FlextAlert",
    # Services
    "FlextAlertService",
    "FlextConstants",
    # flext-core re-exports
    "FlextContainer",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLogger",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    # Factory
    "FlextObservabilityMasterFactory",
    # Monitoring
    "FlextObservabilityMonitor",
    "FlextTrace",
    "FlextTracingService",
    # Version info
    "__version__",
    "__version_info__",
    # Global convenience functions
    "alert",
    # Entity factory functions
    "flext_alert",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    # Health check
    "flext_health_status",
    "flext_metric",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "health_check",
    "log",
    "metric",
    "reset_global_factory",
    "trace",
]
