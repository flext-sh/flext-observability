"""Enterprise observability and monitoring library for FLEXT ecosystem.

FLEXT Observability provides unified observability patterns for monitoring, metrics,
tracing, and alerting across the FLEXT ecosystem using FlextResult railway pattern.

Architecture:
- Single FlextObservability class (domain library pattern)
- Nested domain entities (Metric, Trace, Alert, HealthCheck, LogEntry)
- Nested application services (MetricsService, TracingService, etc.)
- Clean Architecture layers with SOLID principles
- Railway-oriented programming with FlextResult[T]

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import (
        FlextDecorators as d,
        FlextExceptions as e,
        FlextHandlers as h,
        FlextMixins as x,
        FlextResult as r,
        FlextService as s,
    )

    from flext_observability.__version__ import __version__, __version_info__
    from flext_observability._core import (
        FlextObservability,
        FlextObservabilityMasterFactory,
        flext_alert,
        flext_health_check,
        flext_log_entry,
        flext_metric,
        flext_trace,
        get_global_factory,
        reset_global_factory,
    )
    from flext_observability.advanced_context import FlextObservabilityAdvancedContext
    from flext_observability.constants import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )
    from flext_observability.context import FlextObservabilityContext
    from flext_observability.custom_metrics import (
        CustomMetricDefinition,
        FlextObservabilityCustomMetrics,
    )
    from flext_observability.error_handling import (
        ErrorEvent,
        FlextObservabilityErrorHandling,
    )
    from flext_observability.fields import FlextObservabilityFields
    from flext_observability.health import FlextObservabilityHealth
    from flext_observability.http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )
    from flext_observability.http_instrumentation import FlextObservabilityHTTP
    from flext_observability.logging_integration import FlextObservabilityLogging
    from flext_observability.models import (
        FlextObservabilityModels,
        FlextObservabilityModels as m,
    )
    from flext_observability.monitoring import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )
    from flext_observability.performance import FlextObservabilityPerformance
    from flext_observability.protocols import (
        FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )
    from flext_observability.sampling import FlextObservabilitySampling
    from flext_observability.settings import FlextObservabilitySettings
    from flext_observability.typings import (
        FlextObservabilityTypes,
        FlextObservabilityTypes as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities,
        FlextObservabilityUtilities as u,
    )
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "CustomMetricDefinition": (
        "flext_observability.custom_metrics",
        "CustomMetricDefinition",
    ),
    "ErrorEvent": ("flext_observability.error_handling", "ErrorEvent"),
    "FlextObservability": ("flext_observability._core", "FlextObservability"),
    "FlextObservabilityAdvancedContext": (
        "flext_observability.advanced_context",
        "FlextObservabilityAdvancedContext",
    ),
    "FlextObservabilityConstants": (
        "flext_observability.constants",
        "FlextObservabilityConstants",
    ),
    "FlextObservabilityContext": (
        "flext_observability.context",
        "FlextObservabilityContext",
    ),
    "FlextObservabilityCustomMetrics": (
        "flext_observability.custom_metrics",
        "FlextObservabilityCustomMetrics",
    ),
    "FlextObservabilityErrorHandling": (
        "flext_observability.error_handling",
        "FlextObservabilityErrorHandling",
    ),
    "FlextObservabilityFields": (
        "flext_observability.fields",
        "FlextObservabilityFields",
    ),
    "FlextObservabilityHTTP": (
        "flext_observability.http_instrumentation",
        "FlextObservabilityHTTP",
    ),
    "FlextObservabilityHTTPClient": (
        "flext_observability.http_client_instrumentation",
        "FlextObservabilityHTTPClient",
    ),
    "FlextObservabilityHealth": (
        "flext_observability.health",
        "FlextObservabilityHealth",
    ),
    "FlextObservabilityLogging": (
        "flext_observability.logging_integration",
        "FlextObservabilityLogging",
    ),
    "FlextObservabilityMasterFactory": (
        "flext_observability._core",
        "FlextObservabilityMasterFactory",
    ),
    "FlextObservabilityModels": (
        "flext_observability.models",
        "FlextObservabilityModels",
    ),
    "FlextObservabilityMonitor": (
        "flext_observability.monitoring",
        "FlextObservabilityMonitor",
    ),
    "FlextObservabilityPerformance": (
        "flext_observability.performance",
        "FlextObservabilityPerformance",
    ),
    "FlextObservabilityProtocols": (
        "flext_observability.protocols",
        "FlextObservabilityProtocols",
    ),
    "FlextObservabilitySampling": (
        "flext_observability.sampling",
        "FlextObservabilitySampling",
    ),
    "FlextObservabilitySettings": (
        "flext_observability.settings",
        "FlextObservabilitySettings",
    ),
    "FlextObservabilityTypes": (
        "flext_observability.typings",
        "FlextObservabilityTypes",
    ),
    "FlextObservabilityUtilities": (
        "flext_observability.utilities",
        "FlextObservabilityUtilities",
    ),
    "__version__": ("flext_observability.__version__", "__version__"),
    "__version_info__": ("flext_observability.__version__", "__version_info__"),
    "c": ("flext_observability.constants", "FlextObservabilityConstants"),
    "d": ("flext_core", "FlextDecorators"),
    "e": ("flext_core", "FlextExceptions"),
    "flext_alert": ("flext_observability._core", "flext_alert"),
    "flext_health_check": ("flext_observability._core", "flext_health_check"),
    "flext_log_entry": ("flext_observability._core", "flext_log_entry"),
    "flext_metric": ("flext_observability._core", "flext_metric"),
    "flext_monitor_function": (
        "flext_observability.monitoring",
        "flext_monitor_function",
    ),
    "flext_trace": ("flext_observability._core", "flext_trace"),
    "get_global_factory": ("flext_observability._core", "get_global_factory"),
    "h": ("flext_core", "FlextHandlers"),
    "m": ("flext_observability.models", "FlextObservabilityModels"),
    "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
    "r": ("flext_core", "FlextResult"),
    "reset_global_factory": ("flext_observability._core", "reset_global_factory"),
    "s": ("flext_core", "FlextService"),
    "t": ("flext_observability.typings", "FlextObservabilityTypes"),
    "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
    "x": ("flext_core", "FlextMixins"),
}
__all__ = [
    "CustomMetricDefinition",
    "ErrorEvent",
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityConstants",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityFields",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilityProtocols",
    "FlextObservabilitySampling",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "flext_alert",
    "flext_health_check",
    "flext_log_entry",
    "flext_metric",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "h",
    "m",
    "p",
    "r",
    "reset_global_factory",
    "s",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> Any:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
