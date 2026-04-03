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

    api = _flext_observability_api
    import flext_observability.base as _flext_observability_base
    from flext_observability.api import (
        FlextObservability,
        FlextObservabilityMasterFactory,
    )

    base = _flext_observability_base
    import flext_observability.constants as _flext_observability_constants
    from flext_observability.base import (
        FlextObservabilityServiceBase,
        FlextObservabilityServiceBase as s,
    )

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
    import flext_observability.services.advanced_context as _flext_observability_services_advanced_context

    advanced_context = _flext_observability_services_advanced_context
    import flext_observability.services.context as _flext_observability_services_context
    from flext_observability.services.advanced_context import (
        FlextObservabilityAdvancedContext,
    )

    context = _flext_observability_services_context
    import flext_observability.services.custom_metrics as _flext_observability_services_custom_metrics
    from flext_observability.services.context import FlextObservabilityContext

    custom_metrics = _flext_observability_services_custom_metrics
    import flext_observability.services.error_handling as _flext_observability_services_error_handling
    from flext_observability.services.custom_metrics import (
        FlextObservabilityCustomMetrics,
    )

    error_handling = _flext_observability_services_error_handling
    import flext_observability.services.fields as _flext_observability_services_fields
    from flext_observability.services.error_handling import (
        FlextObservabilityErrorHandling,
    )

    fields = _flext_observability_services_fields
    import flext_observability.services.health as _flext_observability_services_health
    from flext_observability.services.fields import FlextObservabilityFields

    health = _flext_observability_services_health
    import flext_observability.services.http_client_instrumentation as _flext_observability_services_http_client_instrumentation
    from flext_observability.services.health import FlextObservabilityHealth

    http_client_instrumentation = (
        _flext_observability_services_http_client_instrumentation
    )
    import flext_observability.services.http_instrumentation as _flext_observability_services_http_instrumentation
    from flext_observability.services.http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )

    http_instrumentation = _flext_observability_services_http_instrumentation
    import flext_observability.services.logging_integration as _flext_observability_services_logging_integration
    from flext_observability.services.http_instrumentation import FlextObservabilityHTTP

    logging_integration = _flext_observability_services_logging_integration
    import flext_observability.services.monitoring as _flext_observability_services_monitoring
    from flext_observability.services.logging_integration import (
        FlextObservabilityLogging,
    )

    monitoring = _flext_observability_services_monitoring
    import flext_observability.services.performance as _flext_observability_services_performance
    from flext_observability.services.monitoring import (
        FlextObservabilityMonitor,
        flext_monitor_function,
    )

    performance = _flext_observability_services_performance
    import flext_observability.services.sampling as _flext_observability_services_sampling
    from flext_observability.services.performance import FlextObservabilityPerformance

    sampling = _flext_observability_services_sampling
    import flext_observability.settings as _flext_observability_settings
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
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_observability.services",),
    {
        "FlextObservability": "flext_observability.api",
        "FlextObservabilityConstants": "flext_observability.constants",
        "FlextObservabilityMasterFactory": "flext_observability.api",
        "FlextObservabilityModels": "flext_observability.models",
        "FlextObservabilityProtocols": "flext_observability.protocols",
        "FlextObservabilityServiceBase": "flext_observability.base",
        "FlextObservabilitySettings": "flext_observability.settings",
        "FlextObservabilityTypes": "flext_observability.typings",
        "FlextObservabilityUtilities": "flext_observability.utilities",
        "__author__": "flext_observability.__version__",
        "__author_email__": "flext_observability.__version__",
        "__description__": "flext_observability.__version__",
        "__license__": "flext_observability.__version__",
        "__title__": "flext_observability.__version__",
        "__url__": "flext_observability.__version__",
        "__version__": "flext_observability.__version__",
        "__version_info__": "flext_observability.__version__",
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
        "s": ("flext_observability.base", "FlextObservabilityServiceBase"),
        "services": "flext_observability.services",
        "settings": "flext_observability.settings",
        "t": ("flext_observability.typings", "FlextObservabilityTypes"),
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
        "utilities": "flext_observability.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

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
