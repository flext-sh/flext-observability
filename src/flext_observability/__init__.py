"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants, FlextContainer, FlextLogger, FlextTypes

# No public API classes currently
from flext_observability.factories import FlextObservabilityMasterFactory
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)
from flext_observability.monitoring import FlextObservabilityMonitor
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)

# Remove unused TYPE_CHECKING - not needed

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Import FlextLogger from flext_core

# Simple API from api module
# No public API classes currently

# Factory patterns from factories module

# Core entities from models module

# Monitor patterns from monitoring module

# Services from services module


# flext_health_status function moved to api.py module


# Legacy facades removed - use direct imports from flext-core and factory classes

__all__: FlextTypes.Core.StringList = [
    # Core entities (actually imported)
    "FlextAlert",
    # Services (actually imported)
    "FlextAlertService",
    # flext-core re-exports (actually imported)
    "FlextConstants",
    "FlextContainer",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLogger",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    # Factory (actually imported)
    "FlextObservabilityMasterFactory",
    # Monitoring (actually imported)
    "FlextObservabilityMonitor",
    "FlextTrace",
    "FlextTracingService",
    "FlextTypes",
    # Version info
    "__version__",
    "__version_info__",
]
