# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability.services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .advanced_context import (
        FlextObservabilityAdvancedContext as FlextObservabilityAdvancedContext,
    )
    from .context import FlextObservabilityContext as FlextObservabilityContext
    from .custom_metrics import (
        FlextObservabilityCustomMetrics as FlextObservabilityCustomMetrics,
    )
    from .error_handling import (
        FlextObservabilityErrorHandling as FlextObservabilityErrorHandling,
    )
    from .health import FlextObservabilityHealth as FlextObservabilityHealth
    from .http_client_instrumentation import (
        FlextObservabilityHTTPClient as FlextObservabilityHTTPClient,
    )
    from .http_instrumentation import FlextObservabilityHTTP as FlextObservabilityHTTP
    from .logging_integration import (
        FlextObservabilityLogging as FlextObservabilityLogging,
    )
    from .monitoring import FlextObservabilityMonitor as FlextObservabilityMonitor
    from .monitoring import flext_monitor_function as flext_monitor_function
    from .performance import (
        FlextObservabilityPerformance as FlextObservabilityPerformance,
    )
    from .sampling import FlextObservabilitySampling as FlextObservabilitySampling
    from .services import FlextObservabilityServices as FlextObservabilityServices

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".advanced_context": ("FlextObservabilityAdvancedContext",),
    ".context": ("FlextObservabilityContext",),
    ".custom_metrics": ("FlextObservabilityCustomMetrics",),
    ".error_handling": ("FlextObservabilityErrorHandling",),
    ".health": ("FlextObservabilityHealth",),
    ".http_client_instrumentation": ("FlextObservabilityHTTPClient",),
    ".http_instrumentation": ("FlextObservabilityHTTP",),
    ".logging_integration": ("FlextObservabilityLogging",),
    ".monitoring": ("FlextObservabilityMonitor", "flext_monitor_function"),
    ".performance": ("FlextObservabilityPerformance",),
    ".sampling": ("FlextObservabilitySampling",),
    ".services": ("FlextObservabilityServices",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilitySampling",
    "FlextObservabilityServices",
    "flext_monitor_function",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
