"""Domain services for observability - business logic that doesn't belong to entities.

This module implements SOLID principles:
- Single Responsibility Principle (SRP): Each service has one responsibility
- Open/Closed Principle (OCP): Extensible through composition and strategy patterns
- Interface Segregation Principle (ISP): Segregated interfaces for different concerns
- Dependency Inversion Principle (DIP): Services depend on abstractions

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

from flext_core.domain.types import ServiceResult

if TYPE_CHECKING:
    from collections.abc import Sequence

# ==============================================================================
# INTERFACE SEGREGATION PRINCIPLE: Segregated analysis interfaces
# ==============================================================================


class AlertRuleStorage(Protocol):
    """Storage interface for alert rules (ISP compliance)."""

    def store_rule(self, metric_name: str, threshold: Any) -> None:
        """Store alert rule for metric."""

    def get_rule(self, metric_name: str) -> Any | None:
        """Get alert rule for metric."""

    def remove_rule(self, metric_name: str) -> bool:
        """Remove alert rule for metric."""


class MetricHistoryStorage(Protocol):
    """Storage interface for metric history (ISP compliance)."""

    def store_metric(self, metric: Any) -> None:
        """Store metric in history."""

    def get_history(self, metric_name: str, limit: int = 100) -> Sequence[Any]:
        """Get metric history."""

    def clear_history(self, metric_name: str) -> None:
        """Clear metric history."""


class HealthStatusStorage(Protocol):
    """Storage interface for health status (ISP compliance)."""

    def update_status(self, component_key: str, health_check: Any) -> Any | None:
        """Update component health status."""

    def get_status(self, component_key: str) -> Any | None:
        """Get component health status."""

    def get_all_status(self) -> dict[str, Any]:
        """Get all component health statuses."""


class PatternStorage(Protocol):
    """Storage interface for error patterns (ISP compliance)."""

    def increment_pattern(self, pattern: str) -> None:
        """Increment pattern count."""

    def get_patterns(self) -> dict[str, int]:
        """Get all patterns with counts."""

    def clear_patterns(self) -> None:
        """Clear all patterns."""


class TraceStorage(Protocol):
    """Storage interface for trace history (ISP compliance)."""

    def store_trace(self, operation_name: str, trace: Any) -> None:
        """Store trace in history."""

    def get_traces(self, operation_name: str, limit: int = 1000) -> Sequence[Any]:
        """Get trace history for operation."""

    def clear_traces(self, operation_name: str) -> None:
        """Clear trace history for operation."""


# ==============================================================================
# OPEN/CLOSED PRINCIPLE: Extensible threshold strategies
# ==============================================================================


class ThresholdEvaluator(ABC):
    """Abstract threshold evaluator for different comparison strategies (OCP compliance)."""

    @abstractmethod
    def compare(self, value: Any, threshold: Any) -> bool:
        """Compare value against threshold."""

    @abstractmethod
    def get_description(self) -> str:
        """Get description of threshold logic."""


class SimpleThresholdEvaluator(ThresholdEvaluator):
    """Simple threshold evaluator using threshold.compare method."""

    def compare(self, value: Any, threshold: Any) -> bool:
        """Use threshold's compare method if available."""
        if hasattr(threshold, "compare"):
            result = threshold.compare(value)
            return bool(result)  # Ensure boolean return
        return False

    def get_description(self) -> str:
        """Get description of simple threshold evaluation."""
        return "Simple threshold comparison using threshold.compare(value)"


class NumericThresholdEvaluator(ThresholdEvaluator):
    """Numeric threshold evaluator for numeric comparisons."""

    def __init__(self, operator_func: Any = operator.gt) -> None:
        """Initialize with comparison operator (default: greater than)."""
        self.operator_func = operator_func

    def compare(self, value: Any, threshold: Any) -> bool:
        """Compare numeric values using operator."""
        try:
            result = self.operator_func(float(value), float(threshold))
            return bool(result)  # Ensure boolean return
        except (ValueError, TypeError):
            return False

    def get_description(self) -> str:
        """Get description of numeric threshold evaluation."""
        op_name = getattr(self.operator_func, "__name__", "unknown")
        return f"Numeric threshold comparison using operator: {op_name}"


# ==============================================================================
# SINGLE RESPONSIBILITY PRINCIPLE: Specialized service classes
# ==============================================================================


class AlertingService:
    """SOLID-compliant domain service for alert management and evaluation.

    Implements:
    - SRP: Focused on alert rule management and evaluation
    - OCP: Extensible through threshold evaluator strategies
    - DIP: Depends on storage and evaluator abstractions
    """

    def __init__(
        self,
        storage: AlertRuleStorage,
        evaluator: ThresholdEvaluator | None = None,
    ) -> None:
        """Initialize alerting service with dependency injection (DIP compliance).

        Args:
            storage: Storage interface for alert rules
            evaluator: Threshold evaluator strategy (defaults to SimpleThresholdEvaluator)

        """
        self._storage = storage
        self._evaluator = evaluator or SimpleThresholdEvaluator()

    def register_alert_rule(self, metric_name: str, threshold: Any) -> ServiceResult[None]:
        """Register alert rule for metric threshold monitoring.

        Args:
            metric_name: Name of metric to monitor.
            threshold: Threshold value object for comparison.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            self._storage.store_rule(metric_name, threshold)
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to register alert rule: {e}")

    def remove_alert_rule(self, metric_name: str) -> ServiceResult[bool]:
        """Remove alert rule for metric.

        Args:
            metric_name: Name of metric to remove rule for.

        Returns:
            ServiceResult with boolean indicating if rule was removed.

        """
        try:
            removed = self._storage.remove_rule(metric_name)
            return ServiceResult.ok(removed)
        except Exception as e:
            return ServiceResult.fail(f"Failed to remove alert rule: {e}")

    def evaluate_metric(self, metric: Any) -> ServiceResult[dict[str, Any] | None]:
        """Evaluate metric against registered alert rules using strategy pattern (OCP compliance).

        Args:
            metric: Metric to evaluate.

        Returns:
            ServiceResult with alert data if threshold exceeded, None otherwise.

        """
        try:
            # Check if there's a rule for this metric
            threshold = self._storage.get_rule(metric.name)
            if threshold is None:
                return ServiceResult.ok(None)

            # Use strategy pattern for threshold evaluation (OCP compliance)
            if not self._evaluator.compare(metric.value, threshold):
                return ServiceResult.ok(None)

            # Create alert data
            alert_data = {
                "title": f"Metric {metric.name} threshold exceeded",
                "description": f"Metric {metric.name} value exceeded threshold using {self._evaluator.get_description()}",
                "severity": self._determine_severity(metric, threshold),
                "metric": metric,
                "threshold": threshold,
                "evaluator": self._evaluator.get_description(),
            }

            return ServiceResult.ok(alert_data)

        except Exception as e:
            return ServiceResult.fail(f"Failed to evaluate metric: {e}")

    def _determine_severity(self, metric: Any, threshold: Any) -> str:
        """Determine alert severity based on metric and threshold (private helper for SRP)."""
        # Simple severity logic - can be extended with more sophisticated rules
        try:
            metric_value = float(metric.value)
            threshold_value = float(threshold.value if hasattr(threshold, "value") else threshold)

            if metric_value > threshold_value * 2:
                return "high"
            if metric_value > threshold_value * 1.5:
                return "medium"
            return "low"
        except (ValueError, TypeError, AttributeError):
            return "medium"  # Default severity


# ==============================================================================
# OPEN/CLOSED PRINCIPLE: Extensible trend analysis strategies
# ==============================================================================


class TrendAnalyzer(ABC):
    """Abstract trend analyzer for different trend detection strategies (OCP compliance)."""

    @abstractmethod
    def analyze(self, values: Sequence[float]) -> dict[str, Any]:
        """Analyze trend from sequence of values."""

    @abstractmethod
    def get_analyzer_name(self) -> str:
        """Get name of trend analyzer."""


class SimpleTrendAnalyzer(TrendAnalyzer):
    """Simple trend analyzer using first/second half comparison."""

    def __init__(self, stability_threshold: float = 5.0) -> None:
        """Initialize with stability threshold percentage."""
        self.stability_threshold = stability_threshold

    def get_analyzer_name(self) -> str:
        """Get name of trend analyzer."""
        return "simple_trend"

    def analyze(self, values: Sequence[float]) -> dict[str, Any]:
        """Analyze trend using first/second half comparison."""
        if len(values) < 2:
            return {
                "trend": "unknown",
                "change": 0.0,
                "points": len(values),
                "analyzer": self.get_analyzer_name(),
            }

        # Simple trend calculation
        first_half = values[: len(values) // 2]
        second_half = values[len(values) // 2 :]

        if not first_half or not second_half:
            return {
                "trend": "stable",
                "change": 0.0,
                "points": len(values),
                "analyzer": self.get_analyzer_name(),
            }

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        change = (
            ((avg_second - avg_first) / avg_first) * 100 if avg_first != 0 else 0
        )

        if abs(change) < self.stability_threshold:
            trend = "stable"
        elif change > 0:
            trend = "increasing"
        else:
            trend = "decreasing"

        return {
            "trend": trend,
            "change": change,
            "points": len(values),
            "average": avg_second,
            "analyzer": self.get_analyzer_name(),
        }


class LinearRegressionTrendAnalyzer(TrendAnalyzer):
    """Linear regression trend analyzer for more sophisticated trend detection."""

    def get_analyzer_name(self) -> str:
        """Get name of trend analyzer."""
        return "linear_regression"

    def analyze(self, values: Sequence[float]) -> dict[str, Any]:
        """Analyze trend using simple linear regression."""
        if len(values) < 2:
            return {
                "trend": "unknown",
                "change": 0.0,
                "points": len(values),
                "analyzer": self.get_analyzer_name(),
            }

        # Simple linear regression: y = ax + b
        n = len(values)
        x_values = list(range(n))

        # Calculate slope (a)
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values, strict=False))
        sum_x_squared = sum(x * x for x in x_values)

        denominator = n * sum_x_squared - sum_x * sum_x
        slope = 0 if denominator == 0 else (n * sum_xy - sum_x * sum_y) / denominator

        # Determine trend based on slope
        if abs(slope) < 0.1:  # Small slope threshold
            trend = "stable"
        elif slope > 0:
            trend = "increasing"
        else:
            trend = "decreasing"

        # Calculate change as percentage
        first_value = values[0]
        last_value = values[-1]
        change = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0

        return {
            "trend": trend,
            "change": change,
            "slope": slope,
            "points": len(values),
            "average": sum(values) / len(values),
            "analyzer": self.get_analyzer_name(),
        }


class MetricsAnalysisService:
    """SOLID-compliant domain service for metrics analysis and trend detection.

    Implements:
    - SRP: Focused on metrics analysis and trend detection
    - OCP: Extensible through trend analyzer strategies
    - DIP: Depends on storage and analyzer abstractions
    """

    def __init__(
        self,
        storage: MetricHistoryStorage,
        trend_analyzer: TrendAnalyzer | None = None,
        max_history_size: int = 100,
    ) -> None:
        """Initialize metrics analysis service with dependency injection (DIP compliance).

        Args:
            storage: Storage interface for metric history
            trend_analyzer: Trend analyzer strategy (defaults to SimpleTrendAnalyzer)
            max_history_size: Maximum number of metrics to keep in history

        """
        self._storage = storage
        self._trend_analyzer = trend_analyzer or SimpleTrendAnalyzer()
        self._max_history_size = max_history_size

    def analyze_trend(self, metric: Any) -> ServiceResult[dict[str, Any]]:
        """Analyze metric trends using strategy pattern (OCP compliance).

        Args:
            metric: Metric to analyze.

        Returns:
            ServiceResult with trend analysis data.

        """
        try:
            # Store metric in history
            self._storage.store_metric(metric)

            # Get history for trend analysis
            history = self._storage.get_history(metric.name, self._max_history_size)

            # Need at least 2 points for trend analysis
            if len(history) < 2:
                return ServiceResult.ok({
                    "trend": "unknown",
                    "change": 0.0,
                    "points": len(history),
                    "analyzer": self._trend_analyzer.get_analyzer_name(),
                })

            # Extract values for analysis
            try:
                values = [float(m.value) for m in history[-10:]]  # Last 10 values
            except (ValueError, AttributeError) as e:
                return ServiceResult.fail(f"Failed to extract numeric values: {e}")

            if len(values) < 2:
                return ServiceResult.ok({
                    "trend": "stable",
                    "change": 0.0,
                    "points": len(values),
                    "analyzer": self._trend_analyzer.get_analyzer_name(),
                })

            # Use strategy pattern for trend analysis (OCP compliance)
            analysis = self._trend_analyzer.analyze(values)
            analysis["metric_name"] = metric.name

            return ServiceResult.ok(analysis)

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze trend: {e}")

    def get_metric_statistics(self, metric_name: str) -> ServiceResult[dict[str, Any]]:
        """Get statistical summary for metric history (additional SRP responsibility).

        Args:
            metric_name: Name of metric to get statistics for.

        Returns:
            ServiceResult with metric statistics.

        """
        try:
            history = self._storage.get_history(metric_name, self._max_history_size)

            if not history:
                return ServiceResult.ok({
                    "metric_name": metric_name,
                    "count": 0,
                    "min": None,
                    "max": None,
                    "average": None,
                    "latest": None,
                })

            # Extract numeric values
            values = []
            for m in history:
                try:
                    values.append(float(m.value))
                except (ValueError, AttributeError):
                    continue

            if not values:
                return ServiceResult.fail("No numeric values found in metric history")

            statistics = {
                "metric_name": metric_name,
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "average": sum(values) / len(values),
                "latest": values[-1] if values else None,
            }

            return ServiceResult.ok(statistics)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get metric statistics: {e}")


class HealthAnalysisService:
    """Domain service for health analysis and status aggregation."""

    def __init__(self) -> None:
        self._component_health: dict[str, Any] = {}

    def update_component_health(self, health_check: Any) -> ServiceResult[bool]:
        """Update component health status and detect changes.

        Args:
            health_check: Health check result for component.

        Returns:
            ServiceResult with boolean indicating if status changed.

        """
        try:
            component_key = str(health_check.component)
            previous_health = self._component_health.get(component_key)

            # Store new health status
            self._component_health[component_key] = health_check

            # Check if status changed
            status_changed = (
                previous_health is None or previous_health.status != health_check.status
            )

            return ServiceResult.ok(status_changed)

        except Exception as e:
            return ServiceResult.fail(f"Failed to update component health: {e}")

    def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get aggregated system health status.

        Returns:
            ServiceResult with system health summary and score.

        """
        try:
            if not self._component_health:
                return ServiceResult.ok(
                    {
                        "overall_status": "unknown",
                        "healthy_components": 0,
                        "unhealthy_components": 0,
                        "total_components": 0,
                        "health_score": 0.0,
                    },
                )

            # Count components by status (simplified)
            total = len(self._component_health)
            healthy = sum(
                1
                for hc in self._component_health.values()
                if str(hc.status) == "healthy"
            )

            health_score = healthy / total if total > 0 else 0.0

            return ServiceResult.ok(
                {
                    "overall_status": "healthy" if health_score > 0.8 else "degraded",
                    "healthy_components": healthy,
                    "unhealthy_components": total - healthy,
                    "total_components": total,
                    "health_score": health_score,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")


class LogAnalysisService:
    """Domain service for log analysis and pattern detection."""

    def __init__(self) -> None:
        self._error_patterns: dict[str, int] = {}

    def analyze_log_entry(self, log_entry: Any) -> ServiceResult[dict[str, Any]]:
        """Analyze log entry for patterns and severity.

        Args:
            log_entry: Log entry to analyze.

        Returns:
            ServiceResult with log analysis data including patterns and severity.

        """
        try:
            analysis: dict[str, Any] = {
                "is_error": getattr(log_entry, "is_error", False),
                "severity": str(log_entry.level),
                "has_exception": getattr(log_entry, "exception", None) is not None,
                "patterns": [],
            }

            # Pattern detection for error messages
            if analysis["is_error"] and hasattr(log_entry, "message"):
                pattern = self._extract_error_pattern(log_entry.message)
                if pattern:
                    analysis["patterns"].append(pattern)
                    self._error_patterns[pattern] = (
                        self._error_patterns.get(pattern, 0) + 1
                    )

            return ServiceResult.ok(analysis)

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze log entry: {e}")

    def _extract_error_pattern(self, message: str) -> str | None:
        """Simple pattern extraction - replace specific values with placeholders."""
        import re

        # Replace numbers with placeholder
        pattern = re.sub(r"\d+", "{number}", message)

        # Replace UUIDs
        pattern = re.sub(
            r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
            "{uuid}",
            pattern,
        )

        # Replace file paths
        pattern = re.sub(r"/[^\s]+", "{path}", pattern)

        return pattern if pattern != message else None

    def get_error_patterns(self) -> ServiceResult[dict[str, int]]:
        """Get error patterns sorted by frequency.

        Returns:
            ServiceResult with dictionary of error patterns and their occurrence counts.

        """
        try:
            # Sort by frequency
            sorted_patterns = dict(
                sorted(
                    self._error_patterns.items(),
                    key=operator.itemgetter(1),
                    reverse=True,
                ),
            )
            return ServiceResult.ok(sorted_patterns)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get error patterns: {e}")


class TraceAnalysisService:
    """Domain service for trace analysis and performance monitoring."""

    def __init__(self) -> None:
        self._trace_history: dict[str, list[Any]] = {}

    def analyze_trace(self, trace: Any) -> ServiceResult[dict[str, Any]]:
        """Analyze trace for performance and error patterns.

        Args:
            trace: Trace to analyze.

        Returns:
            ServiceResult with trace analysis including duration and status.

        """
        try:
            # Store trace in history
            if trace.operation_name not in self._trace_history:
                self._trace_history[trace.operation_name] = []

            self._trace_history[trace.operation_name].append(trace)

            # Keep only last 1000 traces per operation
            if len(self._trace_history[trace.operation_name]) > 1000:
                self._trace_history[trace.operation_name] = self._trace_history[
                    trace.operation_name
                ][-1000:]

            analysis = {
                "operation": trace.operation_name,
                "status": str(trace.status) if hasattr(trace, "status") else "unknown",
                "duration_ms": getattr(trace, "duration_ms", 0),
                "is_error": str(getattr(trace, "status", "")) == "failed",
                "has_logs": len(getattr(trace, "logs", [])) > 0,
            }

            return ServiceResult.ok(analysis)

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze trace: {e}")

    def get_operation_stats(self, operation_name: str) -> ServiceResult[dict[str, Any]]:
        """Get performance statistics for specific operation.

        Args:
            operation_name: Name of operation to get stats for.

        Returns:
            ServiceResult with operation performance statistics.

        """
        try:
            history = self._trace_history.get(operation_name, [])

            if not history:
                return ServiceResult.ok(
                    {
                        "operation": operation_name,
                        "total_traces": 0,
                        "success_rate": 0.0,
                        "error_rate": 0.0,
                        "avg_duration_ms": 0.0,
                    },
                )

            total = len(history)
            successful = sum(
                1 for t in history if str(getattr(t, "status", "")) == "completed"
            )
            failed = sum(
                1 for t in history if str(getattr(t, "status", "")) == "failed"
            )

            durations = [getattr(t, "duration_ms", 0) for t in history]
            avg_duration = sum(durations) / len(durations) if durations else 0

            return ServiceResult.ok(
                {
                    "operation": operation_name,
                    "total_traces": total,
                    "successful_traces": successful,
                    "failed_traces": failed,
                    "success_rate": successful / total if total > 0 else 0,
                    "error_rate": failed / total if total > 0 else 0,
                    "avg_duration_ms": avg_duration,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to get operation stats: {e}")


__all__ = [
    # Protocol interfaces (ISP compliance)
    "AlertRuleStorage",
    # Service classes
    "AlertingService",
    "HealthAnalysisService",
    "HealthStatusStorage",
    "LinearRegressionTrendAnalyzer",
    "LogAnalysisService",
    "MetricHistoryStorage",
    "MetricsAnalysisService",
    "NumericThresholdEvaluator",
    "PatternStorage",
    "SimpleThresholdEvaluator",
    "SimpleTrendAnalyzer",
    # Strategy classes (OCP compliance)
    "ThresholdEvaluator",
    "TraceAnalysisService",
    "TraceStorage",
    "TrendAnalyzer",
]
