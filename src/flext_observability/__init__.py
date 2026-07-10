# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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
    from flext_core._root_typing_parts.facades import (
        d as d,
        e as e,
        h as h,
        r as r,
        s as s,
        x as x,
    )
    from flext_observability.api import (
        FlextObservability as FlextObservability,
        observability as observability,
    )
    from flext_observability.constants import (
        FlextObservabilityConstants as FlextObservabilityConstants,
        c as c,
    )
    from flext_observability.models import (
        FlextObservabilityModels as FlextObservabilityModels,
        m as m,
    )
    from flext_observability.protocols import (
        FlextObservabilityProtocols as FlextObservabilityProtocols,
        p as p,
    )
    from flext_observability.services.advanced_context import (
        FlextObservabilityAdvancedContext as FlextObservabilityAdvancedContext,
    )
    from flext_observability.services.context import (
        FlextObservabilityContext as FlextObservabilityContext,
    )
    from flext_observability.services.custom_metrics import (
        FlextObservabilityCustomMetrics as FlextObservabilityCustomMetrics,
    )
    from flext_observability.services.error_handling import (
        FlextObservabilityErrorHandling as FlextObservabilityErrorHandling,
    )
    from flext_observability.services.fields import (
        FlextObservabilityFields as FlextObservabilityFields,
    )
    from flext_observability.services.health import (
        FlextObservabilityHealth as FlextObservabilityHealth,
    )
    from flext_observability.services.http_client_instrumentation import (
        FlextObservabilityHTTPClient as FlextObservabilityHTTPClient,
    )
    from flext_observability.services.http_instrumentation import (
        FlextObservabilityHTTP as FlextObservabilityHTTP,
    )
    from flext_observability.services.logging_integration import (
        FlextObservabilityLogging as FlextObservabilityLogging,
    )
    from flext_observability.services.monitoring import (
        FlextObservabilityMonitor as FlextObservabilityMonitor,
        flext_monitor_function as flext_monitor_function,
    )
    from flext_observability.services.performance import (
        FlextObservabilityPerformance as FlextObservabilityPerformance,
    )
    from flext_observability.services.sampling import (
        FlextObservabilitySampling as FlextObservabilitySampling,
    )
    from flext_observability.services.services import (
        FlextObservabilityServices as FlextObservabilityServices,
    )
    from flext_observability.typings import (
        FlextObservabilityTypes as FlextObservabilityTypes,
        t as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities as FlextObservabilityUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    build_lazy_import_map(
        {
            "._settings": ("FlextObservabilitySettings", "settings"),
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
            ".services.fields": ("FlextObservabilityFields",),
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
            ".typings": (
                "FlextObservabilityTypes",
                "t",
            ),
            ".utilities": (
                "FlextObservabilityUtilities",
                "u",
            ),
            "flext_core._root_typing_parts.facades": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


__all__: tuple[str, ...] = (
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
