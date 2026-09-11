# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability.services package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .advanced_context import FlextObservabilityAdvancedContext
    from .context import FlextObservabilityContext
    from .custom_metrics import FlextObservabilityCustomMetrics
    from .error_handling import FlextObservabilityErrorHandling
    from .health import FlextObservabilityHealth
    from .http_client_instrumentation import FlextObservabilityHTTPClient
    from .http_instrumentation import FlextObservabilityHTTP
    from .logging_integration import FlextObservabilityLogging
    from .monitoring import FlextObservabilityMonitor, flext_monitor_function
    from .performance import FlextObservabilityPerformance
    from .sampling import FlextObservabilitySampling
    from .services import FlextObservabilityServices
__all__: tuple[str, ...] = (
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
