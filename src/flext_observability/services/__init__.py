# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
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
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".advanced_context": ("FlextObservabilityAdvancedContext",),
        ".context": ("FlextObservabilityContext",),
        ".custom_metrics": ("FlextObservabilityCustomMetrics",),
        ".error_handling": ("FlextObservabilityErrorHandling",),
        ".fields": ("FlextObservabilityFields",),
        ".health": ("FlextObservabilityHealth",),
        ".http_client_instrumentation": ("FlextObservabilityHTTPClient",),
        ".http_instrumentation": ("FlextObservabilityHTTP",),
        ".logging_integration": ("FlextObservabilityLogging",),
        ".monitoring": (
            "FlextObservabilityMonitor",
            "flext_monitor_function",
        ),
        ".performance": ("FlextObservabilityPerformance",),
        ".sampling": ("FlextObservabilitySampling",),
        ".services": ("FlextObservabilityServices",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
