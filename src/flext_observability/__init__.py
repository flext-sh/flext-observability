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
    from flext_cli import d, e, h, r, s, x

    from ._config import FlextObservabilityConfig, config
    from ._settings import FlextObservabilitySettings, settings
    from .api import FlextObservability, observability
    from .constants import FlextObservabilityConstants, FlextObservabilityConstants as c
    from .models import FlextObservabilityModels, FlextObservabilityModels as m
    from .protocols import FlextObservabilityProtocols, FlextObservabilityProtocols as p
    from .typings import FlextObservabilityTypes, FlextObservabilityTypes as t
    from .utilities import FlextObservabilityUtilities, FlextObservabilityUtilities as u
__all__: tuple[str, ...] = (
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
    MappingProxyType(
        build_lazy_import_map(
            MappingProxyType({
                "._config": ("FlextObservabilityConfig", "config"),
                "._settings": ("FlextObservabilitySettings", "settings"),
                ".api": ("FlextObservability", "observability"),
                ".constants": ("FlextObservabilityConstants", "c"),
                ".models": ("FlextObservabilityModels", "m"),
                ".protocols": ("FlextObservabilityProtocols", "p"),
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
                "flext_cli": ("d", "e", "h", "r", "s", "x"),
            }),
            alias_groups=MappingProxyType({}),
            sort_keys=False,
        )
    ),
    public_exports=__all__,
)
