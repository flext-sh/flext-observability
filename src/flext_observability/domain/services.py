"""Domain services for observability - business logic that doesn't belong to entities."""

from __future__ import annotations

import operator
from typing import TYPE_CHECKING
from typing import Any

from flext_core.domain import ServiceResult
from flext_observability.domain.entities import Alert
from flext_observability.domain.value_objects import AlertSeverity
from flext_observability.domain.value_objects import HealthStatus

if TYPE_CHECKING:
    from flext_observability.domain.entities import HealthCheck
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace
    from flext_observability.domain.value_objects import ComponentName
    from flext_observability.domain.value_objects import ThresholdValue


class AlertingService:
    """Domain service for alert management and evaluation."""

    def __init__(self) -> None:
        self._alert_rules: dict[str, ThresholdValue] = {}

    def register_alert_rule(self, metric_name: str, threshold: ThresholdValue) -> None:
        """Register an alert rule for a metric."""
        self._alert_rules[metric_name] = threshold

    def evaluate_metric(self, metric: Metric) -> ServiceResult[Alert | None]:
        """Evaluate a metric against alert rules."""
        try:
            # Check if there's a rule for this metric
            if metric.name not in self._alert_rules:
                return ServiceResult.ok(None)

            threshold = self._alert_rules[metric.name]

            # Check if threshold is exceeded
            if not threshold.compare(metric.value):
                return ServiceResult.ok(None)

            # Create alert
            severity = self._calculate_severity(metric, threshold)
            alert = Alert(
                title=f"Metric {metric.name} threshold exceeded",
                description=f"Metric {metric.name} value {metric.value.value} "
                f"exceeded threshold {threshold.value} ({threshold.operator})",
                severity=severity,
                metric=metric,
                threshold=threshold,
            )

            return ServiceResult.ok(alert)

        except Exception as e:
            return ServiceResult.fail(f"Failed to evaluate metric: {e}")

    def _calculate_severity(
        self, metric: Metric, threshold: ThresholdValue,
    ) -> AlertSeverity:
        """Calculate alert severity based on how much the threshold is exceeded."""
        value = metric.value.value
        threshold_value = threshold.value

        # Simple severity calculation - can be made more sophisticated
        if threshold.operator in {"gt", "ge"}:
            ratio = value / threshold_value
        else:
            ratio = threshold_value / value

        if ratio > 2.0:
            return AlertSeverity.CRITICAL
        if ratio > 1.5:
            return AlertSeverity.WARNING
        return AlertSeverity.INFO


class MetricsAnalysisService:
    """Domain service for metrics analysis and trend detection."""

    def __init__(self) -> None:
        self._metric_history: dict[str, list[Metric]] = {}

    def analyze_trend(self, metric: Metric) -> ServiceResult[dict[str, Any]]:
        """Analyze metric trends."""
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

            # Calculate trend
            recent_values = [
                float(m.value.value) for m in history[-10:]
            ]  # Last 10 values
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

    def detect_anomalies(self, metric: Metric) -> ServiceResult[dict[str, Any]]:
        """Detect anomalies in metric values."""
        try:
            history = self._metric_history.get(metric.name, [])

            # Need at least 10 points for anomaly detection
            if len(history) < 10:
                return ServiceResult.ok(
                    {
                        "is_anomaly": False,
                        "confidence": 0.0,
                        "reason": "insufficient_data",
                    },
                )

            # Simple anomaly detection using standard deviation
            values = [float(m.value.value) for m in history[-50:]]  # Last 50 values
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance**0.5

            current_value = float(metric.value.value)
            z_score = abs(current_value - mean) / std_dev if std_dev > 0 else 0

            # Consider values beyond 2 standard deviations as anomalies
            is_anomaly = z_score > 2.0
            confidence = min(z_score / 3.0, 1.0)  # Normalize confidence

            return ServiceResult.ok(
                {
                    "is_anomaly": is_anomaly,
                    "confidence": confidence,
                    "z_score": z_score,
                    "threshold": 2.0,
                    "mean": mean,
                    "std_dev": std_dev,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to detect anomalies: {e}")


class HealthAnalysisService:
    """Domain service for health analysis and status aggregation."""

    def __init__(self) -> None:
        self._component_health: dict[str, HealthCheck] = {}

    def update_component_health(self, health_check: HealthCheck) -> ServiceResult[bool]:
        """Update component health status."""
        try:
            component_key = health_check.component.full_name
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
        """Get overall system health status."""
        try:
            if not self._component_health:
                return ServiceResult.ok(
                    {
                        "overall_status": HealthStatus.UNKNOWN,
                        "healthy_components": 0,
                        "unhealthy_components": 0,
                        "total_components": 0,
                        "health_score": 0.0,
                    },
                )

            # Count components by status
            status_counts = {}
            for health_check in self._component_health.values():
                status = health_check.status
                status_counts[status] = status_counts.get(status, 0) + 1

            total = len(self._component_health)
            healthy = status_counts.get(HealthStatus.HEALTHY, 0)
            unhealthy = status_counts.get(HealthStatus.UNHEALTHY, 0)
            degraded = status_counts.get(HealthStatus.DEGRADED, 0)

            # Calculate health score
            health_score = (healthy + (degraded * 0.5)) / total if total > 0 else 0.0

            # Determine overall status
            if unhealthy > 0:
                overall_status = HealthStatus.UNHEALTHY
            elif degraded > 0:
                overall_status = HealthStatus.DEGRADED
            elif healthy > 0:
                overall_status = HealthStatus.HEALTHY
            else:
                overall_status = HealthStatus.UNKNOWN

            return ServiceResult.ok(
                {
                    "overall_status": overall_status,
                    "healthy_components": healthy,
                    "unhealthy_components": unhealthy,
                    "degraded_components": degraded,
                    "total_components": total,
                    "health_score": health_score,
                    "status_breakdown": status_counts,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")

    def get_component_dependencies(
        self, component: ComponentName,
    ) -> ServiceResult[list[ComponentName]]:
        """Get dependencies for a component (placeholder implementation)."""
        try:
            # This would typically be loaded from configuration
            # For now, return empty list
            return ServiceResult.ok([])

        except Exception as e:
            return ServiceResult.fail(f"Failed to get component dependencies: {e}")


class LogAnalysisService:
    """Domain service for log analysis and pattern detection."""

    def __init__(self) -> None:
        self._error_patterns: dict[str, int] = {}

    def analyze_log_entry(self, log_entry: LogEntry) -> ServiceResult[dict[str, Any]]:
        """Analyze a log entry for patterns and anomalies."""
        try:
            analysis = {
                "is_error": log_entry.is_error,
                "severity": log_entry.level.value,
                "has_exception": log_entry.exception is not None,
                "field_count": len(log_entry.fields),
                "patterns": [],
            }

            # Pattern detection for error messages
            if log_entry.is_error and log_entry.message:
                pattern = self._extract_error_pattern(log_entry.message)
                if pattern:
                    analysis["patterns"].append(pattern)
                    self._error_patterns[pattern] = (
                        self._error_patterns.get(pattern, 0) + 1
                    )

            # Check for correlation ID
            if log_entry.correlation_id:
                analysis["has_correlation_id"] = True

            # Check for trace information
            if log_entry.trace_id:
                analysis["has_trace_info"] = True

            return ServiceResult.ok(analysis)

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze log entry: {e}")

    def _extract_error_pattern(self, message: str) -> str | None:
        """Extract error pattern from message."""
        # Simple pattern extraction - replace specific values with placeholders
        import re

        # Replace numbers with placeholder
        pattern = re.sub(r"\d+", "{number}", message)

        # Replace common variable patterns
        pattern = re.sub(
            r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
            "{uuid}",
            pattern,
        )

        # Replace file paths
        pattern = re.sub(r"/[^\s]+", "{path}", pattern)

        return pattern if pattern != message else None

    def get_error_patterns(self) -> ServiceResult[dict[str, int]]:
        """Get detected error patterns and their frequencies."""
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
        self._trace_history: dict[str, list[Trace]] = {}

    def analyze_trace(self, trace: Trace) -> ServiceResult[dict[str, Any]]:
        """Analyze a trace for performance and errors."""
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
                "status": trace.status.value,
                "duration_ms": trace.duration.milliseconds if trace.duration else 0,
                "is_error": trace.status.value == "failed",
                "has_logs": len(trace.logs) > 0,
                "tag_count": len(trace.tags),
            }

            # Calculate percentiles for this operation
            history = self._trace_history[trace.operation_name]
            if len(history) >= 10:
                durations = [t.duration.milliseconds for t in history if t.duration]
                if durations:
                    durations.sort()
                    analysis["percentiles"] = {
                        "p50": durations[len(durations) // 2],
                        "p90": durations[int(len(durations) * 0.9)],
                        "p95": durations[int(len(durations) * 0.95)],
                        "p99": durations[int(len(durations) * 0.99)],
                    }

            return ServiceResult.ok(analysis)

        except Exception as e:
            return ServiceResult.fail(f"Failed to analyze trace: {e}")

    def get_operation_stats(self, operation_name: str) -> ServiceResult[dict[str, Any]]:
        """Get statistics for a specific operation."""
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
            successful = sum(1 for t in history if t.status.value == "completed")
            failed = sum(1 for t in history if t.status.value == "failed")

            durations = [t.duration.milliseconds for t in history if t.duration]
            avg_duration = sum(durations) / len(durations) if durations else 0

            return ServiceResult.ok(
                {
                    "operation": operation_name,
                    "total_traces": total,
                    "successful_traces": successful,
                    "failed_traces": failed,
                    "success_rate": successful / total,
                    "error_rate": failed / total,
                    "avg_duration_ms": avg_duration,
                },
            )

        except Exception as e:
            return ServiceResult.fail(f"Failed to get operation stats: {e}")
