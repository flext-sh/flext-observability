# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_observability.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_observability.advanced_context import FlextObservabilityAdvancedContext
    from flext_observability.api import FlextObservability
    from flext_observability.base import FlextObservabilityServiceBase
    from flext_observability.constants import FlextObservabilityConstants, c
    from flext_observability.context import FlextObservabilityContext
    from flext_observability.custom_metrics import FlextObservabilityCustomMetrics
    from flext_observability.error_handling import FlextObservabilityErrorHandling
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
    from flext_observability.performance import FlextObservabilityPerformance
    from flext_observability.protocols import FlextObservabilityProtocols, p
    from flext_observability.sampling import FlextObservabilitySampling
    from flext_observability.services import FlextObservabilityServices
    from flext_observability.settings import FlextObservabilitySettings
    from flext_observability.typings import FlextObservabilityTypes, t
    from flext_observability.utilities import FlextObservabilityUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".advanced_context": ("FlextObservabilityAdvancedContext",),
            ".api": ("FlextObservability",),
            ".base": ("FlextObservabilityServiceBase",),
            ".constants": (
                "FlextObservabilityConstants",
                "c",
            ),
            ".context": ("FlextObservabilityContext",),
            ".custom_metrics": ("FlextObservabilityCustomMetrics",),
            ".error_handling": ("FlextObservabilityErrorHandling",),
            ".fields": ("FlextObservabilityFields",),
            ".health": ("FlextObservabilityHealth",),
            ".http_client_instrumentation": ("FlextObservabilityHTTPClient",),
            ".http_instrumentation": ("FlextObservabilityHTTP",),
            ".logging_integration": ("FlextObservabilityLogging",),
            ".models": (
                "FlextObservabilityModels",
                "m",
            ),
            ".monitoring": (
                "FlextObservabilityMonitor",
                "flext_monitor_function",
            ),
            ".performance": ("FlextObservabilityPerformance",),
            ".protocols": (
                "FlextObservabilityProtocols",
                "p",
            ),
            ".sampling": ("FlextObservabilitySampling",),
            ".services": ("FlextObservabilityServices",),
            ".settings": ("FlextObservabilitySettings",),
            ".typings": (
                "FlextObservabilityTypes",
                "t",
            ),
            ".utilities": (
                "FlextObservabilityUtilities",
                "u",
            ),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
            "flext_core.service": ("s",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

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
    "d",
    "e",
    "flext_monitor_function",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
