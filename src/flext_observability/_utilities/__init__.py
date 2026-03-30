# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Observability Utilities subpackage.

Internal implementation modules for observability domain utilities.
All classes are re-exported via the top-level facade.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_observability._utilities._advanced_context import *
    from flext_observability._utilities._context import *
    from flext_observability._utilities._core import *
    from flext_observability._utilities._custom_metrics import *
    from flext_observability._utilities._error_handling import *
    from flext_observability._utilities._fields import *
    from flext_observability._utilities._health import *
    from flext_observability._utilities._http_client_instrumentation import *
    from flext_observability._utilities._http_instrumentation import *
    from flext_observability._utilities._logging_integration import *
    from flext_observability._utilities._monitoring import *
    from flext_observability._utilities._performance import *
    from flext_observability._utilities._sampling import *
    from flext_observability._utilities._services import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextObservability": "flext_observability._utilities._core",
    "FlextObservabilityAdvancedContext": "flext_observability._utilities._advanced_context",
    "FlextObservabilityContext": "flext_observability._utilities._context",
    "FlextObservabilityCustomMetrics": "flext_observability._utilities._custom_metrics",
    "FlextObservabilityErrorHandling": "flext_observability._utilities._error_handling",
    "FlextObservabilityFields": "flext_observability._utilities._fields",
    "FlextObservabilityHTTP": "flext_observability._utilities._http_instrumentation",
    "FlextObservabilityHTTPClient": "flext_observability._utilities._http_client_instrumentation",
    "FlextObservabilityHealth": "flext_observability._utilities._health",
    "FlextObservabilityLogging": "flext_observability._utilities._logging_integration",
    "FlextObservabilityMasterFactory": "flext_observability._utilities._core",
    "FlextObservabilityMonitor": "flext_observability._utilities._monitoring",
    "FlextObservabilityPerformance": "flext_observability._utilities._performance",
    "FlextObservabilitySampling": "flext_observability._utilities._sampling",
    "FlextObservabilityServices": "flext_observability._utilities._services",
    "_advanced_context": "flext_observability._utilities._advanced_context",
    "_context": "flext_observability._utilities._context",
    "_core": "flext_observability._utilities._core",
    "_custom_metrics": "flext_observability._utilities._custom_metrics",
    "_error_handling": "flext_observability._utilities._error_handling",
    "_fields": "flext_observability._utilities._fields",
    "_health": "flext_observability._utilities._health",
    "_http_client_instrumentation": "flext_observability._utilities._http_client_instrumentation",
    "_http_instrumentation": "flext_observability._utilities._http_instrumentation",
    "_logging_integration": "flext_observability._utilities._logging_integration",
    "_monitoring": "flext_observability._utilities._monitoring",
    "_performance": "flext_observability._utilities._performance",
    "_sampling": "flext_observability._utilities._sampling",
    "_services": "flext_observability._utilities._services",
    "flext_monitor_function": "flext_observability._utilities._monitoring",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
