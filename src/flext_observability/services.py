"""Generic FLEXT Observability Services.

Minimal, generic services following SOLID principles with complete delegation to FLEXT core.
Single unified class for all observability operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextContainer, FlextResult, FlextRuntime
from flext_core.utilities import u

from flext_observability.settings import FlextObservabilitySettings
from flext_observability.typings import t


class FlextObservabilityServices(u):
    """Generic observability services delegating to FLEXT core patterns.

    Single unified class providing generic observability operations through
    complete delegation to FlextContainer, FlextLogger, and FlextResult patterns.
    No domain-specific logic - pure generic foundation.
    """

    def __init__(self) -> None:
        """Initialize with FLEXT core components."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextRuntime.get_logger(__name__)
        self._config = FlextObservabilitySettings.get_global_instance()

    @property
    def container(self) -> FlextContainer:
        """Access FLEXT container."""
        return self._container

    @property
    def logger(self) -> object:
        """Access FLEXT logger."""
        return self._logger

    @property
    def config(self) -> FlextObservabilitySettings:
        """Access observability config."""
        return self._config

    def process_entry(
        self,
        entry_data: t.Dict,
    ) -> FlextResult[t.Dict]:
        """Process generic observability entry through FLEXT patterns."""
        try:
            # Delegate validation to FLEXT core
            if not entry_data:
                return FlextResult[t.Dict].fail("Entry data required")

            # Use container for any service resolution
            processed = t.Dict.model_validate(dict(entry_data.items()))
            processed["processed_at"] = "now"
            processed["processor"] = "flext_observability"

            return FlextResult[t.Dict].ok(processed)
        except Exception as e:
            return FlextResult[t.Dict].fail(f"Entry processing failed: {e}")

    def get_status(self) -> FlextResult[t.Dict]:
        """Get generic service status through FLEXT patterns."""
        try:
            status = {
                "service": "flext_observability",
                "status": "operational",
                "timestamp": "now",
                "version": "generic",
            }
            status_result = t.Dict.model_validate(
                {
                    "service": status["service"],
                    "status": status["status"],
                    "timestamp": status["timestamp"],
                    "version": status["version"],
                },
            )
            return FlextResult[t.Dict].ok(status_result)
        except Exception as e:
            return FlextResult[t.Dict].fail(f"Status check failed: {e}")

    def create_alert(self, **_kwargs: object) -> FlextResult[t.Dict]:
        """Generic alert creation - not implemented in base service."""
        return FlextResult[t.Dict].fail(
            "Alert creation not implemented in generic service",
        )

    def get_metrics_summary(self) -> FlextResult[t.Dict]:
        """Generic metrics summary - not implemented in base service."""
        return FlextResult[t.Dict].fail(
            "Metrics summary not implemented in generic service",
        )

    @property
    def health_service(self) -> object | None:
        """Generic health service - not implemented in base service."""
        return None


# Global factory functions delegating to FLEXT core
def get_global_factory() -> FlextObservabilityServices:
    """Get global factory instance."""
    # For now, return new instance directly - container registration
    # would require protocol implementation
    return FlextObservabilityServices()


def reset_global_factory() -> None:
    """Reset global factory through FLEXT container."""
    # Note: Container may not have remove method, so this is a no-op for now


__all__ = [
    "FlextObservabilityServices",
    "get_global_factory",
    "reset_global_factory",
]
