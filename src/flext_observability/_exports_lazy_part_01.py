# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_OBSERVABILITY_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".api": (
            "FlextObservability",
            "observability",
        ),
        ".constants": (
            "FlextObservabilityConstants",
            "c",
        ),
        ".models": (
            "FlextObservabilityModels",
            "m",
        ),
        ".protocols": (
            "FlextObservabilityProtocols",
            "p",
        ),
        ".services": ("services",),
        ".services.advanced_context": ("FlextObservabilityAdvancedContext",),
        ".services.context": ("FlextObservabilityContext",),
        ".services.custom_metrics": ("FlextObservabilityCustomMetrics",),
        ".services.error_handling": ("FlextObservabilityErrorHandling",),
        ".services.fields": ("FlextObservabilityFields",),
        ".services.health": ("FlextObservabilityHealth",),
        ".services.http_client_instrumentation": ("FlextObservabilityHTTPClient",),
        ".services.http_instrumentation": ("FlextObservabilityHTTP",),
        ".services.logging_integration": ("FlextObservabilityLogging",),
        ".services.monitoring": (
            "FlextObservabilityMonitor",
            "flext_monitor_function",
        ),
        ".services.performance": ("FlextObservabilityPerformance",),
        ".services.sampling": ("FlextObservabilitySampling",),
        ".services.services": ("FlextObservabilityServices",),
        ".settings": ("FlextObservabilitySettings",),
        ".typings": (
            "FlextObservabilityTypes",
            "t",
        ),
        ".utilities": ("FlextObservabilityUtilities",),
        "flext_core": (
            "d",
            "e",
            "h",
            "r",
            "s",
        ),
    },
)

__all__: list[str] = ["FLEXT_OBSERVABILITY_LAZY_IMPORTS_PART_01"]
