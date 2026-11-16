# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._models.base import FlextObservabilityModelsBase
    from flext_observability._models.domains import FlextObservabilityModelsDomains


__all__: tuple[str, ...] = (
    "FlextObservabilityModelsBase",
    "FlextObservabilityModelsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextObservabilityModelsBase": ".base",
        "FlextObservabilityModelsDomains": ".domains",
    },
    public_exports=__all__,
    deferred_members={
        "FlextObservabilityModelsBase": (),
        "FlextObservabilityModelsDomains": (
            "MetricEntry",
            "_EntityWithId",
            "Metric",
            "Trace",
            "Alert",
            "HealthCheck",
            "LogEntry",
            "StartTimePayload",
            "HeadersPayload",
            "ContextSnapshot",
            "BaggageKeyModel",
            "MetricTypeInput",
            "CustomMetricDefinition",
            "CooldownInput",
            "ThresholdInput",
            "ErrorHandlingState",
            "ErrorEvent",
            "LogContext",
            "PerformanceMetrics",
        ),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextObservabilityModelsBase": (
            ("flext_observability", "FlextObservabilityModelsConfig"),
        ),
    },
)
