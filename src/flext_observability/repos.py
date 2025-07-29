"""FLEXT Observability Repositories - Abstract interfaces using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Repository interfaces recovered and simplified using flext-core patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_observability.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )

# ============================================================================
# REPOSITORY INTERFACES - Using flext-core patterns
# ============================================================================


class MetricsRepository(ABC):
    """Abstract metrics repository using flext-core patterns."""

    @abstractmethod
    def save(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Save metric."""

    @abstractmethod
    def get_by_id(self, metric_id: str) -> FlextResult[FlextMetric]:
        """Get metric by ID."""

    @abstractmethod
    def find_by_name(self, name: str) -> FlextResult[list[FlextMetric]]:
        """Find metrics by name."""


class LoggingRepository(ABC):
    """Abstract logging repository using flext-core patterns."""

    @abstractmethod
    def save(self, entry: FlextLogEntry) -> FlextResult[FlextLogEntry]:
        """Save log entry."""

    @abstractmethod
    def find_by_level(self, level: str) -> FlextResult[list[FlextLogEntry]]:
        """Find logs by level."""

    @abstractmethod
    def get_recent(self, limit: int = 100) -> FlextResult[list[FlextLogEntry]]:
        """Get recent log entries."""


class AlertRepository(ABC):
    """Abstract alert repository using flext-core patterns."""

    @abstractmethod
    def save(self, alert: FlextAlert) -> FlextResult[FlextAlert]:
        """Save alert."""

    @abstractmethod
    def get_by_id(self, alert_id: str) -> FlextResult[FlextAlert]:
        """Get alert by ID."""

    @abstractmethod
    def find_active(self) -> FlextResult[list[FlextAlert]]:
        """Find active alerts."""

    @abstractmethod
    def find_by_severity(self, severity: str) -> FlextResult[list[FlextAlert]]:
        """Find alerts by severity."""


class TracingRepository(ABC):
    """Abstract tracing repository using flext-core patterns."""

    @abstractmethod
    def save(self, trace: FlextTrace) -> FlextResult[FlextTrace]:
        """Save trace."""

    @abstractmethod
    def get_by_trace_id(self, trace_id: str) -> FlextResult[FlextTrace]:
        """Get trace by trace ID."""

    @abstractmethod
    def find_by_operation(self, operation: str) -> FlextResult[list[FlextTrace]]:
        """Find traces by operation."""


class HealthRepository(ABC):
    """Abstract health repository using flext-core patterns."""

    @abstractmethod
    def save(self, health: FlextHealthCheck) -> FlextResult[FlextHealthCheck]:
        """Save health check."""

    @abstractmethod
    def get_by_component(self, component: str) -> FlextResult[FlextHealthCheck]:
        """Get health by component."""

    @abstractmethod
    def get_all_components(self) -> FlextResult[list[FlextHealthCheck]]:
        """Get all component health checks."""

    @abstractmethod
    def find_unhealthy(self) -> FlextResult[list[FlextHealthCheck]]:
        """Find unhealthy components."""


# ============================================================================
# IN-MEMORY IMPLEMENTATIONS - For testing/development
# ============================================================================

class InMemoryMetricsRepository(MetricsRepository):
    """In-memory metrics repository for testing."""

    def __init__(self) -> None:
        """Initialize repository."""
        self._metrics: dict[str, FlextMetric] = {}
        self._by_name: dict[str, list[FlextMetric]] = {}

    def save(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Save metric in memory."""
        try:
            self._metrics[metric.id] = metric
            if metric.name not in self._by_name:
                self._by_name[metric.name] = []
            self._by_name[metric.name].append(metric)
            return FlextResult.ok(metric)
        except Exception as e:
            return FlextResult.error(f"Failed to save metric: {e}")

    def get_by_id(self, metric_id: str) -> FlextResult[FlextMetric]:
        """Get metric by ID from memory."""
        if metric_id in self._metrics:
            return FlextResult.ok(self._metrics[metric_id])
        return FlextResult.error(f"Metric not found: {metric_id}")

    def find_by_name(self, name: str) -> FlextResult[list[FlextMetric]]:
        """Find metrics by name from memory."""
        return FlextResult.ok(self._by_name.get(name, []))
