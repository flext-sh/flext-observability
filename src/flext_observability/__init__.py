# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports
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
from flext_observability._exports import FLEXT_OBSERVABILITY_LAZY_IMPORTS

_LAZY_IMPORTS = FLEXT_OBSERVABILITY_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = (
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
    "FlextObservabilityServices",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "flext_monitor_function",
    "observability",
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
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
