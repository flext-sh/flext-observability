# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".advanced_context": ("FlextObservabilityAdvancedContext",),
            ".context": ("FlextObservabilityContext",),
            ".custom_metrics": ("FlextObservabilityCustomMetrics",),
            ".error_handling": ("FlextObservabilityErrorHandling",),
            ".health": ("FlextObservabilityHealth",),
            ".http_client_instrumentation": ("FlextObservabilityHTTPClient",),
            ".http_instrumentation": ("FlextObservabilityHTTP",),
            ".logging_integration": ("FlextObservabilityLogging",),
            ".monitoring": ("FlextObservabilityMonitor",),
            ".performance": ("FlextObservabilityPerformance",),
            ".sampling": ("FlextObservabilitySampling",),
            ".services": ("FlextObservabilityServices",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
