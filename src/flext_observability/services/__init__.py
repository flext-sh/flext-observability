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
    "advanced_context": "flext_observability.services.advanced_context",
    "context": "flext_observability.services.context",
    "custom_metrics": "flext_observability.services.custom_metrics",
    "error_handling": "flext_observability.services.error_handling",
    "fields": "flext_observability.services.fields",
    "flext_monitor_function": (
        "flext_observability.services.monitoring",
        "flext_monitor_function",
    ),
    "health": "flext_observability.services.health",
    "http_client_instrumentation": "flext_observability.services.http_client_instrumentation",
    "http_instrumentation": "flext_observability.services.http_instrumentation",
    "logging_integration": "flext_observability.services.logging_integration",
    "monitoring": "flext_observability.services.monitoring",
    "performance": "flext_observability.services.performance",
    "sampling": "flext_observability.services.sampling",
    "services": "flext_observability.services.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
