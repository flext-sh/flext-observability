# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
