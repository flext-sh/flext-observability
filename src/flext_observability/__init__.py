# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from . import services as services
    from enum import StrEnum, unique
    from flext_cli import d, e, h, r, s, x
    from typing import ClassVar, Final

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
    from .services.monitoring import FlextObservabilityMonitor, flext_monitor_function
    from .services.performance import FlextObservabilityPerformance
    from .services.sampling import FlextObservabilitySampling
    from .services.services import FlextObservabilityServices
    from .typings import FlextObservabilityTypes, FlextObservabilityTypes as t
    from .utilities import FlextObservabilityUtilities, FlextObservabilityUtilities as u
__all__: tuple[str, ...] = (
    "ClassVar",
    "Final",
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
    "StrEnum",
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
    "flext_monitor_function",
    "h",
    "m",
    "observability",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "unique",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextObservabilityConfig", "config"),
            "._settings": ("FlextObservabilitySettings", "settings"),
            ".api": ("FlextObservability", "observability"),
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
            ".services.monitoring": (
                "FlextObservabilityMonitor",
                "flext_monitor_function",
            ),
            ".services.performance": ("FlextObservabilityPerformance",),
            ".services.sampling": ("FlextObservabilitySampling",),
            ".services.services": ("FlextObservabilityServices",),
            ".typings": ("FlextObservabilityTypes", "t"),
            ".utilities": ("FlextObservabilityUtilities", "u"),
            "enum": ("StrEnum", "unique"),
            "flext_cli": ("d", "e", "h", "r", "s", "x"),
            "typing": ("ClassVar", "Final"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
