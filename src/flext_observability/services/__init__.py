# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from flext_observability.services import (
        advanced_context,
        context,
        custom_metrics,
        error_handling,
        fields,
        health,
        http_client_instrumentation,
        http_instrumentation,
        logging_integration,
        monitoring,
        performance,
        sampling,
        services,
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextObservabilityAdvancedContext": "flext_observability.services.advanced_context",
    "FlextObservabilityContext": "flext_observability.services.context",
    "FlextObservabilityCustomMetrics": "flext_observability.services.custom_metrics",
    "FlextObservabilityErrorHandling": "flext_observability.services.error_handling",
    "FlextObservabilityFields": "flext_observability.services.fields",
    "FlextObservabilityHTTP": "flext_observability.services.http_instrumentation",
    "FlextObservabilityHTTPClient": "flext_observability.services.http_client_instrumentation",
    "FlextObservabilityHealth": "flext_observability.services.health",
    "FlextObservabilityLogging": "flext_observability.services.logging_integration",
    "FlextObservabilityMonitor": "flext_observability.services.monitoring",
    "FlextObservabilityPerformance": "flext_observability.services.performance",
    "FlextObservabilitySampling": "flext_observability.services.sampling",
    "FlextObservabilityServices": "flext_observability.services.services",
    "advanced_context": "flext_observability.services.advanced_context",
    "c": ("flext_core.constants", "FlextConstants"),
    "context": "flext_observability.services.context",
    "custom_metrics": "flext_observability.services.custom_metrics",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_handling": "flext_observability.services.error_handling",
    "fields": "flext_observability.services.fields",
    "flext_monitor_function": "flext_observability.services.monitoring",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
