# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_observability.__version__ import *
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

if _t.TYPE_CHECKING:
    import flext_observability.api as _flext_observability_api

    api = _flext_observability_api
    import flext_observability.base as _flext_observability_base

    base = _flext_observability_base
    import flext_observability.constants as _flext_observability_constants

    constants = _flext_observability_constants
    import flext_observability.models as _flext_observability_models

    models = _flext_observability_models
    import flext_observability.protocols as _flext_observability_protocols

    protocols = _flext_observability_protocols
    import flext_observability.services as _flext_observability_services

    services = _flext_observability_services
    import flext_observability.services.advanced_context as _flext_observability_services_advanced_context

    advanced_context = _flext_observability_services_advanced_context
    import flext_observability.services.context as _flext_observability_services_context

    context = _flext_observability_services_context
    import flext_observability.services.custom_metrics as _flext_observability_services_custom_metrics

    custom_metrics = _flext_observability_services_custom_metrics
    import flext_observability.services.error_handling as _flext_observability_services_error_handling

    error_handling = _flext_observability_services_error_handling
    import flext_observability.services.fields as _flext_observability_services_fields

    fields = _flext_observability_services_fields
    import flext_observability.services.health as _flext_observability_services_health

    health = _flext_observability_services_health
    import flext_observability.services.http_client_instrumentation as _flext_observability_services_http_client_instrumentation

    http_client_instrumentation = (
        _flext_observability_services_http_client_instrumentation
    )
    import flext_observability.services.http_instrumentation as _flext_observability_services_http_instrumentation

    http_instrumentation = _flext_observability_services_http_instrumentation
    import flext_observability.services.logging_integration as _flext_observability_services_logging_integration

    logging_integration = _flext_observability_services_logging_integration
    import flext_observability.services.monitoring as _flext_observability_services_monitoring

    monitoring = _flext_observability_services_monitoring
    import flext_observability.services.performance as _flext_observability_services_performance

    performance = _flext_observability_services_performance
    import flext_observability.services.sampling as _flext_observability_services_sampling

    sampling = _flext_observability_services_sampling
    import flext_observability.settings as _flext_observability_settings

    settings = _flext_observability_settings
    import flext_observability.typings as _flext_observability_typings

    typings = _flext_observability_typings
    import flext_observability.utilities as _flext_observability_utilities

    utilities = _flext_observability_utilities

    _ = (
        FlextObservability,
        FlextObservabilityAdvancedContext,
        FlextObservabilityConstants,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityFields,
        FlextObservabilityHTTP,
        FlextObservabilityHTTPClient,
        FlextObservabilityHealth,
        FlextObservabilityLogging,
        FlextObservabilityMasterFactory,
        FlextObservabilityModels,
        FlextObservabilityMonitor,
        FlextObservabilityPerformance,
        FlextObservabilityProtocols,
        FlextObservabilitySampling,
        FlextObservabilityServiceBase,
        FlextObservabilityServices,
        FlextObservabilitySettings,
        FlextObservabilityTypes,
        FlextObservabilityUtilities,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        advanced_context,
        api,
        base,
        c,
        constants,
        context,
        custom_metrics,
        d,
        e,
        error_handling,
        fields,
        flext_monitor_function,
        h,
        health,
        http_client_instrumentation,
        http_instrumentation,
        logging_integration,
        m,
        models,
        monitoring,
        p,
        performance,
        protocols,
        r,
        s,
        sampling,
        services,
        settings,
        t,
        typings,
        u,
        utilities,
        x,
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
