"""FLEXT Observability Metrics - Temporary implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Temporary implementation for metrics collection.
"""

from __future__ import annotations


class MetricsCollector:
    """Temporary metrics collector for testing."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize metrics collector."""
        self.config = config or {}

    def collect_metrics(self) -> dict[str, object]:
        """Collect metrics data."""
        return {
            "timestamp": "2025-01-01T00:00:00Z",
            "metrics": [],
            "config": self.config,
        }
