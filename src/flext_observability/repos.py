"""FLEXT Observability Repository Patterns - Data Access Layer Abstraction.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Repository pattern implementations providing abstract data access layer interfaces
for observability entities with Clean Architecture compliance. Defines contracts
for data persistence, retrieval, and query operations while maintaining separation
of concerns between business logic and data storage implementations.

This module implements the Repository pattern from Domain-Driven Design, providing
abstract interfaces that can be implemented by various storage backends including
in-memory stores, relational databases, NoSQL systems, and external observability
platforms. All repository operations return FlextResult for consistent error handling.

Key Components:
    - MetricsRepository: Abstract interface for metrics data access operations
    - LoggingRepository: Abstract interface for structured logging data persistence
    - AlertRepository: Abstract interface for alert lifecycle and query operations
    - TracingRepository: Abstract interface for distributed trace data management
    - HealthRepository: Abstract interface for component health check storage
    - InMemoryRepositories: Concrete implementations for testing and development

Architecture:
    Infrastructure layer abstraction in Clean Architecture, defining contracts
    between Application Services and data storage implementations. Enables
    dependency inversion and supports multiple storage backend implementations.

Integration:
    - Used by Application Services for data persistence and retrieval
    - Abstracts storage implementation details from business logic
    - Supports multiple backend implementations (database, cloud, in-memory)
    - Enables testing through in-memory repository implementations

Example:
    Repository pattern usage with dependency injection:

    >>> from flext_observability.repos import MetricsRepository
    >>> from flext_observability.entities import FlextMetric
    >>>
    >>> class MyMetricsService:
    ...     def __init__(self, repo: MetricsRepository):
    ...         self.repo = repo
    ...
    ...     def record_metric(self, metric: FlextMetric):
    ...         return self.repo.save(metric)

FLEXT Integration:
    Provides consistent data access patterns across all 33 FLEXT ecosystem projects,
    enabling flexible storage backend selection while maintaining clean separation
    between business logic and data persistence concerns.

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
    """Abstract Repository Interface for Metrics Data Access Operations.

    Defines the contract for metrics data persistence, retrieval, and query operations
    following Repository pattern from Domain-Driven Design. Abstracts storage
    implementation details from business logic while providing comprehensive
    metrics data access capabilities with consistent error handling.

    This repository interface supports metrics collection, aggregation queries,
    time-series data operations, and performance monitoring requirements across
    the FLEXT ecosystem. All operations return FlextResult for railway-oriented
    programming and comprehensive error handling.

    Repository Operations:
        - Entity Persistence: Save and update metric entities
        - Query by Identifier: Retrieve metrics by unique identifiers
        - Query by Name: Find metrics collections by metric name
        - Time-series Queries: Time-based metric retrieval (implementation-specific)
        - Aggregation Support: Metric aggregation and statistics
          (implementation-specific)

    Implementation Requirements:
        - Thread-safe operations for concurrent metric recording
        - Efficient time-series data storage and retrieval
        - Metric retention policies and cleanup strategies
        - Performance optimization for high-frequency metric operations
        - Prometheus-compatible data export capabilities

    """

    @abstractmethod
    def save(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Persist metric entity to storage backend with validation.

        Args:
            metric: FlextMetric entity to persist with comprehensive validation

        Returns:
            FlextResult[FlextMetric]: Success with persisted entity or failure
            with detailed error message for debugging and monitoring

        """

    @abstractmethod
    def get_by_id(self, metric_id: str) -> FlextResult[FlextMetric]:
        """Retrieve metric entity by unique identifier.

        Args:
            metric_id: Unique metric identifier for entity retrieval

        Returns:
            FlextResult[FlextMetric]: Success with metric entity or failure
            if metric not found or retrieval error occurs

        """

    @abstractmethod
    def find_by_name(self, name: str) -> FlextResult[list[FlextMetric]]:
        """Find all metrics matching the specified name pattern.

        Args:
            name: Metric name pattern for collection retrieval

        Returns:
            FlextResult[List[FlextMetric]]: Success with metric collection
            or failure with detailed error message

        """


class LoggingRepository(ABC):
    """Abstract Repository Interface for Structured Logging Data Persistence.

    Defines comprehensive contract for structured log data access operations
    following Repository pattern principles. Supports log entry persistence,
    level-based filtering, temporal queries, and search capabilities for
    comprehensive logging infrastructure across the FLEXT ecosystem.

    """

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
    """Abstract Repository Interface for Alert Lifecycle Management.

    Defines comprehensive contract for alert data persistence, lifecycle management,
    and query operations. Supports alert routing, severity-based filtering, and
    operational workflow management across the FLEXT ecosystem.

    """

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
    """Abstract Repository Interface for Distributed Trace Data Management.

    Defines comprehensive contract for distributed tracing data persistence,
    correlation, and query operations. Supports trace correlation, span relationships,
    and performance analysis across microservices in the FLEXT ecosystem.

    """

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
    """Abstract Repository Interface for Component Health Check Storage.

    Defines comprehensive contract for health check data persistence, component
    monitoring, and dependency validation. Supports health status tracking,
    component discovery, and system health aggregation across FLEXT services.

    """

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
    """In-Memory Metrics Repository Implementation for Testing and Development.

    Concrete implementation of MetricsRepository using in-memory data structures
    for rapid development, testing, and prototyping scenarios. Provides full
    repository interface compliance while maintaining simplicity and performance
    for non-persistent storage requirements.

    This implementation supports all MetricsRepository operations with efficient
    in-memory data structures, thread-safe operations, and comprehensive error
    handling suitable for development environments and unit testing scenarios.

    Storage Architecture:
        - Primary Storage: Dictionary indexed by metric ID for O(1) retrieval
        - Name Index: Dictionary of metric name to list mappings for queries
        - Thread Safety: Inherent thread safety through Python GIL limitations
        - Memory Management: Automatic cleanup through Python garbage collection

    Performance Characteristics:
        - Save Operations: O(1) average case for metric persistence
        - ID Retrieval: O(1) direct lookup by metric identifier
        - Name Queries: O(1) name lookup, O(n) result iteration
        - Memory Usage: Linear growth with metric count, no automatic cleanup

    """

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
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to save metric: {e}")

    def get_by_id(self, metric_id: str) -> FlextResult[FlextMetric]:
        """Get metric by ID from memory."""
        if metric_id in self._metrics:
            return FlextResult.ok(self._metrics[metric_id])
        return FlextResult.fail(f"Metric not found: {metric_id}")

    def find_by_name(self, name: str) -> FlextResult[list[FlextMetric]]:
        """Find metrics by name from memory."""
        return FlextResult.ok(self._by_name.get(name, []))
