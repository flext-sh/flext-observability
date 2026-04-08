# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports
from flext_observability.__version__ import *

if _t.TYPE_CHECKING:
    import flext_observability.api as _flext_observability_api

    api = _flext_observability_api
    import flext_observability.base as _flext_observability_base
    from flext_observability.api import FlextObservability

    base = _flext_observability_base
    import flext_observability.constants as _flext_observability_constants
    from flext_observability.base import FlextObservabilityServiceBase, s

    constants = _flext_observability_constants
    import flext_observability.factory as _flext_observability_factory
    import flext_observability.models as _flext_observability_models
    from flext_observability.constants import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )

    factory = _flext_observability_factory
    from flext_observability.factory import FlextObservabilityMasterFactory

    models = _flext_observability_models
    import flext_observability.protocols as _flext_observability_protocols
    from flext_observability.models import (
        FlextObservabilityModels,
        FlextObservabilityModels as m,
    )

    protocols = _flext_observability_protocols
    import flext_observability.settings as _flext_observability_settings
    from flext_observability.protocols import (
        FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )
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
    from flext_observability.services.fields import FlextObservabilityFields
    from flext_observability.services.health import FlextObservabilityHealth
    from flext_observability.services.http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )
    from flext_observability.services.http_instrumentation import FlextObservabilityHTTP
    from flext_observability.services.logging_integration import (
        FlextObservabilityLogging,
    )
    from flext_observability.services.monitoring import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )
    from flext_observability.services.performance import FlextObservabilityPerformance
    from flext_observability.services.sampling import FlextObservabilitySampling
    from flext_observability.services.services import FlextObservabilityServices

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
_LAZY_IMPORTS = {
    "FlextObservability": ("flext_observability.api", "FlextObservability"),
    "FlextObservabilityAdvancedContext": (
        "flext_observability.services.advanced_context",
        "FlextObservabilityAdvancedContext",
    ),
    "FlextObservabilityConstants": (
        "flext_observability.constants",
        "FlextObservabilityConstants",
    ),
    "FlextObservabilityContext": (
        "flext_observability.services.context",
        "FlextObservabilityContext",
    ),
    "FlextObservabilityCustomMetrics": (
        "flext_observability.services.custom_metrics",
        "FlextObservabilityCustomMetrics",
    ),
    "FlextObservabilityErrorHandling": (
        "flext_observability.services.error_handling",
        "FlextObservabilityErrorHandling",
    ),
    "FlextObservabilityFields": (
        "flext_observability.services.fields",
        "FlextObservabilityFields",
    ),
    "FlextObservabilityHTTP": (
        "flext_observability.services.http_instrumentation",
        "FlextObservabilityHTTP",
    ),
    "FlextObservabilityHTTPClient": (
        "flext_observability.services.http_client_instrumentation",
        "FlextObservabilityHTTPClient",
    ),
    "FlextObservabilityHealth": (
        "flext_observability.services.health",
        "FlextObservabilityHealth",
    ),
    "FlextObservabilityLogging": (
        "flext_observability.services.logging_integration",
        "FlextObservabilityLogging",
    ),
    "FlextObservabilityMasterFactory": (
        "flext_observability.factory",
        "FlextObservabilityMasterFactory",
    ),
    "FlextObservabilityModels": (
        "flext_observability.models",
        "FlextObservabilityModels",
    ),
    "FlextObservabilityMonitor": (
        "flext_observability.services.monitoring",
        "FlextObservabilityMonitor",
    ),
    "FlextObservabilityPerformance": (
        "flext_observability.services.performance",
        "FlextObservabilityPerformance",
    ),
    "FlextObservabilityProtocols": (
        "flext_observability.protocols",
        "FlextObservabilityProtocols",
    ),
    "FlextObservabilitySampling": (
        "flext_observability.services.sampling",
        "FlextObservabilitySampling",
    ),
    "FlextObservabilityServiceBase": (
        "flext_observability.base",
        "FlextObservabilityServiceBase",
    ),
    "FlextObservabilityServices": (
        "flext_observability.services.services",
        "FlextObservabilityServices",
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
    "factory": "flext_observability.factory",
    "flext_monitor_function": (
        "flext_observability.services.monitoring",
        "flext_monitor_function",
    ),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_observability.models", "FlextObservabilityModels"),
    "models": "flext_observability.models",
    "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
    "protocols": "flext_observability.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_observability.base", "s"),
    "settings": "flext_observability.settings",
    "t": ("flext_observability.typings", "FlextObservabilityTypes"),
    "typings": "flext_observability.typings",
    "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
    "utilities": "flext_observability.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

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
    "api",
    "base",
    "c",
    "constants",
    "d",
    "e",
    "factory",
    "flext_monitor_function",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
