"""FLEXT Observability Unified Models.

Provides unified access to all observability domain models through focused,
modular namespace classes. Each domain (metrics, tracing, alerting, health, logging)
has its own dedicated module with proper separation of concerns.

Built on flext-core patterns with comprehensive type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels

# Import focused domain models
from flext_observability.alerting import FlextObservabilityAlerting
from flext_observability.health import FlextObservabilityHealth
from flext_observability.logging import FlextObservabilityLogging
from flext_observability.metrics import FlextObservabilityMetrics
from flext_observability.tracing import FlextObservabilityTracing


class FlextObservabilityModels(FlextModels):
    """Unified observability models facade extending FlextModels.

    Provides consolidated access to all observability domain models through
    focused namespace classes. Each domain (metrics, tracing, alerting, health, logging)
    maintains its own dedicated module with proper separation of concerns.

    This facade ensures backward compatibility while providing clean domain boundaries.
    """

    # Domain-specific namespace classes - each in its own focused module
    Metrics = FlextObservabilityMetrics
    Tracing = FlextObservabilityTracing
    Alerting = FlextObservabilityAlerting
    Health = FlextObservabilityHealth
    Logging = FlextObservabilityLogging

    # Backward compatibility aliases for direct entity access
    FlextMetric = FlextObservabilityMetrics.FlextMetric
    FlextTrace = FlextObservabilityTracing.FlextTrace
    FlextAlert = FlextObservabilityAlerting.FlextAlert
    FlextHealthCheck = FlextObservabilityHealth.FlextHealthCheck
    FlextLogEntry = FlextObservabilityLogging.FlextLogEntry

    # Factory methods for direct entity creation (maintained for compatibility)
    flext_metric = staticmethod(FlextObservabilityMetrics.flext_metric)
    flext_trace = staticmethod(FlextObservabilityTracing.flext_trace)
    flext_alert = staticmethod(FlextObservabilityAlerting.flext_alert)
    flext_health_check = staticmethod(FlextObservabilityHealth.flext_health_check)


# Direct exports for backward compatibility (used by __init__.py)
FlextMetric = FlextObservabilityModels.FlextMetric
FlextTrace = FlextObservabilityModels.FlextTrace
FlextAlert = FlextObservabilityModels.FlextAlert
FlextHealthCheck = FlextObservabilityModels.FlextHealthCheck
FlextLogEntry = FlextObservabilityModels.FlextLogEntry

# Export the unified models class and direct entities
__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextObservabilityModels",
    "FlextTrace",
]
