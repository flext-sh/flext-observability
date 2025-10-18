"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.factories import FlextObservabilityFactories


# Generic factory functions - all observability creation goes through these
def flext_create_entry(
    name: str,
    entry_type: str,
    data: dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
) -> FlextResult[FlextObservabilityEntry]:
    """Create generic observability entry - all creation goes through this."""
    return FlextObservabilityFactories.create_entry(name, entry_type, data, metadata)


from flext_observability.fields import (
    FlextObservabilityFields,
)
from flext_observability.models import (
    FlextObservabilityModels,
)
from flext_observability.monitoring import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)
from flext_observability.services import (
    FlextObservabilityServices,
    get_global_factory,
    reset_global_factory,
)
from flext_observability.typings import (
    FlextObservabilityTypes,
)

# Generic model exports
FlextObservabilityEntry = FlextObservabilityModels.GenericObservabilityEntry
FlextObservabilityConfig = FlextObservabilityModels.GenericObservabilityConfig

# Removed over-engineered FlextObservability facade class - not used anywhere in flext ecosystem

__all__ = [
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityEntry",
    "FlextObservabilityFactories",
    "FlextObservabilityFields",
    "FlextObservabilityMasterFactory",
    "FlextObservabilityModels",
    "FlextObservabilityMonitor",
    "FlextObservabilityServices",
    "FlextObservabilityTypes",
    "__version__",
    "__version_info__",
    "flext_create_entry",
    "flext_monitor_function",
    "get_global_factory",
    "reset_global_factory",
]
