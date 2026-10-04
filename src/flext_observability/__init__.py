# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports
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
    from flext_cli import d, e, h, r, x

    from flext_observability import services
    from flext_observability._config import FlextObservabilityConfig, config
    from flext_observability._settings import FlextObservabilitySettings, settings
    from flext_observability.api import FlextObservability, observability
    from flext_observability.base import FlextObservabilityServiceBase, s
    from flext_observability.cli import FlextObservabilityCli, main
    from flext_observability.constants import FlextObservabilityConstants, c
    from flext_observability.models import FlextObservabilityModels, m
    from flext_observability.protocols import FlextObservabilityProtocols, p
    from flext_observability.services.advanced_context import (
        FlextObservabilityAdvancedContext,
    )
    from flext_observability.services.context import FlextObservabilityContext
    from flext_observability.services.custom_metrics import (
        FlextObservabilityCustomMetrics,
    )
    from flext_observability.services.error_handling import (
        FlextObservabilityErrorHandling,
    )
    from flext_observability.services.health import FlextObservabilityHealth
    from flext_observability.services.http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )
    from flext_observability.services.http_instrumentation import FlextObservabilityHTTP
    from flext_observability.services.logging_integration import (
        FlextObservabilityLogging,
    )
    from flext_observability.services.monitoring import FlextObservabilityMonitor
    from flext_observability.services.performance import FlextObservabilityPerformance
    from flext_observability.services.sampling import FlextObservabilitySampling
    from flext_observability.services.services import FlextObservabilityServices
    from flext_observability.typings import FlextObservabilityTypes, t
    from flext_observability.utilities import FlextObservabilityUtilities, u


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
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "observability",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservability": ".api",
        "FlextObservabilityAdvancedContext": ".services.advanced_context",
        "FlextObservabilityCli": ".cli",
        "FlextObservabilityConfig": "._config",
        "FlextObservabilityConstants": ".constants",
        "FlextObservabilityContext": ".services.context",
        "FlextObservabilityCustomMetrics": ".services.custom_metrics",
        "FlextObservabilityErrorHandling": ".services.error_handling",
        "FlextObservabilityHTTP": ".services.http_instrumentation",
        "FlextObservabilityHTTPClient": ".services.http_client_instrumentation",
        "FlextObservabilityHealth": ".services.health",
        "FlextObservabilityLogging": ".services.logging_integration",
        "FlextObservabilityModels": ".models",
        "FlextObservabilityMonitor": ".services.monitoring",
        "FlextObservabilityPerformance": ".services.performance",
        "FlextObservabilityProtocols": ".protocols",
        "FlextObservabilitySampling": ".services.sampling",
        "FlextObservabilityServiceBase": ".base",
        "FlextObservabilityServices": ".services.services",
        "FlextObservabilitySettings": "._settings",
        "FlextObservabilityTypes": ".typings",
        "FlextObservabilityUtilities": ".utilities",
        "c": ".constants",
        "config": "._config",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "observability": ".api",
        "p": ".protocols",
        "r": "flext_cli",
        "s": ".base",
        "services": ".services",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)
