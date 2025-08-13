"""FLEXT Observability - Production-Grade Foundation Library.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Production-grade observability library implementing docs/patterns/ foundation
with SOLID principles, zero redundancy, and complete flext-core alignment.
Provides minimal but comprehensive observability capabilities with legacy
compatibility facades for ecosystem migration.

Public API (docs/patterns/ aligned):
    Core Entities: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck, FlextLogEntry
    Factory Pattern: FlextObservabilityMasterFactory (centralized entity creation)
    Application Services: FlextMetricsService, FlextTracingService, etc.
    Simple API: Convenience functions (flext_create_*)
    Monitoring: @flext_monitor_function decorator

Architecture (Clean Architecture + SOLID):
    Domain Layer: entities.py (business entities with validate_business_rules)
    Application Layer: services.py (business logic coordination)
    Interface Adapters: factory.py (creation patterns)
    Infrastructure: flext_simple.py, flext_monitor.py (utilities)

Integration:
    100% flext-core foundation patterns, FlextTypes.Data.Dict,
    FlextResult railway-oriented programming, zero local duplication.

Version: 0.9.0
"""

from __future__ import annotations

import warnings

# Remove unused TYPE_CHECKING - not needed

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Import get_logger from flext_core
from flext_core import FlextContainer, get_logger
from flext_core.constants import FlextConstants

# Core entities (minimal, no redundancy) - Updated imports to use consolidated files
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_trace,
)

# Factory patterns (centralized entity creation) - Updated imports to use consolidated files
from flext_observability.observability_factory import (
    FlextObservabilityMasterFactory,
    alert,
    get_global_factory,
    health_check,
    log,
    metric,
    reset_global_factory,
    trace,
)

# Monitor patterns (automation) - Updated imports to use consolidated files
from flext_observability.observability_monitor import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Simple API (convenience) - Updated imports to use consolidated files
from flext_observability.observability_api import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

# Services (application layer) - Updated imports to use consolidated files
from flext_observability.observability_services import (
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


# =============================================================================
# LEGACY COMPATIBILITY FACADES - DEPRECATED INTERFACES
# =============================================================================


def _deprecated_warning(old_name: str, new_name: str) -> None:
    """Issue deprecation warning for legacy interfaces."""
    warnings.warn(
        f"{old_name} is deprecated. Use {new_name} instead. "
        f"Will be removed in v1.0.0. See docs/patterns/ for migration guide.",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy aliases with deprecation warnings
def create_observability_platform(
    container: object | None = None,
) -> FlextObservabilityMasterFactory:
    """Create master factory (deprecated; use FlextObservabilityMasterFactory)."""
    _deprecated_warning(
        "create_observability_platform", "FlextObservabilityMasterFactory",
    )
    container_typed = container if isinstance(container, FlextContainer) else None
    return FlextObservabilityMasterFactory(container_typed)


def observability_platform(
    container: object | None = None,
) -> FlextObservabilityMasterFactory:
    """Return master factory (deprecated; prefer FlextObservabilityMasterFactory)."""
    _deprecated_warning("observability_platform", "FlextObservabilityMasterFactory")
    container_typed = container if isinstance(container, FlextContainer) else None
    return FlextObservabilityMasterFactory(container_typed)


# Legacy constant facades
class _LegacyConstants:
    """DEPRECATED: Use flext_core.constants.FlextConstants instead."""

    def __getattr__(self, name: str) -> object:
        _deprecated_warning(f"constants.{name}", "flext_core.constants.FlextConstants")
        return getattr(FlextConstants, name, "UNKNOWN")


constants = _LegacyConstants()

__all__: list[str] = [
    "FlextAlert",
    "FlextAlertService",
    "FlextContainer",
    "FlextConstants",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityMonitor",
    "FlextTrace",
    "FlextTracingService",
    "__version__",
    "__version_info__",
    "alert",
    "annotations",
    "constants",
    "create_observability_platform",
    "flext_alert",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    "flext_health_status",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "get_logger",
    "health_check",
    "log",
    "metric",
    "observability_platform",
    "reset_global_factory",
    "trace",
]
