"""FLEXT Observability - Enterprise Observability Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade observability platform built on flext-core foundation.
Provides unified monitoring, logging, metrics, tracing, and alerting.

Simple usage:
>>> from flext_observability import FlextMetricsService, FlextLogEntry
>>> from flext_observability import create_flext_observability_platform
>>>
>>> # Create unified platform
>>> platform = create_flext_observability_platform()
>>>
>>> # Use modern services
>>> metrics_service = platform.get_metrics_service()
>>> log_entry = FlextLogEntry(message="System started", level="INFO")
>>> result = metrics_service.record_log(log_entry)
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings
from typing import TYPE_CHECKING, Any

# Import from flext-core for foundational patterns (standardized)
from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextCoreSettings as BaseConfig,
    FlextEntity as DomainEntity,
    FlextField as Field,
    FlextResult,
    FlextValueObject as BaseModel,
    FlextValueObject as DomainBaseModel,
    FlextValueObject as DomainValueObject,
)

try:
    __version__ = importlib.metadata.version("flext-observability")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.8.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextObservabilityDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Observability import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT Observability docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextObservabilityDeprecationWarning,
        stacklevel=3,
    )


# Enable deprecation warnings
warnings.filterwarnings("default", category=FlextObservabilityDeprecationWarning)

if TYPE_CHECKING:
    from flext_observability.platform import FlextObservabilityPlatform

# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Application services - simplified imports
with contextlib.suppress(ImportError):
    from flext_observability.application.services import (
        FlextAlertService,
        FlextHealthService,
        FlextLoggingService,
        FlextMetricsService,
        FlextTracingService,
    )

# Core domain entities - simplified imports
with contextlib.suppress(ImportError):
    from flext_observability.domain.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )

# Platform exports - actual implementations only
with contextlib.suppress(ImportError):
    from flext_observability.platform import FlextObservabilityPlatform

# Simple API for common operations - simplified imports
with contextlib.suppress(ImportError):
    from flext_observability.simple_api import (
        create_flext_alert,
        create_flext_health_check,
        create_flext_log_entry,
        create_flext_metric,
        create_flext_trace,
    )


# Platform factory function
def create_flext_observability_platform(
    config: dict[str, object] | None = None,
) -> FlextObservabilityPlatform:
    """Create unified FLEXT Observability platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextObservabilityPlatform instance

    """
    from flext_observability.platform import FlextObservabilityPlatform

    return FlextObservabilityPlatform(config or {})


# FlextObservability-specific aliases (following FlextXxx pattern)
try:
    FlextObservability = FlextObservabilityPlatform  # Main class
except NameError:
    FlextObservability = None

FlextObservabilityResult = FlextResult  # FlextObservability result pattern
FlextObservabilityBaseModel = DomainBaseModel  # FlextObservability base model

# Prefixed helper functions following flext_observability_ pattern
try:
    flext_observability_create_metric = create_flext_metric
    flext_observability_create_log_entry = create_flext_log_entry
    flext_observability_create_trace = create_flext_trace
    flext_observability_create_alert = create_flext_alert
    flext_observability_create_health_check = create_flext_health_check
except NameError:
    flext_observability_create_metric = None
    flext_observability_create_log_entry = None
    flext_observability_create_trace = None
    flext_observability_create_alert = None
    flext_observability_create_health_check = None

flext_observability_create_platform = create_flext_observability_platform

# Backwards compatibility aliases
try:
    Alert = FlextAlert
    AlertService = FlextAlertService
    HealthCheck = FlextHealthCheck
    HealthService = FlextHealthService
    LogEntry = FlextLogEntry
    LoggingService = FlextLoggingService
    Metric = FlextMetric
    MetricsService = FlextMetricsService
    ObservabilityPlatform = FlextObservabilityPlatform
    Trace = FlextTrace
    TracingService = FlextTracingService
except NameError:
    Alert = None
    AlertService = None
    HealthCheck = None
    HealthService = None
    LogEntry = None
    LoggingService = None
    Metric = None
    MetricsService = None
    ObservabilityPlatform = None
    Trace = None
    TracingService = None

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "Alert",  # from flext_observability import Alert
    "AlertService",  # from flext_observability import AlertService (LEGACY)
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🔧 COMPATIBILITY ALIASES
    # ═══════════════════════════════════════════════════════════════════════════════
    "BaseConfig",  # from flext_observability import BaseConfig
    "BaseModel",  # from flext_observability import BaseModel
    "DomainBaseModel",  # from flext_observability import DomainBaseModel
    "DomainEntity",  # from flext_observability import DomainEntity
    "DomainValueObject",  # from flext_observability import DomainValueObject
    "Field",  # from flext_observability import Field
    "FlextAlert",  # from flext_observability import FlextAlert
    "FlextAlertService",  # from flext_observability import FlextAlertService
    "FlextConstants",  # from flext_observability import FlextConstants
    # ═══════════════════════════════════════════════════════════════════════════════
    # ✅ CORE FLEXT PATTERNS - RECOMMENDED IMPORTS
    # ═══════════════════════════════════════════════════════════════════════════════
    "FlextContainer",  # from flext_observability import FlextContainer
    "FlextHealthCheck",  # from flext_observability import FlextHealthCheck
    "FlextHealthService",  # from flext_observability import FlextHealthService
    "FlextLogEntry",  # from flext_observability import FlextLogEntry
    "FlextLoggingService",  # from flext_observability import FlextLoggingService
    # ═══════════════════════════════════════════════════════════════════════════════
    # 👤 DOMAIN ENTITIES - MODERN FLEXT STANDARD
    # ═══════════════════════════════════════════════════════════════════════════════
    "FlextMetric",  # from flext_observability import FlextMetric
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🏢 PLATFORM & SERVICES - UNIFIED ACCESS
    # ═══════════════════════════════════════════════════════════════════════════════
    "FlextMetricsService",  # from flext_observability import FlextMetricsService
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🏢 FLEXT OBSERVABILITY SPECIFIC PATTERNS
    # ═══════════════════════════════════════════════════════════════════════════════
    "FlextObservability",  # Main class
    "FlextObservabilityBaseModel",  # from flext_observability import FlextObservabilityBaseModel
    "FlextObservabilityResult",  # from flext_observability import FlextObservabilityResult
    "FlextResult",  # from flext_observability import FlextResult
    "FlextTrace",  # from flext_observability import FlextTrace
    "FlextTracingService",  # from flext_observability import FlextTracingService
    "HealthCheck",  # from flext_observability import HealthCheck
    "HealthService",  # from flext_observability import HealthService (LEGACY)
    "LogEntry",  # from flext_observability import LogEntry
    "LoggingService",  # from flext_observability import LoggingService (LEGACY)
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🔧 DOMAIN ENTITIES - LEGACY COMPATIBILITY
    # ═══════════════════════════════════════════════════════════════════════════════
    "Metric",  # from flext_observability import Metric
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🚨 LEGACY COMPATIBILITY - Will be deprecated
    # ═══════════════════════════════════════════════════════════════════════════════
    "MetricsService",  # from flext_observability import MetricsService (LEGACY)
    "ObservabilityPlatform",  # from flext_observability import ObservabilityPlatform (LEGACY)
    "Trace",  # from flext_observability import Trace
    "TracingService",  # from flext_observability import TracingService (LEGACY)
    # ═══════════════════════════════════════════════════════════════════════════════
    # 📦 METADATA
    # ═══════════════════════════════════════════════════════════════════════════════
    "__version__",  # Package version
    "__version_info__",  # Version info tuple
    "create_flext_alert",  # from flext_observability import create_flext_alert
    "create_flext_health_check",  # from flext_observability import create_flext_health_check
    "create_flext_log_entry",  # from flext_observability import create_flext_log_entry
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🛠️ SIMPLE API - MODERN FLEXT STANDARD
    # ═══════════════════════════════════════════════════════════════════════════════
    "create_flext_metric",  # from flext_observability import create_flext_metric
    "create_flext_observability_platform",  # from flext_observability import create_flext_observability_platform
    "create_flext_trace",  # from flext_observability import create_flext_trace
    "flext_observability_create_alert",  # from flext_observability import flext_observability_create_alert
    "flext_observability_create_health_check",  # from flext_observability import flext_observability_create_health_check
    "flext_observability_create_log_entry",  # from flext_observability import flext_observability_create_log_entry
    # ═══════════════════════════════════════════════════════════════════════════════
    # 🔄 PREFIXED HELPER FUNCTIONS - FLEXT STANDARD
    # ═══════════════════════════════════════════════════════════════════════════════
    "flext_observability_create_metric",  # from flext_observability import flext_observability_create_metric
    "flext_observability_create_platform",  # from flext_observability import flext_observability_create_platform
    "flext_observability_create_trace",  # from flext_observability import flext_observability_create_trace
]


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 📦 DYNAMIC IMPORT HANDLER - Legacy path resolution                        │
# └─────────────────────────────────────────────────────────────────────────────┘
def __getattr__(name: str) -> Any:
    """Handle legacy imports with automatic deprecation warnings and guidance."""
    # Legacy import mapping with migration paths
    legacy_mapping = {
        # Application services
        "ObservabilityService": ("application.services", "FlextMetricsService"),
        "MonitoringService": ("application.services", "FlextMetricsService"),
        # Infrastructure components
        "ObservabilityClient": ("platform", "FlextObservabilityPlatform"),
        "MetricsCollector": ("platform", "FlextObservabilityPlatform"),
        # Configuration and utilities
        "ObservabilityValidator": ("platform", "FlextObservabilityPlatform"),
        # Legacy aliases
        "ObservabilityConfig": ("config", "FlextObservabilityConfig"),
    }

    if name in legacy_mapping:
        old_module, new_import = legacy_mapping[name]

        _show_deprecation_warning(f"flext_observability.{old_module}.{name}", new_import)

        # NO FALLBACKS - SEMPRE usar implementações originais conforme instrução
        # Import from legacy location directly without fallback
        try:
            module = __import__(f"flext_observability.{old_module}", fromlist=[name])
            return getattr(module, name)
        except (ImportError, AttributeError):
            # Return the new recommended class instead
            if new_import == "FlextMetricsService":
                return FlextMetricsService
            if new_import == "FlextObservabilityPlatform":
                return create_flext_observability_platform()

    # If completely unknown attribute
    msg = (
        f"\\n❌ module 'flext_observability' has no attribute '{name}'\\n"
        f"✅ Available imports: {', '.join(sorted(__all__[:10]))}...\\n"
        f"📖 See: https://docs.flext.dev/flext-observability/api\\n"
    )
    raise AttributeError(msg)


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 📋 MODULE METADATA AND UTILITIES                                          │
# └─────────────────────────────────────────────────────────────────────────────┘

__architecture__ = "Clean Architecture + DDD"
__migration_guide__ = "https://docs.flext.dev/migration/observability"
