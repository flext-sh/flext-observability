# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextObservabilityAdvancedContext": ".advanced_context",
    "FlextObservabilityContext": ".context",
    "FlextObservabilityCustomMetrics": ".custom_metrics",
    "FlextObservabilityErrorHandling": ".error_handling",
    "FlextObservabilityFields": ".fields",
    "FlextObservabilityHTTP": ".http_instrumentation",
    "FlextObservabilityHTTPClient": ".http_client_instrumentation",
    "FlextObservabilityHealth": ".health",
    "FlextObservabilityLogging": ".logging_integration",
    "FlextObservabilityMonitor": ".monitoring",
    "FlextObservabilityPerformance": ".performance",
    "FlextObservabilitySampling": ".sampling",
    "FlextObservabilityServices": ".services",
    "flext_monitor_function": ".monitoring",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
