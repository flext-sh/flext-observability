"""Domain services for observability - business logic that doesn't belong to entities.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import operator
from typing import Any

from flext_core.domain.types import ServiceResult


class AlertingService:
    """Domain service for alert management and evaluation."""

    def __init__(self) -> None:
        self._alert_rules: dict[str, Any] = {}

    def register_alert_rule(self, metric_name: str, threshold: Any) -> None:
        """Register alert rule for metric threshold monitoring.

        Args:
            metric_name: Name of metric to monitor.
            threshold: Threshold value object for comparison.

        """
        self._alert_rules[metric_name] = threshold

    def evaluate_metric(self, metric: Any) -> ServiceResult[Any]:
        """Evaluate metric against registered alert rules.

        Args:
            metric: Metric to evaluate.

        Returns:
            ServiceResult with alert data if threshold exceeded, None otherwise.

        """
        try:
            # Check if there's a rule for this metric
            if metric.name not in self._alert_rules:
                return ServiceResult.ok(None)

            threshold = self._alert_rules[metric.name]

            # Check if threshold is exceeded
            if not threshold.compare(metric.value):
                return ServiceResult.ok(None)

            # Create alert (simplified)
            alert_data = {
                "title": f"Metric {metric.name} threshold exceeded",
                "description": f"Metric {metric.name} value exceeded threshold",
                "severity": "medium",
                "metric": metric,
                "threshold": threshold,
            }

            return ServiceResult.ok(alert_data)

        except Exception as e:
            return ServiceResult.fail(f"Failed to evaluate metric: {e}")


class MetricsAnalysisService:
    """Domain service for metrics analysis and trend detection."""

    def __init__(self) -> None:
        self._metric_history: dict[str, list[Any]] = {}

    def analyze_trend(self, metric: Any) -> ServiceResult[dict[str, Any]]:
        """Analyze metric trends and detect patterns.

        Args:
            metric: Metric to analyze.

        Returns:
            ServiceResult with trend analysis data.

        """
        try:
            # Store metric in history
            if metric.name not in self._metric_history:
                self._metric_history[metric.name] = []

            self._metric_history[metric.name].append(metric)

            # Keep only last 100 metrics for performance
            if len(self._metric_history[metric.name]) > 100:
                self._metric_history[metric.name] = self._metric_history[metric.name][
                    -100:
                ]

            history = self._metric_history[metric.name]

            # Need at least 2 points for trend analysis
            if len(history) < 2:
                return ServiceResult.ok(
                    {
                        "trend": "unknown",
                        "change": 0.0,
                        "points": len(history),
                    },
                )

            # Calculate trend (simplified)
            recent_values = [float(m.value) for m in history[-10:]]  # Last 10 values
            if len(recent_values) < 2:
                return ServiceResult.ok(
                    {
                        "trend": "stable",
                        "change": 0.0,
                        "points": len(recent_values),
                    },
                )

            # Simple trend calculation
            first_half = recent_values[: len(recent_values) // 2]
            second_half = recent_values[len(recent_values) // 2 :]

            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)

            change = (
                ((avg_second - avg_first) / avg_first) * 100 if avg_first != 0 else 0
            )

            if abs(change) < 5:
                trend = "stable"
            elif change > 0:
                trend = "increasing"
            else:
                trend = "decreasing"

            return ServiceResult.ok(
                {
                    "trend": trend,
                    "change": change,
                    "points": len(recent_values),
                    "average": avg_second,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze trend: {e}")


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
    "AlertingService",
    "HealthAnalysisService",
    "LogAnalysisService",
    "MetricsAnalysisService",
    "TraceAnalysisService",
]
