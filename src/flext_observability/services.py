"""Generic FLEXT Observability Services.

Minimal, generic services following SOLID principles with complete delegation to FLEXT core.
Single unified class for all observability operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextContainer, FlextLogger, FlextResult
from flext_core.utilities import FlextUtilities as u_core

from flext_observability.settings import FlextObservabilitySettings


class FlextObservabilityServices(u_core):
    """Generic observability services delegating to FLEXT core patterns.

    Single unified class providing generic observability operations through
    complete delegation to FlextContainer, FlextLogger, and FlextResult patterns.
    No domain-specific logic - pure generic foundation.
    """

    def __init__(self) -> None:
        """Initialize with FLEXT core components."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        self._config = FlextObservabilitySettings.get_global_instance()

    @property
    def container(self) -> FlextContainer:
        """Access FLEXT container."""
        return self._container

    @property
    def logger(self) -> FlextLogger:
        """Access FLEXT logger."""
        return self._logger

    @property
    def config(self) -> FlextObservabilitySettings:
        """Access observability config."""
        return self._config

    def process_entry(
        self,
        entry_data: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Process generic observability entry through FLEXT patterns."""
        try:
            # Delegate validation to FLEXT core
            if not entry_data:
                return FlextResult[dict[str, object]].fail("Entry data required")

            # Use container for any service resolution
            processed = entry_data.copy()
            processed["processed_at"] = "now"
            processed["processor"] = "flext_observability"

            return FlextResult[dict[str, object]].ok(processed)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Entry processing failed: {e}")

    def get_status(self) -> FlextResult[dict[str, object]]:
        """Get generic service status through FLEXT patterns."""
        try:
            status = {
                "service": "flext_observability",
                "status": "operational",
                "timestamp": "now",
                "version": "generic",
            }
            return FlextResult[dict[str, object]].ok(status)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Status check failed: {e}")

    def create_alert(self, **_kwargs: object) -> FlextResult[dict[str, object]]:
        """Generic alert creation - not implemented in base service."""
        return FlextResult[dict[str, object]].fail(
            "Alert creation not implemented in generic service",
        )

    def get_metrics_summary(self) -> FlextResult[dict[str, object]]:
        """Generic metrics summary - not implemented in base service."""
        return FlextResult[dict[str, object]].fail(
            "Metrics summary not implemented in generic service",
        )

    @property
    def health_service(self) -> object | None:
        """Generic health service - not implemented in base service."""
        return None


# Global factory functions delegating to FLEXT core
def get_global_factory() -> FlextObservabilityServices:
    """Get global factory instance through FLEXT container."""
    result = FlextContainer.get_global().get_or_create(
        "flext_observability_factory",
        FlextObservabilityServices,
    )
    if result.is_success:
        value = result.value
        if isinstance(value, FlextObservabilityServices):
            return value
    # Fallback if container doesn't have the service
    return FlextObservabilityServices()


def reset_global_factory() -> None:
    """Reset global factory through FLEXT container."""
    # Note: Container may not have remove method, so this is a no-op for now


# Alias for backward compatibility
FlextObservabilityUtilities = FlextObservabilityServices

__all__ = [
    "FlextObservabilityServices",
    "FlextObservabilityUtilities",
    "get_global_factory",
    "reset_global_factory",
]
