# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

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
    "flext_monitor_function": (
        "flext_observability.services.monitoring",
        "flext_monitor_function",
    ),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
