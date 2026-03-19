# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Enterprise observability and monitoring library for FLEXT ecosystem.

FLEXT Observability provides unified observability patterns for monitoring, metrics,
tracing, and alerting across the FLEXT ecosystem using r railway pattern.

Architecture:
- Single FlextObservability class (domain library pattern)
- Nested domain entities (Metric, Trace, Alert, HealthCheck, LogEntry)
- Nested application services (MetricsService, TracingService, etc.)
- Clean Architecture layers with SOLID principles
- Railway-oriented programming with r[T]

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

from flext_observability.typings import T

if TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_core.typings import FlextTypes

    from flext_observability.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_observability.advanced_context import (
        ContextSnapshot,
        FlextObservabilityAdvancedContext,
    )
    from flext_observability.constants import FlextObservabilityConstants, c
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
    from flext_observability.models import FlextObservabilityModels, m
    from flext_observability.monitoring import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )
    from flext_observability.performance import (
        FlextObservabilityPerformance,
        PerformanceMetrics,
    )
    from flext_observability.protocols import FlextObservabilityProtocols, p
    from flext_observability.sampling import FlextObservabilitySampling
    from flext_observability.services import (
        FlextObservabilityServices,
        get_global_factory,
        reset_global_factory,
    )
    from flext_observability.settings import FlextObservabilitySettings
    from flext_observability.typings import FlextObservabilityTypes, t
    from flext_observability.utilities import FlextObservabilityUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "ContextSnapshot": ("flext_observability.advanced_context", "ContextSnapshot"),
    "CustomMetricDefinition": (
        "flext_observability.custom_metrics",
        "CustomMetricDefinition",
    ),
    "ErrorEvent": ("flext_observability.error_handling", "ErrorEvent"),
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
    "FlextObservabilityServices": (
        "flext_observability.services",
        "FlextObservabilityServices",
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
    "PerformanceMetrics": ("flext_observability.performance", "PerformanceMetrics"),
    "__all__": ("flext_observability.__version__", "__all__"),
    "__author__": ("flext_observability.__version__", "__author__"),
    "__author_email__": ("flext_observability.__version__", "__author_email__"),
    "__description__": ("flext_observability.__version__", "__description__"),
    "__license__": ("flext_observability.__version__", "__license__"),
    "__title__": ("flext_observability.__version__", "__title__"),
    "__url__": ("flext_observability.__version__", "__url__"),
    "__version__": ("flext_observability.__version__", "__version__"),
    "__version_info__": ("flext_observability.__version__", "__version_info__"),
    "c": ("flext_observability.constants", "c"),
    "d": ("flext_core.decorators", "d"),
    "e": ("flext_core.exceptions", "e"),
    "flext_monitor_function": (
        "flext_observability.monitoring",
        "flext_monitor_function",
    ),
    "get_global_factory": ("flext_observability.services", "get_global_factory"),
    "h": ("flext_core.handlers", "h"),
    "m": ("flext_observability.models", "m"),
    "p": ("flext_observability.protocols", "p"),
    "r": ("flext_core.result", "r"),
    "reset_global_factory": ("flext_observability.services", "reset_global_factory"),
    "s": ("flext_core.service", "s"),
    "t": ("flext_observability.typings", "t"),
    "u": ("flext_observability.utilities", "u"),
    "x": ("flext_core.mixins", "x"),
}

__all__ = [
    "ContextSnapshot",
    "CustomMetricDefinition",
    "ErrorEvent",
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
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilityProtocols",
    "FlextObservabilitySampling",
    "FlextObservabilityServices",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "PerformanceMetrics",
    "T",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "flext_monitor_function",
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


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
