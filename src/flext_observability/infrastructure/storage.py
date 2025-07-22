"""Concrete storage implementations for observability domain services.

This module provides SOLID-compliant concrete implementations of storage protocols
defined in the domain layer, implementing Dependency Inversion Principle.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence


# ==============================================================================
# DEPENDENCY INVERSION PRINCIPLE: Concrete storage implementations
# ==============================================================================


class InMemoryAlertRuleStorage:
    """In-memory implementation of AlertRuleStorage protocol (DIP compliance)."""

    def __init__(self) -> None:
        """Initialize in-memory alert rule storage."""
        self._rules: dict[str, Any] = {}

    def store_rule(self, metric_name: str, threshold: Any) -> None:
        """Store alert rule for metric."""
        self._rules[metric_name] = threshold

    def get_rule(self, metric_name: str) -> Any | None:
        """Get alert rule for metric."""
        return self._rules.get(metric_name)

    def remove_rule(self, metric_name: str) -> bool:
        """Remove alert rule for metric."""
        if metric_name in self._rules:
            del self._rules[metric_name]
            return True
        return False


class InMemoryMetricHistoryStorage:
    """In-memory implementation of MetricHistoryStorage protocol (DIP compliance)."""

    def __init__(self) -> None:
        """Initialize in-memory metric history storage."""
        self._history: dict[str, list[Any]] = {}

    def store_metric(self, metric: Any) -> None:
        """Store metric in history."""
        if metric.name not in self._history:
            self._history[metric.name] = []
        self._history[metric.name].append(metric)

    def get_history(self, metric_name: str, limit: int = 100) -> Sequence[Any]:
        """Get metric history."""
        history = self._history.get(metric_name, [])
        # Keep only the most recent entries up to the limit
        if len(history) > limit:
            history = history[-limit:]
            # Update stored history to maintain limit
            self._history[metric_name] = history
        return history

    def clear_history(self, metric_name: str) -> None:
        """Clear metric history."""
        if metric_name in self._history:
            del self._history[metric_name]


class InMemoryHealthStatusStorage:
    """In-memory implementation of HealthStatusStorage protocol (DIP compliance)."""

    def __init__(self) -> None:
        """Initialize in-memory health status storage."""
        self._status: dict[str, Any] = {}

    def update_status(self, component_key: str, health_check: Any) -> Any | None:
        """Update component health status."""
        previous = self._status.get(component_key)
        self._status[component_key] = health_check
        return previous

    def get_status(self, component_key: str) -> Any | None:
        """Get component health status."""
        return self._status.get(component_key)

    def get_all_status(self) -> dict[str, Any]:
        """Get all component health statuses."""
        return self._status.copy()


class InMemoryPatternStorage:
    """In-memory implementation of PatternStorage protocol (DIP compliance)."""

    def __init__(self) -> None:
        """Initialize in-memory pattern storage."""
        self._patterns: dict[str, int] = {}

    def increment_pattern(self, pattern: str) -> None:
        """Increment pattern count."""
        self._patterns[pattern] = self._patterns.get(pattern, 0) + 1

    def get_patterns(self) -> dict[str, int]:
        """Get all patterns with counts."""
        return self._patterns.copy()

    def clear_patterns(self) -> None:
        """Clear all patterns."""
        self._patterns.clear()


class InMemoryTraceStorage:
    """In-memory implementation of TraceStorage protocol (DIP compliance)."""

    def __init__(self) -> None:
        """Initialize in-memory trace storage."""
        self._traces: dict[str, list[Any]] = {}

    def store_trace(self, operation_name: str, trace: Any) -> None:
        """Store trace in history."""
        if operation_name not in self._traces:
            self._traces[operation_name] = []
        self._traces[operation_name].append(trace)

    def get_traces(self, operation_name: str, limit: int = 1000) -> Sequence[Any]:
        """Get trace history for operation."""
        traces = self._traces.get(operation_name, [])
        # Keep only the most recent entries up to the limit
        if len(traces) > limit:
            traces = traces[-limit:]
            # Update stored traces to maintain limit
            self._traces[operation_name] = traces
        return traces

    def clear_traces(self, operation_name: str) -> None:
        """Clear trace history for operation."""
        if operation_name in self._traces:
            del self._traces[operation_name]


# ==============================================================================
# DEPENDENCY INVERSION PRINCIPLE: Redis-based storage implementations
# ==============================================================================


class RedisAlertRuleStorage:
    """Redis implementation of AlertRuleStorage protocol for production use."""

    def __init__(self, redis_client: Any, key_prefix: str = "flext:alerts") -> None:
        """Initialize Redis alert rule storage.

        Args:
            redis_client: Redis client instance
            key_prefix: Prefix for Redis keys

        """
        self._redis = redis_client
        self._key_prefix = key_prefix

    def store_rule(self, metric_name: str, threshold: Any) -> None:
        """Store alert rule for metric in Redis."""
        key = f"{self._key_prefix}:rules:{metric_name}"
        # Serialize threshold object - would need proper serialization in production
        self._redis.set(key, str(threshold))

    def get_rule(self, metric_name: str) -> Any | None:
        """Get alert rule for metric from Redis."""
        key = f"{self._key_prefix}:rules:{metric_name}"
        rule = self._redis.get(key)
        return rule.decode() if rule else None

    def remove_rule(self, metric_name: str) -> bool:
        """Remove alert rule for metric from Redis."""
        key = f"{self._key_prefix}:rules:{metric_name}"
        return bool(self._redis.delete(key))


class RedisMetricHistoryStorage:
    """Redis implementation of MetricHistoryStorage protocol for production use."""

    def __init__(self, redis_client: Any, key_prefix: str = "flext:metrics") -> None:
        """Initialize Redis metric history storage.

        Args:
            redis_client: Redis client instance
            key_prefix: Prefix for Redis keys

        """
        self._redis = redis_client
        self._key_prefix = key_prefix

    def store_metric(self, metric: Any) -> None:
        """Store metric in Redis list."""
        key = f"{self._key_prefix}:history:{metric.name}"
        # Serialize metric object - would need proper serialization in production
        self._redis.lpush(key, str(metric))

    def get_history(self, metric_name: str, limit: int = 100) -> Sequence[Any]:
        """Get metric history from Redis."""
        key = f"{self._key_prefix}:history:{metric_name}"
        # Get most recent entries (Redis list is newest first)
        raw_history = self._redis.lrange(key, 0, limit - 1)
        # Would need proper deserialization in production
        return [item.decode() for item in raw_history]

    def clear_history(self, metric_name: str) -> None:
        """Clear metric history from Redis."""
        key = f"{self._key_prefix}:history:{metric_name}"
        self._redis.delete(key)


# Export for dependency injection
__all__ = [
    "InMemoryAlertRuleStorage",
    "InMemoryHealthStatusStorage",
    "InMemoryMetricHistoryStorage",
    "InMemoryPatternStorage",
    "InMemoryTraceStorage",
    "RedisAlertRuleStorage",
    "RedisMetricHistoryStorage",
]
