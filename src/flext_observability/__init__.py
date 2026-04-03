# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_observability.__version__ import (
    __all__,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_observability import (
        advanced_context,
        api,
        base,
        constants,
        context,
        custom_metrics,
        error_handling,
        fields,
        health,
        http_client_instrumentation,
        http_instrumentation,
        logging_integration,
        models,
        monitoring,
        performance,
        protocols,
        sampling,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_observability.api import (
        FlextObservability,
        FlextObservabilityMasterFactory,
    )
    from flext_observability.base import FlextObservabilityServiceBase, s
    from flext_observability.constants import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
    )
    from flext_observability.models import (
        FlextObservabilityModels,
        FlextObservabilityModels as m,
    )
    from flext_observability.protocols import (
        FlextObservabilityProtocols,
        FlextObservabilityProtocols as p,
    )
    from flext_observability.services import (
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityFields,
        FlextObservabilityHealth,
        FlextObservabilityHTTP,
        FlextObservabilityHTTPClient,
        FlextObservabilityLogging,
        FlextObservabilityMonitor,
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
        FlextObservabilityServices,
        flext_monitor_function,
    )
    from flext_observability.settings import FlextObservabilitySettings
    from flext_observability.typings import (
        FlextObservabilityTypes,
        FlextObservabilityTypes as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities,
        FlextObservabilityUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_observability.services",),
    {
        "FlextObservability": "flext_observability.api",
        "FlextObservabilityConstants": "flext_observability.constants",
        "FlextObservabilityMasterFactory": "flext_observability.api",
        "FlextObservabilityModels": "flext_observability.models",
        "FlextObservabilityProtocols": "flext_observability.protocols",
        "FlextObservabilityServiceBase": "flext_observability.base",
        "FlextObservabilitySettings": "flext_observability.settings",
        "FlextObservabilityTypes": "flext_observability.typings",
        "FlextObservabilityUtilities": "flext_observability.utilities",
        "advanced_context": "flext_observability.services.advanced_context",
        "api": "flext_observability.api",
        "base": "flext_observability.base",
        "c": ("flext_observability.constants", "FlextObservabilityConstants"),
        "constants": "flext_observability.constants",
        "context": "flext_observability.services.context",
        "custom_metrics": "flext_observability.services.custom_metrics",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "error_handling": "flext_observability.services.error_handling",
        "fields": "flext_observability.services.fields",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "health": "flext_observability.services.health",
        "http_client_instrumentation": "flext_observability.services.http_client_instrumentation",
        "http_instrumentation": "flext_observability.services.http_instrumentation",
        "logging_integration": "flext_observability.services.logging_integration",
        "m": ("flext_observability.models", "FlextObservabilityModels"),
        "models": "flext_observability.models",
        "monitoring": "flext_observability.services.monitoring",
        "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
        "performance": "flext_observability.services.performance",
        "protocols": "flext_observability.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": "flext_observability.base",
        "sampling": "flext_observability.services.sampling",
        "services": "flext_observability.services",
        "settings": "flext_observability.settings",
        "t": ("flext_observability.typings", "FlextObservabilityTypes"),
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
        "utilities": "flext_observability.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
