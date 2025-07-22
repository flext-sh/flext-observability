"""FLEXT Observability - Enterprise monitoring with simplified imports.

🎯 SIMPLE IMPORTS - Use these for ALL new code:

# Core entities (short paths)
from flext_observability import Metric, Trace, LogEntry, Alert, HealthCheck

# Services (direct access)
from flext_observability import MetricsService, TracingService, LoggingService

# Essential functions (no path complexity)
from flext_observability import get_logger, setup_logging, configure_observability

# Protocols and abstractions
from flext_observability import MetricCollector, TraceExporter, LogAggregator

🚨 DEPRECATED LONG PATHS (still work, but discouraged):
❌ from flext_observability.infrastructure.logging.structured import get_logger
✅ from flext_observability import get_logger

❌ from flext_observability.application.services.metrics import MetricsService
✅ from flext_observability import MetricsService

❌ from flext_observability.domain.entities.metric import Metric
✅ from flext_observability import Metric

🔄 MIGRATION STRATEGY:
All complex paths show warnings pointing to simple root-level imports.
Use short, direct imports for maximum productivity and clarity.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

# Import types from flext-core using correct simplified imports (no fallbacks)
from flext_core import (
    AlertSeverity,
    LogLevel,
    MetricType,
    ServiceResult,
    TraceStatus,
)

# Essential imports for compatibility with existing code
from flext_observability._compatibility import LoggingConfig
from flext_observability._deprecated import (
    FlextObservabilityDeprecationWarning,
    create_compatibility_function,
    create_compatibility_wrapper,
    warn_deprecated_import,
    warn_deprecated_path,
)

# Import services directly - NO FALLBACKS (refactor real implementation instead)
from flext_observability.application import (
    AlertService,
    HealthService,
    LoggingService,
    MetricsService,
    TracingService,
)

# Configuration functions with simple access
from flext_observability.configuration import (
    ObservabilitySettings,
    configure_observability,
    create_development_config,
    create_production_config,
    create_testing_config,
    get_settings,
)
from flext_observability.domain.entities import (
    Alert,  # Alerting
    HealthCheck,  # Health
    LogEntry,  # Logging
    Metric,  # Metrics
    Trace,  # Tracing
)
from flext_observability.domain.value_objects import (
    ComponentName,  # Component identification
    Duration,  # Values
    MetricValue,
    ThresholdValue,
    TraceId,
)

# Import protocols directly - NO FALLBACKS (foundation must be implemented)
from flext_observability.foundation import (
    AlertManagerProtocol,
    LogAggregatorProtocol,
    MetricCollectorProtocol,
    ObservabilityProtocol,
    TraceExporterProtocol,
)

# Legacy health status - NO FALLBACKS, use real implementation
from flext_observability.health import (
    ComponentHealth,
    HealthChecker,
    HealthStatus,
)
from flext_observability.infrastructure.logging import (
    bind_context,
    clear_context,
    get_logger,
    setup_logging,
    with_context,
)

if TYPE_CHECKING:
    from typing import Any

# Enable deprecation warnings to be shown
warnings.filterwarnings("default", category=FlextObservabilityDeprecationWarning)

__version__ = "0.7.0"

# Also expose without Protocol suffix for simple access
AlertManager = AlertManagerProtocol
MetricCollector = MetricCollectorProtocol
TraceExporter = TraceExporterProtocol
LogAggregator = LogAggregatorProtocol


# ═══════════════════════════════════════════════════════════════════════════════
# ⚠️ DEPRECATED COMPATIBILITY LAYER - Will show warnings
# ═══════════════════════════════════════════════════════════════════════════════

# Legacy business metrics - DEPRECATED, use domain.metrics instead
def business_metric(*args: Any, **kwargs: Any) -> Any:
    """Deprecated: Use Metric instead."""
    warn_deprecated_path(
        "BusinessMetric",
        "Use: from flext_observability import Metric instead",
    )
    return Metric


def business_metric_type(*args: Any, **kwargs: Any) -> Any:
    """Deprecated: Use MetricType instead."""
    warn_deprecated_path(
        "BusinessMetricType",
        "Use: from flext_observability import MetricType instead",
    )
    return MetricType


def enterprise_business_metrics(*args: Any, **kwargs: Any) -> Any:
    """Deprecated: Use MetricsService instead."""
    warn_deprecated_path(
        "EnterpriseBusinessMetrics",
        "Use: from flext_observability import MetricsService instead",
    )
    return MetricsService


# Expose legacy names for backward compatibility
BusinessMetric = business_metric
BusinessMetricType = business_metric_type
EnterpriseBusinessMetrics = enterprise_business_metrics


# ════════════════════════════════════════════════════════════════════════════════════════════════════════════
# 📋 SIMPLIFIED PUBLIC API - All exports available at root level
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════

__all__ = [
    "Alert",                     # from flext_observability import Alert
    "AlertManager",       # from flext_observability import AlertManager
    "AlertManagerProtocol",
    "AlertService",                               # from flext_observability import AlertService
    "AlertSeverity",
    # ⚠️ LEGACY COMPATIBILITY (will show warnings)
    "BusinessMetric",  # Use Metric instead
    "BusinessMetricType",
    "ComponentHealth",          # from flext_observability import ComponentHealth
    "ComponentName",             # from flext_observability import ComponentName
    "Duration",                 # from flext_observability import Duration
    "EnterpriseBusinessMetrics",
    "FlextObservabilityDeprecationWarning",       # For custom warnings
    "HealthCheck",             # from flext_observability import HealthCheck
    "HealthChecker",            # from flext_observability import HealthChecker
    "HealthService",                              # from flext_observability import HealthService
    "HealthStatus",              # Legacy health types
    "LogAggregator",     # from flext_observability import LogAggregator
    "LogAggregatorProtocol",
    "LogEntry",                       # from flext_observability import LogEntry
    "LogLevel",
    "LoggingConfig",                              # from flext_observability import LoggingConfig
    "LoggingService",                             # from flext_observability import LoggingService
    # 🎯 CORE ENTITIES (simple direct imports)
    "Metric",       # from flext_observability import Metric
    # 🔌 PROTOCOLS (simple interface access)
    "MetricCollector",  # from flext_observability import MetricCollector
    "MetricCollectorProtocol",
    "MetricType",
    "MetricValue",
    # 🔧 SERVICES (direct access without paths)
    "MetricsService",                             # from flext_observability import MetricsService
    "ObservabilityProtocol",                      # from flext_observability import ObservabilityProtocol
    # ⚙️ CONFIGURATION (simple access)
    "ObservabilitySettings",                      # from flext_observability import ObservabilitySettings
    "ThresholdValue",
    "Trace",           # from flext_observability import Trace
    "TraceExporter",     # from flext_observability import TraceExporter
    "TraceExporterProtocol",
    "TraceId",
    "TraceStatus",
    "TracingService",                             # from flext_observability import TracingService
    # 📦 META
    "__version__",                                # Package version
    "bind_context",  # Context management
    "clear_context",
    "configure_observability",                    # from flext_observability import configure_observability
    "create_development_config",                  # from flext_observability import create_development_config
    "create_production_config",                   # from flext_observability import create_production_config
    "create_testing_config",                      # from flext_observability import create_testing_config
    # 🚀 ESSENTIAL FUNCTIONS (no complex paths)
    "get_logger",                                 # from flext_observability import get_logger
    "get_settings",                               # from flext_observability import get_settings
    "setup_logging",                              # from flext_observability import setup_logging
    "with_context",
]
