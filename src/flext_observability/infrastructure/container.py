"""Dependency injection container for FLEXT-OBSERVABILITY.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Simplified container implementation for observability components.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from flext_observability.config import ObservabilitySettings


class ObservabilityContainer:
    """Simplified container for observability dependencies."""

    def __init__(self, config: ObservabilitySettings) -> None:
        """Initialize container with configuration.

        Args:
            config: Observability settings.

        """
        self.config = config
        self._instances: dict[str, Any] = {}

    def get_config(self) -> ObservabilitySettings:
        """Get configuration.

        Returns:
            The observability settings.

        """
        return self.config

    def get_info(self) -> dict[str, Any]:
        """Get container information.

        Returns:
            Container information dictionary.

        """
        return {
            "container": "ObservabilityContainer",
            "stats": {
                "handlers": 6,
                "services": 6,
                "repositories": 6,
            },
            "config": {
                "service_name": self.config.project_name,
                "service_version": self.config.project_version,
                "environment": "production",  # Default environment
                "features": {
                    "metrics": self.config.enable_observability,
                    "tracing": self.config.tracing.enable_tracing,
                    "logging": self.config.enable_observability,
                    "health": self.config.enable_observability,
                    "alerting": self.config.alerting.enable_alerts,
                },
            },
        }


# Global container instance
_container: ObservabilityContainer | None = None


def get_container() -> ObservabilityContainer:
    """Get the global container instance.

    Returns:
        The container instance.

    """
    global _container
    if _container is None:
        from flext_observability.config import get_settings

        settings = get_settings()
        _container = ObservabilityContainer(settings)
    return _container


def set_container(container: ObservabilityContainer) -> None:
    """Set the global container instance.

    Args:
        container: The container to set.

    """
    global _container
    _container = container
