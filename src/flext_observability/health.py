"""FLEXT Observability Health Checker.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple health checker for testing purposes.
"""

from __future__ import annotations

from flext_core import get_logger


class HealthChecker:
    """Simple health checker for testing purposes."""

    def __init__(self) -> None:
        """Initialize the health checker."""
        self.logger = get_logger(self.__class__.__name__)

    def check_health(self) -> dict[str, str]:
        """Check basic health status."""
        return {
            "status": "healthy",
            "service": "flext-observability",
            "version": "0.9.0",
        }
