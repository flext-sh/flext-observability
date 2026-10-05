# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
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
    from flext_observability.services.health import FlextObservabilityHealth
    from flext_observability.services.http_client_instrumentation import (
        FlextObservabilityHTTPClient,
    )
    from flext_observability.services.http_instrumentation import FlextObservabilityHTTP
    from flext_observability.services.logging_integration import (
        FlextObservabilityLogging,
    )
    from flext_observability.services.monitoring import FlextObservabilityMonitor
    from flext_observability.services.performance import FlextObservabilityPerformance
    from flext_observability.services.sampling import FlextObservabilitySampling
    from flext_observability.services.services import FlextObservabilityServices


__all__: tuple[str, ...] = (
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilitySampling",
    "FlextObservabilityServices",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityAdvancedContext": ".advanced_context",
        "FlextObservabilityContext": ".context",
        "FlextObservabilityCustomMetrics": ".custom_metrics",
        "FlextObservabilityErrorHandling": ".error_handling",
        "FlextObservabilityHTTP": ".http_instrumentation",
        "FlextObservabilityHTTPClient": ".http_client_instrumentation",
        "FlextObservabilityHealth": ".health",
        "FlextObservabilityLogging": ".logging_integration",
        "FlextObservabilityMonitor": ".monitoring",
        "FlextObservabilityPerformance": ".performance",
        "FlextObservabilitySampling": ".sampling",
        "FlextObservabilityServices": ".services",
    }),
    public_exports=__all__,
)
