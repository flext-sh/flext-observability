# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import (
        cli,
        core,
        d,
        e,
        from_json,
        h,
        lazy_attribute,
        r,
        to_json,
        to_jsonable_python,
        x,
    )

    from . import services
    from ._config import FlextObservabilityConfig, config
    from ._settings import FlextObservabilitySettings, settings
    from .api import FlextObservability, observability
    from .base import FlextObservabilityServiceBase, s
    from .cli import FlextObservabilityCli, main
    from .constants import FlextObservabilityConstants, FlextObservabilityConstants as c
    from .models import FlextObservabilityModels, m
    from .protocols import FlextObservabilityProtocols, p
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
    from .typings import FlextObservabilityTypes, t
    from .utilities import FlextObservabilityUtilities, u
__all__: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityCli",
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
    "FlextObservabilityServiceBase",
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
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "observability",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "to_json",
    "to_jsonable_python",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextObservabilityConfig", "config"),
            "._settings": ("FlextObservabilitySettings", "settings"),
            ".api": ("FlextObservability", "observability"),
            ".base": ("FlextObservabilityServiceBase", "s"),
            ".cli": ("FlextObservabilityCli", "main"),
            ".constants": ("FlextObservabilityConstants", "c"),
            ".models": ("FlextObservabilityModels", "m"),
            ".protocols": ("FlextObservabilityProtocols", "p"),
            ".services": ("services",),
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
            ".typings": ("FlextObservabilityTypes", "t"),
            ".utilities": ("FlextObservabilityUtilities", "u"),
            "flext_cli": (
                "cli",
                "core",
                "d",
                "e",
                "from_json",
                "h",
                "lazy_attribute",
                "r",
                "to_json",
                "to_jsonable_python",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
