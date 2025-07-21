"""Health monitoring components for flext-infrastructure.monitoring.flext-observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides health checking functionality following clean architecture.
"""

from __future__ import annotations

from typing import Any

from flext_observability.domain.value_objects import HealthStatus


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
        """String representation of component health."""
        return f"ComponentHealth(name={self.name}, status={self.status.value.upper()})"


class HealthChecker:
    """Health checker implementation using clean architecture."""

    def __init__(self) -> None:
        """Initialize health checker."""
        self._components: dict[str, ComponentHealth] = {}

    async def check_health(self) -> dict[str, Any]:
        """Perform comprehensive health check.

        Returns:
            Health status dictionary.

        """
        try:
            # Perform system health check
            system_health = await self._check_system_health()

            return {
                "status": "healthy" if system_health else "unhealthy",
                "timestamp": self._get_current_timestamp(),
                "components": list(self._components.values()),
                "system": system_health,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": self._get_current_timestamp(),
            }

    async def _check_system_health(self) -> bool:
        """Check overall system health.

        Returns:
            True if system is healthy, False otherwise.

        """
        # Basic system health checks
        import psutil

        try:
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                return False

            # Check memory usage
            memory = psutil.virtual_memory()
            return not memory.percent > 90
        except Exception:
            return False

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for health check.

        Returns:
            ISO formatted timestamp.

        """
        from datetime import UTC, datetime

        return datetime.now(UTC).isoformat()

    def register_component(self, component: ComponentHealth) -> None:
        """Register a component for health monitoring.

        Args:
            component: Component health to register.

        """
        self._components[component.name] = component


__all__ = [
    "ComponentHealth",
    "HealthChecker",
    "HealthStatus",
]
