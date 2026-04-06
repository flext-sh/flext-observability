# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
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
    import flext_observability.services.services as _flext_observability_services_services
    from flext_observability.services.sampling import FlextObservabilitySampling

    services = _flext_observability_services_services
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_observability.services.services import FlextObservabilityServices
_LAZY_IMPORTS = {
    "FlextObservabilityAdvancedContext": (
        "flext_observability.services.advanced_context",
        "FlextObservabilityAdvancedContext",
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
    "FlextObservabilityMonitor": (
        "flext_observability.services.monitoring",
        "FlextObservabilityMonitor",
    ),
    "FlextObservabilityPerformance": (
        "flext_observability.services.performance",
        "FlextObservabilityPerformance",
    ),
    "FlextObservabilitySampling": (
        "flext_observability.services.sampling",
        "FlextObservabilitySampling",
    ),
    "FlextObservabilityServices": (
        "flext_observability.services.services",
        "FlextObservabilityServices",
    ),
    "advanced_context": "flext_observability.services.advanced_context",
    "c": ("flext_core.constants", "FlextConstants"),
    "context": "flext_observability.services.context",
    "custom_metrics": "flext_observability.services.custom_metrics",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_handling": "flext_observability.services.error_handling",
    "fields": "flext_observability.services.fields",
    "flext_monitor_function": (
        "flext_observability.services.monitoring",
        "flext_monitor_function",
    ),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "health": "flext_observability.services.health",
    "http_client_instrumentation": "flext_observability.services.http_client_instrumentation",
    "http_instrumentation": "flext_observability.services.http_instrumentation",
    "logging_integration": "flext_observability.services.logging_integration",
    "m": ("flext_core.models", "FlextModels"),
    "monitoring": "flext_observability.services.monitoring",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "performance": "flext_observability.services.performance",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sampling": "flext_observability.services.sampling",
    "services": "flext_observability.services.services",
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityFields",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilitySampling",
    "FlextObservabilityServices",
    "advanced_context",
    "c",
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
    "monitoring",
    "p",
    "performance",
    "r",
    "s",
    "sampling",
    "services",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
