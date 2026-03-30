# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_observability.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_observability import (
        advanced_context as advanced_context,
        constants as constants,
        context as context,
        core as core,
        custom_metrics as custom_metrics,
        error_handling as error_handling,
        fields as fields,
        health as health,
        http_client_instrumentation as http_client_instrumentation,
        http_instrumentation as http_instrumentation,
        logging_integration as logging_integration,
        models as models,
        monitoring as monitoring,
        observability_logging as observability_logging,
        performance as performance,
        protocols as protocols,
        sampling as sampling,
        services as services,
        settings as settings,
        typings as typings,
        utilities as utilities,
    )
    from flext_observability._utilities._advanced_context import (
        FlextObservabilityAdvancedContext as FlextObservabilityAdvancedContext,
    )
    from flext_observability._utilities._context import (
        FlextObservabilityContext as FlextObservabilityContext,
    )
    from flext_observability._utilities._custom_metrics import (
        FlextObservabilityCustomMetrics as FlextObservabilityCustomMetrics,
    )
    from flext_observability._utilities._error_handling import (
        FlextObservabilityErrorHandling as FlextObservabilityErrorHandling,
    )
    from flext_observability._utilities._fields import (
        FlextObservabilityFields as FlextObservabilityFields,
    )
    from flext_observability._utilities._health import (
        FlextObservabilityHealth as FlextObservabilityHealth,
    )
    from flext_observability._utilities._http_client_instrumentation import (
        FlextObservabilityHTTPClient as FlextObservabilityHTTPClient,
    )
    from flext_observability._utilities._http_instrumentation import (
        FlextObservabilityHTTP as FlextObservabilityHTTP,
    )
    from flext_observability._utilities._logging_integration import (
        FlextObservabilityLogging as FlextObservabilityLogging,
    )
    from flext_observability._utilities._performance import (
        FlextObservabilityPerformance as FlextObservabilityPerformance,
    )
    from flext_observability._utilities._sampling import (
        FlextObservabilitySampling as FlextObservabilitySampling,
    )
    from flext_observability._utilities._services import (
        FlextObservabilityServices as FlextObservabilityServices,
    )
    from flext_observability.constants import (
        FlextObservabilityConstants as FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )
    from flext_observability.core import (
        FlextObservability as FlextObservability,
        FlextObservabilityMasterFactory as FlextObservabilityMasterFactory,
    )
    from flext_observability.models import (
        FlextObservabilityModels as FlextObservabilityModels,
        FlextObservabilityModels as m,
    )
    from flext_observability.monitoring import (
        FlextObservabilityMonitor as FlextObservabilityMonitor,
        flext_monitor_function as flext_monitor_function,
    )
    from flext_observability.protocols import (
        FlextObservabilityProtocols as FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )
    from flext_observability.settings import (
        FlextObservabilitySettings as FlextObservabilitySettings,
    )
    from flext_observability.typings import (
        FlextObservabilityTypes as FlextObservabilityTypes,
        FlextObservabilityTypes as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities as FlextObservabilityUtilities,
        FlextObservabilityUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextObservability": ["flext_observability.core", "FlextObservability"],
    "FlextObservabilityAdvancedContext": [
        "flext_observability._utilities._advanced_context",
        "FlextObservabilityAdvancedContext",
    ],
    "FlextObservabilityConstants": [
        "flext_observability.constants",
        "FlextObservabilityConstants",
    ],
    "FlextObservabilityContext": [
        "flext_observability._utilities._context",
        "FlextObservabilityContext",
    ],
    "FlextObservabilityCustomMetrics": [
        "flext_observability._utilities._custom_metrics",
        "FlextObservabilityCustomMetrics",
    ],
    "FlextObservabilityErrorHandling": [
        "flext_observability._utilities._error_handling",
        "FlextObservabilityErrorHandling",
    ],
    "FlextObservabilityFields": [
        "flext_observability._utilities._fields",
        "FlextObservabilityFields",
    ],
    "FlextObservabilityHTTP": [
        "flext_observability._utilities._http_instrumentation",
        "FlextObservabilityHTTP",
    ],
    "FlextObservabilityHTTPClient": [
        "flext_observability._utilities._http_client_instrumentation",
        "FlextObservabilityHTTPClient",
    ],
    "FlextObservabilityHealth": [
        "flext_observability._utilities._health",
        "FlextObservabilityHealth",
    ],
    "FlextObservabilityLogging": [
        "flext_observability._utilities._logging_integration",
        "FlextObservabilityLogging",
    ],
    "FlextObservabilityMasterFactory": [
        "flext_observability.core",
        "FlextObservabilityMasterFactory",
    ],
    "FlextObservabilityModels": [
        "flext_observability.models",
        "FlextObservabilityModels",
    ],
    "FlextObservabilityMonitor": [
        "flext_observability.monitoring",
        "FlextObservabilityMonitor",
    ],
    "FlextObservabilityPerformance": [
        "flext_observability._utilities._performance",
        "FlextObservabilityPerformance",
    ],
    "FlextObservabilityProtocols": [
        "flext_observability.protocols",
        "FlextObservabilityProtocols",
    ],
    "FlextObservabilitySampling": [
        "flext_observability._utilities._sampling",
        "FlextObservabilitySampling",
    ],
    "FlextObservabilityServices": [
        "flext_observability._utilities._services",
        "FlextObservabilityServices",
    ],
    "FlextObservabilitySettings": [
        "flext_observability.settings",
        "FlextObservabilitySettings",
    ],
    "FlextObservabilityTypes": [
        "flext_observability.typings",
        "FlextObservabilityTypes",
    ],
    "FlextObservabilityUtilities": [
        "flext_observability.utilities",
        "FlextObservabilityUtilities",
    ],
    "advanced_context": ["flext_observability.advanced_context", ""],
    "c": ["flext_observability.constants", "FlextObservabilityConstants"],
    "constants": ["flext_observability.constants", ""],
    "context": ["flext_observability.context", ""],
    "core": ["flext_observability.core", ""],
    "custom_metrics": ["flext_observability.custom_metrics", ""],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "error_handling": ["flext_observability.error_handling", ""],
    "fields": ["flext_observability.fields", ""],
    "flext_monitor_function": [
        "flext_observability.monitoring",
        "flext_monitor_function",
    ],
    "h": ["flext_core", "h"],
    "health": ["flext_observability.health", ""],
    "http_client_instrumentation": [
        "flext_observability.http_client_instrumentation",
        "",
    ],
    "http_instrumentation": ["flext_observability.http_instrumentation", ""],
    "logging_integration": ["flext_observability.logging_integration", ""],
    "m": ["flext_observability.models", "FlextObservabilityModels"],
    "models": ["flext_observability.models", ""],
    "monitoring": ["flext_observability.monitoring", ""],
    "observability_logging": ["flext_observability.observability_logging", ""],
    "p": ["flext_observability.protocols", "FlextObservabilityProtocols"],
    "performance": ["flext_observability.performance", ""],
    "protocols": ["flext_observability.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "sampling": ["flext_observability.sampling", ""],
    "services": ["flext_observability.services", ""],
    "settings": ["flext_observability.settings", ""],
    "t": ["flext_observability.typings", "FlextObservabilityTypes"],
    "typings": ["flext_observability.typings", ""],
    "u": ["flext_observability.utilities", "FlextObservabilityUtilities"],
    "utilities": ["flext_observability.utilities", ""],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextObservability",
    "FlextObservabilityAdvancedContext",
    "FlextObservabilityConstants",
    "FlextObservabilityContext",
    "FlextObservabilityCustomMetrics",
    "FlextObservabilityErrorHandling",
    "FlextObservabilityFields",
    "FlextObservabilityHTTP",
    "FlextObservabilityHTTPClient",
    "FlextObservabilityHealth",
    "FlextObservabilityLogging",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityPerformance",
    "FlextObservabilityProtocols",
    "FlextObservabilitySampling",
    "FlextObservabilityServices",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "advanced_context",
    "c",
    "constants",
    "context",
    "core",
    "custom_metrics",
    "d",
    "e",
    "error_handling",
    "fields",
    "flext_monitor_function",
    "h",
    "health",
    "http_client_instrumentation",
    "http_instrumentation",
    "logging_integration",
    "m",
    "models",
    "monitoring",
    "observability_logging",
    "p",
    "performance",
    "protocols",
    "r",
    "s",
    "sampling",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
