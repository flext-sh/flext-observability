"""FLEXT Observability Platform - Simplified using factory patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform simplificada usando factory patterns do flext-core.
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.constants import (
    DEFAULT_OBSERVABILITY_CONFIG,
    ObservabilityConstants,
)
from flext_observability.factory import FlextObservabilityMasterFactory


class FlextObservabilityPlatformV2:
    """Simplified observability platform using factory patterns."""

    def __init__(
        self,
        config: dict[str, object] | None = None,
        container: FlextContainer | None = None,
    ) -> None:
        """Initialize simplified platform."""
        merged_config = {**DEFAULT_OBSERVABILITY_CONFIG, **(config or {})}

        self.name = ObservabilityConstants.NAME
        self.version = ObservabilityConstants.VERSION
        self.config = merged_config
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

        # Use factory for all operations
        self._factory = FlextObservabilityMasterFactory(self.container)

    def metric(
        self,
        name: str,
        value: float,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create metric using factory."""
        return self._factory.metric(name, value, **kwargs)

    def log(
        self,
        message: str,
        level: str = "info",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create log entry using factory."""
        return self._factory.log(message, level, **kwargs)

    def alert(
        self,
        title: str,
        message: str,
        severity: str = "low",
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create alert using factory."""
        return self._factory.alert(title, message, severity, **kwargs)

    def trace(
        self,
        trace_id: str,
        operation: str,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Create trace using factory."""
        return self._factory.trace(trace_id, operation, **kwargs)

    def health_check(self) -> FlextResult[dict[str, object]]:
        """Get health status using factory."""
        return self._factory.health_status()


def create_simplified_observability_platform(
    config: dict[str, object] | None = None,
    container: FlextContainer | None = None,
) -> FlextObservabilityPlatformV2:
    """Create simplified observability platform."""
    return FlextObservabilityPlatformV2(config=config, container=container)


# Compatibility alias
FlextObservabilityPlatformSimplified = FlextObservabilityPlatformV2
