"""Enterprise observability and monitoring library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult

from flext_observability.__version__ import __version__, __version_info__
from flext_observability.config import FlextObservabilityConfig
from flext_observability.constants import FlextObservabilityConstants
from flext_observability.models import FlextObservabilityModels
from flext_observability.monitoring import flext_monitor_function
from flext_observability.services import (
    FlextObservabilityServices,
    FlextObservabilityUtilities,
)

# Single generic entry for all observability types
FlextObservabilityEntry = FlextObservabilityModels.GenericObservabilityEntry


# Generic factory function - all observability creation goes through this
def flext_create_entry(
    name: str,
    entry_type: str,
    data: dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
) -> FlextResult[FlextObservabilityEntry]:
    """Create generic observability entry - all creation goes through this."""
    try:
        if not name or not isinstance(name, str):
            return FlextResult[FlextObservabilityEntry].fail(
                "Entry name must be non-empty string"
            )
        if not entry_type or not isinstance(entry_type, str):
            return FlextResult[FlextObservabilityEntry].fail(
                "Entry type must be non-empty string"
            )

        entry = FlextObservabilityEntry(
            name=name.strip(),
            type=entry_type.strip(),
            data=data or {},
            metadata=metadata or {},
        )
        return FlextResult[FlextObservabilityEntry].ok(entry)
    except Exception as e:
        return FlextResult[FlextObservabilityEntry].fail(f"Entry creation failed: {e}")


__all__ = [
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityEntry",
    "FlextObservabilityServices",
    "FlextObservabilityUtilities",
    "__version__",
    "__version_info__",
    "flext_create_entry",
    "flext_monitor_function",
]
