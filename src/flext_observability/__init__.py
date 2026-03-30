# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

from flext_observability.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_observability import (
        advanced_context,
        constants,
        context,
        core,
        custom_metrics,
        error_handling,
        fields,
        health,
        http_client_instrumentation,
        http_instrumentation,
        logging_integration,
        models,
        monitoring,
        observability_logging,
        performance,
        protocols,
        sampling,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_observability._utilities._advanced_context import (
        FlextObservabilityAdvancedContext,
    )
    from flext_observability._utilities._context import FlextObservabilityContext
    from flext_observability._utilities._custom_metrics import (
        FlextObservabilityCustomMetrics,
    )
    from flext_observability._utilities._error_handling import (
        FlextObservabilityErrorHandling,
    )
    from flext_observability._utilities._fields import FlextObservabilityFields
    from flext_observability._utilities._health import FlextObservabilityHealth
    from flext_observability._utilities._http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )
    from flext_observability._utilities._http_instrumentation import (
        FlextObservabilityHTTP,
    )
    from flext_observability._utilities._logging_integration import (
        FlextObservabilityLogging,
    )
    from flext_observability._utilities._performance import (
        FlextObservabilityPerformance,
    )
    from flext_observability._utilities._sampling import FlextObservabilitySampling
    from flext_observability._utilities._services import FlextObservabilityServices
    from flext_observability.constants import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )
    from flext_observability.core import (
        FlextObservability,
        FlextObservabilityMasterFactory,
    )
    from flext_observability.models import (
        FlextObservabilityModels,
        FlextObservabilityModels as m,
    )
    from flext_observability.monitoring import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )
    from flext_observability.protocols import (
        FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )
    from flext_observability.settings import FlextObservabilitySettings
    from flext_observability.typings import (
        FlextObservabilityTypes,
        FlextObservabilityTypes as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities,
        FlextObservabilityUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextObservability": ["flext_observability.core", "FlextObservability"],
    "FlextObservabilityAdvancedContext": [
        "flext_observability._utilities._advanced_context",
        "FlextObservabilityAdvancedContext",
    ],
    "FlextObservabilityConstants": [
        "flext_observability.constants",
        "FlextObservabilityConstants",
    ],
    "FlextObservabilityContext": [
        "flext_observability._utilities._context",
        "FlextObservabilityContext",
    ],
    "FlextObservabilityCustomMetrics": [
        "flext_observability._utilities._custom_metrics",
        "FlextObservabilityCustomMetrics",
    ],
    "FlextObservabilityErrorHandling": [
        "flext_observability._utilities._error_handling",
        "FlextObservabilityErrorHandling",
    ],
    "FlextObservabilityFields": [
        "flext_observability._utilities._fields",
        "FlextObservabilityFields",
    ],
    "FlextObservabilityHTTP": [
        "flext_observability._utilities._http_instrumentation",
        "FlextObservabilityHTTP",
    ],
    "FlextObservabilityHTTPClient": [
        "flext_observability._utilities._http_client_instrumentation",
        "FlextObservabilityHTTPClient",
    ],
    "FlextObservabilityHealth": [
        "flext_observability._utilities._health",
        "FlextObservabilityHealth",
    ],
    "FlextObservabilityLogging": [
        "flext_observability._utilities._logging_integration",
        "FlextObservabilityLogging",
    ],
    "FlextObservabilityMasterFactory": [
        "flext_observability.core",
        "FlextObservabilityMasterFactory",
    ],
    "FlextObservabilityModels": [
        "flext_observability.models",
        "FlextObservabilityModels",
    ],
    "FlextObservabilityMonitor": [
        "flext_observability.monitoring",
        "FlextObservabilityMonitor",
    ],
    "FlextObservabilityPerformance": [
        "flext_observability._utilities._performance",
        "FlextObservabilityPerformance",
    ],
    "FlextObservabilityProtocols": [
        "flext_observability.protocols",
        "FlextObservabilityProtocols",
    ],
    "FlextObservabilitySampling": [
        "flext_observability._utilities._sampling",
        "FlextObservabilitySampling",
    ],
    "FlextObservabilityServices": [
        "flext_observability._utilities._services",
        "FlextObservabilityServices",
    ],
    "FlextObservabilitySettings": [
        "flext_observability.settings",
        "FlextObservabilitySettings",
    ],
    "FlextObservabilityTypes": [
        "flext_observability.typings",
        "FlextObservabilityTypes",
    ],
    "FlextObservabilityUtilities": [
        "flext_observability.utilities",
        "FlextObservabilityUtilities",
    ],
    "advanced_context": ["flext_observability.advanced_context", ""],
    "c": ["flext_observability.constants", "FlextObservabilityConstants"],
    "constants": ["flext_observability.constants", ""],
    "context": ["flext_observability.context", ""],
    "core": ["flext_observability.core", ""],
    "custom_metrics": ["flext_observability.custom_metrics", ""],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "error_handling": ["flext_observability.error_handling", ""],
    "fields": ["flext_observability.fields", ""],
    "flext_monitor_function": [
        "flext_observability.monitoring",
        "flext_monitor_function",
    ],
    "h": ["flext_core", "h"],
    "health": ["flext_observability.health", ""],
    "http_client_instrumentation": [
        "flext_observability.http_client_instrumentation",
        "",
    ],
    "http_instrumentation": ["flext_observability.http_instrumentation", ""],
    "logging_integration": ["flext_observability.logging_integration", ""],
    "m": ["flext_observability.models", "FlextObservabilityModels"],
    "models": ["flext_observability.models", ""],
    "monitoring": ["flext_observability.monitoring", ""],
    "observability_logging": ["flext_observability.observability_logging", ""],
    "p": ["flext_observability.protocols", "FlextObservabilityProtocols"],
    "performance": ["flext_observability.performance", ""],
    "protocols": ["flext_observability.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "sampling": ["flext_observability.sampling", ""],
    "services": ["flext_observability.services", ""],
    "settings": ["flext_observability.settings", ""],
    "t": ["flext_observability.typings", "FlextObservabilityTypes"],
    "typings": ["flext_observability.typings", ""],
    "u": ["flext_observability.utilities", "FlextObservabilityUtilities"],
    "utilities": ["flext_observability.utilities", ""],
    "x": ["flext_core", "x"],
}

__all__ = [
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
    "FlextObservabilityServices",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "advanced_context",
    "c",
    "constants",
    "context",
    "core",
    "custom_metrics",
    "d",
    "e",
    "error_handling",
    "fields",
    "flext_monitor_function",
    "h",
    "health",
    "http_client_instrumentation",
    "http_instrumentation",
    "logging_integration",
    "m",
    "models",
    "monitoring",
    "observability_logging",
    "p",
    "performance",
    "protocols",
    "r",
    "s",
    "sampling",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
