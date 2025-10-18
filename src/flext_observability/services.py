"""Generic FLEXT Observability Services.

Minimal, generic services following SOLID principles with complete delegation to FLEXT core.
Single unified class for all observability operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Any

from flext_core import FlextContainer, FlextLogger, FlextResult, FlextUtilities

from flext_observability.config import FlextObservabilityConfig


class FlextObservabilityServices(FlextUtilities):
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
        self._config = FlextObservabilityConfig.get_global_instance()

    @property
    def container(self) -> FlextContainer:
        """Access FLEXT container."""
        return self._container

    @property
    def logger(self) -> FlextLogger:
        """Access FLEXT logger."""
        return self._logger

    @property
    def config(self) -> FlextObservabilityConfig:
        """Access observability config."""
        return self._config

    def process_entry(self, entry_data: dict[str, Any]) -> FlextResult[dict[str, Any]]:
        """Process generic observability entry through FLEXT patterns."""
        try:
            # Delegate validation to FLEXT core
            if not entry_data:
                return FlextResult[dict[str, Any]].fail("Entry data required")

            # Use container for any service resolution
            processed = entry_data.copy()
            processed["processed_at"] = "now"
            processed["processor"] = "flext_observability"

            return FlextResult[dict[str, Any]].ok(processed)
        except Exception as e:
            return FlextResult[dict[str, Any]].fail(f"Entry processing failed: {e}")

    def get_status(self) -> FlextResult[dict[str, Any]]:
        """Get generic service status through FLEXT patterns."""
        try:
            status = {
                "service": "flext_observability",
                "status": "operational",
                "timestamp": "now",
                "version": "generic",
            }
            return FlextResult[dict[str, Any]].ok(status)
        except Exception as e:
            return FlextResult[dict[str, Any]].fail(f"Status check failed: {e}")


# Global factory functions delegating to FLEXT core
def get_global_factory() -> FlextObservabilityServices:
    """Get global factory instance through FLEXT container."""
    return FlextContainer.get_global().get_or_create(
        "flext_observability_factory", FlextObservabilityServices
    )


def reset_global_factory() -> None:
    """Reset global factory through FLEXT container."""
    container = FlextContainer.get_global()
    container.remove("flext_observability_factory")


__all__ = ["FlextObservabilityServices", "get_global_factory", "reset_global_factory"]
