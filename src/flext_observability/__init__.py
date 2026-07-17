# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
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
    from flext_cli import d, e, h, r, s, x

    from ._config import FlextObservabilityConfig, config
    from ._settings import FlextObservabilitySettings, settings
    from .api import FlextObservability, observability
    from .constants import FlextObservabilityConstants, FlextObservabilityConstants as c
    from .models import FlextObservabilityModels, FlextObservabilityModels as m
    from .protocols import FlextObservabilityProtocols, FlextObservabilityProtocols as p
    from .services.advanced_context import FlextObservabilityAdvancedContext
    from .services.context import FlextObservabilityContext
    from .services.custom_metrics import FlextObservabilityCustomMetrics
    from .services.error_handling import FlextObservabilityErrorHandling
    from .services.health import FlextObservabilityHealth
    from .services.http_client_instrumentation import FlextObservabilityHTTPClient
    from .services.http_instrumentation import FlextObservabilityHTTP
    from .services.logging_integration import FlextObservabilityLogging
    from .services.monitoring import FlextObservabilityMonitor
    from .services.performance import FlextObservabilityPerformance
    from .services.sampling import FlextObservabilitySampling
    from .services.services import FlextObservabilityServices
    from .typings import FlextObservabilityTypes, FlextObservabilityTypes as t
    from .utilities import FlextObservabilityUtilities, FlextObservabilityUtilities as u

    _ = (
        c,
        FlextObservabilityConstants,
        t,
        FlextObservabilityTypes,
        p,
        FlextObservabilityProtocols,
        m,
        FlextObservabilityModels,
        u,
        FlextObservabilityUtilities,
        d,
        e,
        h,
        r,
        s,
        x,
        FlextObservabilitySettings,
        settings,
        FlextObservability,
        observability,
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityHealth,
        FlextObservabilityHTTP,
        FlextObservabilityHTTPClient,
        FlextObservabilityLogging,
        FlextObservabilityMonitor,
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
        FlextObservabilityServices,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": (
        "FlextObservabilityConfig",
        "config",
    ),
    "._settings": (
        "FlextObservabilitySettings",
        "settings",
    ),
    ".api": (
        "FlextObservability",
        "observability",
    ),
    ".constants": (
        "FlextObservabilityConstants",
        "c",
    ),
    ".models": (
        "FlextObservabilityModels",
        "m",
    ),
    ".protocols": (
        "FlextObservabilityProtocols",
        "p",
    ),
    ".services.advanced_context": ("FlextObservabilityAdvancedContext",),
    ".services.context": ("FlextObservabilityContext",),
    ".services.custom_metrics": ("FlextObservabilityCustomMetrics",),
    ".services.error_handling": ("FlextObservabilityErrorHandling",),
    ".services.health": ("FlextObservabilityHealth",),
    ".services.http_client_instrumentation": ("FlextObservabilityHTTPClient",),
    ".services.http_instrumentation": ("FlextObservabilityHTTP",),
    ".services.logging_integration": ("FlextObservabilityLogging",),
    ".services.monitoring": ("FlextObservabilityMonitor",),
    ".services.performance": ("FlextObservabilityPerformance",),
    ".services.sampling": ("FlextObservabilitySampling",),
    ".services.services": ("FlextObservabilityServices",),
    ".typings": (
        "FlextObservabilityTypes",
        "t",
    ),
    ".utilities": (
        "FlextObservabilityUtilities",
        "u",
    ),
    "flext_cli": (
        "d",
        "e",
        "h",
        "r",
        "s",
        "x",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityHealth",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
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
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "build_lazy_import_map",
    "c",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "observability",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
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
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "observability",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
