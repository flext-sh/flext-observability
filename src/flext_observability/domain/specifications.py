"""Domain specifications for observability - business rules and validation.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from flext_core.domain.types import AlertSeverity, LogLevel, MetricType, TraceStatus

from flext_observability.domain.entities import (
    Alert,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)

T = TypeVar("T")


class Specification[T](ABC):
    """Base specification class for domain rules."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the candidate satisfies this specification."""

    def and_(self, other: Specification[T]) -> Specification[T]:
        """Create an AND specification."""
        return AndSpecification(self, other)

    def or_(self, other: Specification[T]) -> Specification[T]:
        """Create an OR specification."""
        return OrSpecification(self, other)

    def not_(self) -> Specification[T]:
        """Create a NOT specification."""
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    """AND combination of two specifications."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if both specifications are satisfied."""
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(
            candidate,
        )


class OrSpecification(Specification[T]):
    """OR combination of two specifications."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if either specification is satisfied."""
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(
            candidate,
        )


class NotSpecification(Specification[T]):
    """NOT negation of a specification."""

    def __init__(self, spec: Specification[T]) -> None:
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the specification is NOT satisfied."""
        return not self.spec.is_satisfied_by(candidate)


# Alert-specific specifications
class AlertThresholdSpec(Specification[Alert]):
    """Specification for alert threshold validation."""

    def __init__(self, min_threshold: float, max_threshold: float) -> None:
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def is_satisfied_by(self, candidate: Alert) -> bool:
        """Check if alert threshold is within valid range."""
        if candidate.threshold is None:
            return False
        return self.min_threshold <= candidate.threshold <= self.max_threshold


class AlertSeveritySpec(Specification[Alert]):
    """Specification for alert severity validation."""

    def __init__(self, allowed_severities: list[AlertSeverity]) -> None:
        self.allowed_severities = allowed_severities

    def is_satisfied_by(self, candidate: Alert) -> bool:
        """Check if alert severity is allowed."""
        return candidate.severity in self.allowed_severities


# Metric-specific specifications
class MetricValueRangeSpec(Specification[Metric]):
    """Specification for metric value range validation."""

    def __init__(self, min_value: float, max_value: float) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def is_satisfied_by(self, candidate: Metric) -> bool:
        """Check if metric value is within valid range."""
        return self.min_value <= candidate.value <= self.max_value


class MetricTypeSpec(Specification[Metric]):
    """Specification for metric type validation."""

    def __init__(self, allowed_types: list[MetricType]) -> None:
        self.allowed_types = allowed_types

    def is_satisfied_by(self, candidate: Metric) -> bool:
        """Check if metric type is allowed."""
        return candidate.metric_type in self.allowed_types


# Log-specific specifications
class LogLevelSpec(Specification[LogEntry]):
    """Specification for log level validation."""

    def __init__(self, min_level: LogLevel) -> None:
        self.min_level = min_level

    def is_satisfied_by(self, candidate: LogEntry) -> bool:
        """Check if log level meets minimum requirement."""
        # Simple level comparison - in reality you'd have proper level ordering
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4,
        }
        return level_order.get(candidate.level, 0) >= level_order.get(self.min_level, 0)


class ErrorLogSpec(Specification[LogEntry]):
    """Specification for error log detection."""

    def is_satisfied_by(self, candidate: LogEntry) -> bool:
        """Check if log entry represents an error."""
        return candidate.is_error


# Trace-specific specifications
class TraceCompletionSpec(Specification[Trace]):
    """Specification for trace completion validation."""

    def is_satisfied_by(self, candidate: Trace) -> bool:
        """Check if trace is completed."""
        return candidate.trace_status == TraceStatus.COMPLETED


class TraceDurationSpec(Specification[Trace]):
    """Specification for trace duration validation."""

    def __init__(self, max_duration_ms: float) -> None:
        self.max_duration_ms = max_duration_ms

    def is_satisfied_by(self, candidate: Trace) -> bool:
        """Check if trace duration is within acceptable range."""
        if candidate.duration_ms is None:
            return False
        return candidate.duration_ms <= self.max_duration_ms


# Health check specifications
class HealthyComponentSpec(Specification[HealthCheck]):
    """Specification for healthy component validation."""

    def is_satisfied_by(self, candidate: HealthCheck) -> bool:
        """Check if component is healthy."""
        return candidate.is_healthy


class ComponentResponseTimeSpec(Specification[HealthCheck]):
    """Specification for component response time validation."""

    def __init__(self, max_response_time_ms: float) -> None:
        self.max_response_time_ms = max_response_time_ms

    def is_satisfied_by(self, candidate: HealthCheck) -> bool:
        """Check if component response time is acceptable."""
        if candidate.response_time_ms is None:
            return False
        return candidate.response_time_ms <= self.max_response_time_ms


__all__ = [
    "AlertSeveritySpec",
    "AlertThresholdSpec",
    "AndSpecification",
    "ComponentResponseTimeSpec",
    "ErrorLogSpec",
    "HealthyComponentSpec",
    "LogLevelSpec",
    "MetricTypeSpec",
    "MetricValueRangeSpec",
    "NotSpecification",
    "OrSpecification",
    "Specification",
    "TraceCompletionSpec",
    "TraceDurationSpec",
]
