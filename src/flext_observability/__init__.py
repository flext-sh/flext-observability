# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import d, e, h, r, s, x

    from flext_observability.__version__ import *
    from flext_observability._utilities import *
    from flext_observability.constants import *
    from flext_observability.core import *
    from flext_observability.models import *
    from flext_observability.monitoring import *
    from flext_observability.protocols import *
    from flext_observability.settings import *
    from flext_observability.typings import *
    from flext_observability.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_observability._utilities",),
    {
        "FlextObservability": "flext_observability.core",
        "FlextObservabilityConstants": "flext_observability.constants",
        "FlextObservabilityMasterFactory": "flext_observability.core",
        "FlextObservabilityModels": "flext_observability.models",
        "FlextObservabilityMonitor": "flext_observability.monitoring",
        "FlextObservabilityProtocols": "flext_observability.protocols",
        "FlextObservabilitySettings": "flext_observability.settings",
        "FlextObservabilityTypes": "flext_observability.typings",
        "FlextObservabilityUtilities": "flext_observability.utilities",
        "__author__": "flext_observability.__version__",
        "__author_email__": "flext_observability.__version__",
        "__description__": "flext_observability.__version__",
        "__license__": "flext_observability.__version__",
        "__title__": "flext_observability.__version__",
        "__url__": "flext_observability.__version__",
        "__version__": "flext_observability.__version__",
        "__version_info__": "flext_observability.__version__",
        "_utilities": "flext_observability._utilities",
        "advanced_context": "flext_observability.advanced_context",
        "c": ("flext_observability.constants", "FlextObservabilityConstants"),
        "constants": "flext_observability.constants",
        "context": "flext_observability.context",
        "core": "flext_observability.core",
        "custom_metrics": "flext_observability.custom_metrics",
        "d": "flext_core",
        "e": "flext_core",
        "error_handling": "flext_observability.error_handling",
        "fields": "flext_observability.fields",
        "flext_monitor_function": "flext_observability.monitoring",
        "h": "flext_core",
        "health": "flext_observability.health",
        "http_client_instrumentation": "flext_observability.http_client_instrumentation",
        "http_instrumentation": "flext_observability.http_instrumentation",
        "logging_integration": "flext_observability.logging_integration",
        "m": ("flext_observability.models", "FlextObservabilityModels"),
        "models": "flext_observability.models",
        "monitoring": "flext_observability.monitoring",
        "observability_logging": "flext_observability.observability_logging",
        "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
        "performance": "flext_observability.performance",
        "protocols": "flext_observability.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "sampling": "flext_observability.sampling",
        "services": "flext_observability.services",
        "settings": "flext_observability.settings",
        "t": ("flext_observability.typings", "FlextObservabilityTypes"),
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
        "utilities": "flext_observability.utilities",
        "x": "flext_core",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
