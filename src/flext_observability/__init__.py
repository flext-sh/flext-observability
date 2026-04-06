# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_observability.__version__ import *

if _t.TYPE_CHECKING:
    import flext_observability.api as _flext_observability_api

    api = _flext_observability_api
    import flext_observability.base as _flext_observability_base
    from flext_observability.api import (
        FlextObservability,
        FlextObservabilityMasterFactory,
    )

    base = _flext_observability_base
    import flext_observability.constants as _flext_observability_constants
    from flext_observability.base import FlextObservabilityServiceBase, s

    constants = _flext_observability_constants
    import flext_observability.models as _flext_observability_models
    from flext_observability.constants import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )

    models = _flext_observability_models
    import flext_observability.protocols as _flext_observability_protocols
    from flext_observability.models import (
        FlextObservabilityModels,
        FlextObservabilityModels as m,
    )

    protocols = _flext_observability_protocols
    import flext_observability.services as _flext_observability_services
    from flext_observability.protocols import (
        FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )

    services = _flext_observability_services
    import flext_observability.settings as _flext_observability_settings
    from flext_observability.services import (
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityFields,
        FlextObservabilityHealth,
        FlextObservabilityHTTP,
        FlextObservabilityHTTPClient,
        FlextObservabilityLogging,
        FlextObservabilityMonitor,
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
        FlextObservabilityServices,
        advanced_context,
        context,
        custom_metrics,
        error_handling,
        fields,
        flext_monitor_function,
        health,
        http_client_instrumentation,
        http_instrumentation,
        logging_integration,
        monitoring,
        performance,
        sampling,
    )

    settings = _flext_observability_settings
    import flext_observability.typings as _flext_observability_typings
    from flext_observability.settings import FlextObservabilitySettings

    typings = _flext_observability_typings
    import flext_observability.utilities as _flext_observability_utilities
    from flext_observability.typings import (
        FlextObservabilityTypes,
        FlextObservabilityTypes as t,
    )

    utilities = _flext_observability_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_observability.utilities import (
        FlextObservabilityUtilities,
        FlextObservabilityUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_observability.services",),
    {
        "FlextObservability": ("flext_observability.api", "FlextObservability"),
        "FlextObservabilityConstants": (
            "flext_observability.constants",
            "FlextObservabilityConstants",
        ),
        "FlextObservabilityMasterFactory": (
            "flext_observability.api",
            "FlextObservabilityMasterFactory",
        ),
        "FlextObservabilityModels": (
            "flext_observability.models",
            "FlextObservabilityModels",
        ),
        "FlextObservabilityProtocols": (
            "flext_observability.protocols",
            "FlextObservabilityProtocols",
        ),
        "FlextObservabilityServiceBase": (
            "flext_observability.base",
            "FlextObservabilityServiceBase",
        ),
        "FlextObservabilitySettings": (
            "flext_observability.settings",
            "FlextObservabilitySettings",
        ),
        "FlextObservabilityTypes": (
            "flext_observability.typings",
            "FlextObservabilityTypes",
        ),
        "FlextObservabilityUtilities": (
            "flext_observability.utilities",
            "FlextObservabilityUtilities",
        ),
        "__author__": ("flext_observability.__version__", "__author__"),
        "__author_email__": ("flext_observability.__version__", "__author_email__"),
        "__description__": ("flext_observability.__version__", "__description__"),
        "__license__": ("flext_observability.__version__", "__license__"),
        "__title__": ("flext_observability.__version__", "__title__"),
        "__url__": ("flext_observability.__version__", "__url__"),
        "__version__": ("flext_observability.__version__", "__version__"),
        "__version_info__": ("flext_observability.__version__", "__version_info__"),
        "api": "flext_observability.api",
        "base": "flext_observability.base",
        "c": ("flext_observability.constants", "FlextObservabilityConstants"),
        "constants": "flext_observability.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_observability.models", "FlextObservabilityModels"),
        "models": "flext_observability.models",
        "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
        "protocols": "flext_observability.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_observability.base", "s"),
        "services": "flext_observability.services",
        "settings": "flext_observability.settings",
        "t": ("flext_observability.typings", "FlextObservabilityTypes"),
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
        "utilities": "flext_observability.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "FlextObservabilityMasterFactory",
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
    "advanced_context",
    "api",
    "base",
    "c",
    "constants",
    "context",
    "custom_metrics",
    "d",
    "e",
    "error_handling",
    "fields",
    "flext_monitor_function",
    "h",
    "health",
    "http_client_instrumentation",
    "http_instrumentation",
    "logging_integration",
    "m",
    "models",
    "monitoring",
    "p",
    "performance",
    "protocols",
    "r",
    "s",
    "sampling",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
