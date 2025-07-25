"""Health monitoring components for flext-infrastructure.monitoring.flext-observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides health checking functionality following clean architecture.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

import psutil
from flext_core import get_logger

logger = get_logger(__name__)


class HealthStatus(Enum):
    """Health status enumeration for system components."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class ComponentHealth:
    """Represents the health status of a system component."""

    def __init__(
        self,
        name: str,
        status: HealthStatus,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize component health.

        Args:
            name: Component name.
            status: Health status.
            details: Additional health details.

        """
        self.name = name
        self.status = status
        self.details = details or {}

    @classmethod
    def healthy(
        cls,
        name: str,
        details: dict[str, Any] | None = None,
    ) -> ComponentHealth:
        """Create a healthy component health status.

        Args:
            name: Component name.
            details: Additional health details.

        Returns:
            ComponentHealth instance with healthy status.

        """
        return cls(name, HealthStatus.HEALTHY, details)

    @classmethod
    def unhealthy(
        cls,
        name: str,
        details: dict[str, Any] | None = None,
    ) -> ComponentHealth:
        """Create an unhealthy component health status.

        Args:
            name: Component name.
            details: Additional health details.

        Returns:
            ComponentHealth instance with unhealthy status.

        """
        return cls(name, HealthStatus.UNHEALTHY, details)

    def __str__(self) -> str:
        """Return string representation of component health."""
        return f"ComponentHealth(name={self.name}, status={self.status.value.upper()})"


class HealthChecker:
    """Health checker for FLEXT services."""

    def __init__(self) -> None:
        """Initialize health checker."""
        self.start_time = datetime.now(UTC)
        self.checks: list[dict[str, Any]] = []

    async def check_system_health(self) -> dict[str, Any]:
        """Check system health status.

        Returns:
            Health status dictionary

        """
        # Basic system health checks

        try:
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                return False

            # Check memory usage
            memory = psutil.virtual_memory()
            memory_ok = not memory.percent > 90
        except Exception:
            return False
        else:
            return memory_ok

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for health check.

        Returns:
            ISO formatted timestamp.

        """
        return datetime.now(UTC).isoformat()

    def register_component(self, component: ComponentHealth) -> None:
        """Register a component for health monitoring.

        Args:
            component: Component health to register.

        """
        try:
            self._components[component.name] = component
        except Exception:
            logger.exception(f"Failed to register component {component.name}")
        else:
            logger.info(f"Registered component: {component.name}")


__all__ = [
    "ComponentHealth",
    "HealthChecker",
    "HealthStatus",
]
