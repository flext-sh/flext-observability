# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Observability service mixins for MRO composition."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_observability.services.advanced_context import *
    from flext_observability.services.context import *
    from flext_observability.services.custom_metrics import *
    from flext_observability.services.error_handling import *
    from flext_observability.services.fields import *
    from flext_observability.services.health import *
    from flext_observability.services.http_client_instrumentation import *
    from flext_observability.services.http_instrumentation import *
    from flext_observability.services.logging_integration import *
    from flext_observability.services.monitoring import *
    from flext_observability.services.performance import *
    from flext_observability.services.sampling import *
    from flext_observability.services.services import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextObservabilityAdvancedContext": "flext_observability.services.advanced_context",
    "FlextObservabilityContext": "flext_observability.services.context",
    "FlextObservabilityCustomMetrics": "flext_observability.services.custom_metrics",
    "FlextObservabilityErrorHandling": "flext_observability.services.error_handling",
    "FlextObservabilityFields": "flext_observability.services.fields",
    "FlextObservabilityHTTP": "flext_observability.services.http_instrumentation",
    "FlextObservabilityHTTPClient": "flext_observability.services.http_client_instrumentation",
    "FlextObservabilityHealth": "flext_observability.services.health",
    "FlextObservabilityLogging": "flext_observability.services.logging_integration",
    "FlextObservabilityMonitor": "flext_observability.services.monitoring",
    "FlextObservabilityPerformance": "flext_observability.services.performance",
    "FlextObservabilitySampling": "flext_observability.services.sampling",
    "FlextObservabilityServices": "flext_observability.services.services",
    "advanced_context": "flext_observability.services.advanced_context",
    "context": "flext_observability.services.context",
    "custom_metrics": "flext_observability.services.custom_metrics",
    "error_handling": "flext_observability.services.error_handling",
    "fields": "flext_observability.services.fields",
    "flext_monitor_function": "flext_observability.services.monitoring",
    "health": "flext_observability.services.health",
    "http_client_instrumentation": "flext_observability.services.http_client_instrumentation",
    "http_instrumentation": "flext_observability.services.http_instrumentation",
    "logging_integration": "flext_observability.services.logging_integration",
    "monitoring": "flext_observability.services.monitoring",
    "performance": "flext_observability.services.performance",
    "sampling": "flext_observability.services.sampling",
    "services": "flext_observability.services.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
