"""Infrastructure Repositories - Data access using flext-core patterns.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Infrastructure Layer
Following SOLID, KISS, DRY principles using flext-core FlextResult.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_observability.domain.entities import (
        Alert,
        HealthCheck,
        LogEntry,
        Metric,
        Trace,
    )


class MetricsRepository(ABC):
    """Abstract metrics repository - Interface Segregation."""

    @abstractmethod
    def save(self, metric: Metric) -> FlextResult[Metric]:
        """Save metric."""

    @abstractmethod
    def get_by_id(self, metric_id: str) -> FlextResult[Metric]:
        """Get metric by ID."""


class LoggingRepository(ABC):
    """Abstract logging repository - Interface Segregation."""

    @abstractmethod
    def save(self, entry: LogEntry) -> FlextResult[LogEntry]:
        """Save log entry."""

    @abstractmethod
    def find_by_level(self, level: str | None) -> FlextResult[list[LogEntry]]:
        """Find logs by level."""


class TracingRepository(ABC):
    """Abstract tracing repository - Interface Segregation."""

    @abstractmethod
    def save(self, trace: Trace) -> FlextResult[Trace]:
        """Save trace."""

    @abstractmethod
    def get_by_id(self, trace_id: str) -> FlextResult[Trace]:
        """Get trace by ID."""


class AlertRepository(ABC):
    """Abstract alert repository - Interface Segregation."""

    @abstractmethod
    def save(self, alert: Alert) -> FlextResult[Alert]:
        """Save alert."""


class HealthRepository(ABC):
    """Abstract health repository - Interface Segregation."""

    @abstractmethod
    def get_by_component(self, component: str) -> FlextResult[HealthCheck]:
        """Get health check by component."""

    @abstractmethod
    def get_all(self) -> FlextResult[list[HealthCheck]]:
        """Get all health checks."""


# Simple in-memory implementations for development
class InMemoryMetricsRepository(MetricsRepository):
    """In-memory metrics repository - Simple implementation."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: dict[str, Metric] = {}

    def save(self, metric: Metric) -> FlextResult[Metric]:
        """Save metric to memory."""
        self._storage[metric.id] = metric
        return FlextResult.ok(metric)

    def get_by_id(self, metric_id: str) -> FlextResult[Metric]:
        """Get metric from memory."""
        if metric_id not in self._storage:
            return FlextResult.fail(f"Metric {metric_id} not found")
        return FlextResult.ok(self._storage[metric_id])


class InMemoryLoggingRepository(LoggingRepository):
    """In-memory logging repository - Simple implementation."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: list[LogEntry] = []

    def save(self, entry: LogEntry) -> FlextResult[LogEntry]:
        """Save log entry to memory."""
        self._storage.append(entry)
        return FlextResult.ok(entry)

    def find_by_level(self, level: str | None) -> FlextResult[list[LogEntry]]:
        """Find logs by level from memory."""
        if level is None:
            return FlextResult.ok(self._storage.copy())

        filtered = [entry for entry in self._storage if entry.level == level]
        return FlextResult.ok(filtered)
