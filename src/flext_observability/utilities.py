"""FLEXT Observability Utilities - Comprehensive Monitoring and Observability Utilities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextUtilities,
)
from flext_observability.models import FlextObservabilityModels


class FlextObservabilityUtilities(FlextUtilities):
    """Unified observability utilities service extending FlextUtilities.

    Provides comprehensive observability utilities for monitoring, metrics,
    tracing, alerting, and performance analysis without duplicating functionality.
    Uses FlextObservabilityModels for all domain-specific data structures.
    """

    def __init__(self) -> None:
        """Initialize FlextObservabilityUtilities service."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute the main observability service operation.

        Returns:
            FlextResult[dict[str, Any]]: Service status and capabilities.

        """
        return FlextResult[dict[str, Any]].ok({
            "status": "operational",
            "service": "flext-observability-utilities",
            "capabilities": [
                "metrics_collection",
                "distributed_tracing",
                "alert_management",
                "health_monitoring",
                "log_analysis",
                "performance_monitoring",
                "dashboard_management",
            ],
        })

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return self._logger

    @property
    def container(self) -> FlextContainer:
        """Get container instance."""
        return self._container

    class MetricsCollection:
        """Metrics collection and management utilities."""

        @staticmethod
        def create_metric_entry(
            name: str,
            value: float,
            unit: str = "count",
            labels: dict[str, str] | None = None,
            source: str = "unknown",
        ) -> FlextResult[FlextObservabilityModels.MetricEntry]:
            """Create a new metric entry.

            Args:
                name: Metric name
                value: Metric value
                unit: Metric unit (default: count)
                labels: Optional metric labels
                source: Metric source service

            Returns:
                FlextResult containing metric entry or error

            """
            try:
                import uuid

                metric = FlextObservabilityModels.MetricEntry(
                    metric_id=str(uuid.uuid4()),
                    name=name,
                    value=value,
                    unit=unit,
                    labels=labels or {},
                    source=source,
                )
                return FlextResult[FlextObservabilityModels.MetricEntry].ok(metric)
            except Exception as e:
                return FlextResult[FlextObservabilityModels.MetricEntry].fail(
                    f"Metric creation failed: {e}"
                )

        @staticmethod
        def aggregate_metrics(
            metrics: list[FlextObservabilityModels.MetricEntry],
            aggregation_method: str = "sum",
        ) -> FlextResult[float]:
            """Aggregate multiple metrics using specified method.

            Args:
                metrics: List of metric entries
                aggregation_method: Aggregation method (sum, avg, min, max, count)

            Returns:
                FlextResult containing aggregated value or error

            """
            try:
                if not metrics:
                    return FlextResult[float].fail("No metrics to aggregate")

                values = [metric.value for metric in metrics]

                if aggregation_method == "sum":
                    result = sum(values)
                elif aggregation_method == "avg":
                    result = sum(values) / len(values)
                elif aggregation_method == "min":
                    result = min(values)
                elif aggregation_method == "max":
                    result = max(values)
                elif aggregation_method == "count":
                    result = float(len(values))
                else:
                    return FlextResult[float].fail(
                        f"Unknown aggregation method: {aggregation_method}"
                    )

                return FlextResult[float].ok(result)
            except Exception as e:
                return FlextResult[float].fail(f"Metric aggregation failed: {e}")

        @staticmethod
        def filter_metrics_by_labels(
            metrics: list[FlextObservabilityModels.MetricEntry],
            label_filters: dict[str, str],
        ) -> FlextResult[list[FlextObservabilityModels.MetricEntry]]:
            """Filter metrics by label values.

            Args:
                metrics: List of metric entries
                label_filters: Label key-value pairs to filter by

            Returns:
                FlextResult containing filtered metrics or error

            """
            try:
                filtered_metrics = []
                for metric in metrics:
                    matches = all(
                        metric.labels.get(key) == value
                        for key, value in label_filters.items()
                    )
                    if matches:
                        filtered_metrics.append(metric)

                return FlextResult[list[FlextObservabilityModels.MetricEntry]].ok(
                    filtered_metrics
                )
            except Exception as e:
                return FlextResult[list[FlextObservabilityModels.MetricEntry]].fail(
                    f"Metric filtering failed: {e}"
                )

    class DistributedTracing:
        """Distributed tracing utilities."""

        @staticmethod
        def create_trace_entry(
            operation_name: str,
            service_name: str,
            parent_span_id: str | None = None,
            tags: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservabilityModels.TraceEntry]:
            """Create a new trace entry.

            Args:
                operation_name: Name of the operation being traced
                service_name: Name of the service
                parent_span_id: Optional parent span identifier
                tags: Optional trace tags

            Returns:
                FlextResult containing trace entry or error

            """
            try:
                import uuid

                trace = FlextObservabilityModels.TraceEntry(
                    trace_id=str(uuid.uuid4()),
                    span_id=str(uuid.uuid4()),
                    parent_span_id=parent_span_id,
                    operation_name=operation_name,
                    service_name=service_name,
                    tags=tags or {},
                )
                return FlextResult[FlextObservabilityModels.TraceEntry].ok(trace)
            except Exception as e:
                return FlextResult[FlextObservabilityModels.TraceEntry].fail(
                    f"Trace creation failed: {e}"
                )

        @staticmethod
        def finish_trace(
            trace: FlextObservabilityModels.TraceEntry,
            status: str = "completed",
        ) -> FlextResult[FlextObservabilityModels.TraceEntry]:
            """Finish a trace entry by setting end time and duration.

            Args:
                trace: Trace entry to finish
                status: Final trace status

            Returns:
                FlextResult containing finished trace or error

            """
            try:
                finished_trace = trace.model_copy()
                finished_trace.end_time = datetime.now()
                if finished_trace.start_time and finished_trace.end_time:
                    duration = finished_trace.end_time - finished_trace.start_time
                    finished_trace.duration_ms = duration.total_seconds() * 1000
                finished_trace.status = status

                return FlextResult[FlextObservabilityModels.TraceEntry].ok(
                    finished_trace
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.TraceEntry].fail(
                    f"Trace finishing failed: {e}"
                )

        @staticmethod
        def calculate_trace_tree_depth(
            traces: list[FlextObservabilityModels.TraceEntry],
        ) -> FlextResult[int]:
            """Calculate the maximum depth of a trace tree.

            Args:
                traces: List of trace entries forming a tree

            Returns:
                FlextResult containing maximum depth or error

            """
            try:
                # Build parent-child relationships
                children_map: dict[str, list[str]] = {}
                for trace in traces:
                    if trace.parent_span_id:
                        if trace.parent_span_id not in children_map:
                            children_map[trace.parent_span_id] = []
                        children_map[trace.parent_span_id].append(trace.span_id)

                # Find root spans (no parent)
                root_spans = [
                    trace.span_id for trace in traces if not trace.parent_span_id
                ]

                def calculate_depth(span_id: str) -> int:
                    if span_id not in children_map:
                        return 1
                    max_child_depth = max(
                        calculate_depth(child_id) for child_id in children_map[span_id]
                    )
                    return 1 + max_child_depth

                if not root_spans:
                    return FlextResult[int].ok(0)

                max_depth = max(calculate_depth(root_id) for root_id in root_spans)
                return FlextResult[int].ok(max_depth)
            except Exception as e:
                return FlextResult[int].fail(f"Trace depth calculation failed: {e}")

    class AlertManagement:
        """Alert management utilities."""

        @staticmethod
        def create_alert(
            name: str,
            severity: str,
            message: str,
            source: str,
            metadata: dict[str, str] | None = None,
        ) -> FlextResult[FlextObservabilityModels.AlertEntry]:
            """Create a new alert entry.

            Args:
                name: Alert name
                severity: Alert severity (critical, warning, info, low)
                message: Alert message
                source: Alert source
                metadata: Optional alert metadata

            Returns:
                FlextResult containing alert entry or error

            """
            try:
                import uuid

                alert = FlextObservabilityModels.AlertEntry(
                    alert_id=str(uuid.uuid4()),
                    name=name,
                    severity=severity,
                    message=message,
                    source=source,
                    metadata=metadata or {},
                )
                return FlextResult[FlextObservabilityModels.AlertEntry].ok(alert)
            except Exception as e:
                return FlextResult[FlextObservabilityModels.AlertEntry].fail(
                    f"Alert creation failed: {e}"
                )

        @staticmethod
        def resolve_alert(
            alert: FlextObservabilityModels.AlertEntry,
        ) -> FlextResult[FlextObservabilityModels.AlertEntry]:
            """Resolve an alert by setting resolved timestamp and status.

            Args:
                alert: Alert entry to resolve

            Returns:
                FlextResult containing resolved alert or error

            """
            try:
                resolved_alert = alert.model_copy()
                resolved_alert.resolved_at = datetime.now()
                resolved_alert.status = "resolved"

                return FlextResult[FlextObservabilityModels.AlertEntry].ok(
                    resolved_alert
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.AlertEntry].fail(
                    f"Alert resolution failed: {e}"
                )

        @staticmethod
        def filter_alerts_by_severity(
            alerts: list[FlextObservabilityModels.AlertEntry],
            min_severity: str = "info",
        ) -> FlextResult[list[FlextObservabilityModels.AlertEntry]]:
            """Filter alerts by minimum severity level.

            Args:
                alerts: List of alert entries
                min_severity: Minimum severity level to include

            Returns:
                FlextResult containing filtered alerts or error

            """
            try:
                severity_levels = {"low": 0, "info": 1, "warning": 2, "critical": 3}
                min_level = severity_levels.get(min_severity.lower(), 0)

                filtered_alerts = [
                    alert
                    for alert in alerts
                    if severity_levels.get(alert.severity.lower(), 0) >= min_level
                ]

                return FlextResult[list[FlextObservabilityModels.AlertEntry]].ok(
                    filtered_alerts
                )
            except Exception as e:
                return FlextResult[list[FlextObservabilityModels.AlertEntry]].fail(
                    f"Alert filtering failed: {e}"
                )

    class HealthMonitoring:
        """Health monitoring utilities."""

        @staticmethod
        def create_health_check(
            name: str,
            component: str,
            status: str = "unknown",
            response_time_ms: float | None = None,
            details: dict[str, object] | None = None,
        ) -> FlextResult[FlextObservabilityModels.HealthCheckEntry]:
            """Create a new health check entry.

            Args:
                name: Health check name
                component: Component being checked
                status: Health status (healthy, degraded, unhealthy, unknown)
                response_time_ms: Optional response time in milliseconds
                details: Optional health check details

            Returns:
                FlextResult containing health check entry or error

            """
            try:
                import uuid

                health_check = FlextObservabilityModels.HealthCheckEntry(
                    check_id=str(uuid.uuid4()),
                    name=name,
                    status=status,
                    component=component,
                    response_time_ms=response_time_ms,
                    details=details or {},
                )
                return FlextResult[FlextObservabilityModels.HealthCheckEntry].ok(
                    health_check
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.HealthCheckEntry].fail(
                    f"Health check creation failed: {e}"
                )

        @staticmethod
        def evaluate_system_health(
            health_checks: list[FlextObservabilityModels.HealthCheckEntry],
        ) -> FlextResult[str]:
            """Evaluate overall system health based on individual health checks.

            Args:
                health_checks: List of health check entries

            Returns:
                FlextResult containing overall health status or error

            """
            try:
                if not health_checks:
                    return FlextResult[str].ok("unknown")

                status_counts = {}
                for check in health_checks:
                    status = check.status
                    status_counts[status] = status_counts.get(status, 0) + 1

                # Determine overall health based on worst status
                if status_counts.get("unhealthy", 0) > 0:
                    overall_status = "unhealthy"
                elif status_counts.get("degraded", 0) > 0:
                    overall_status = "degraded"
                elif status_counts.get("healthy", 0) == len(health_checks):
                    overall_status = "healthy"
                else:
                    overall_status = "unknown"

                return FlextResult[str].ok(overall_status)
            except Exception as e:
                return FlextResult[str].fail(f"Health evaluation failed: {e}")

    class LogAnalysis:
        """Log analysis utilities."""

        @staticmethod
        def create_log_entry(
            level: str,
            message: str,
            logger_name: str,
            source: str,
            context: dict[str, object] | None = None,
        ) -> FlextResult[FlextObservabilityModels.LogEntry]:
            """Create a new log entry.

            Args:
                level: Log level (debug, info, warning, error, critical)
                message: Log message
                logger_name: Name of the logger
                source: Log source
                context: Optional log context

            Returns:
                FlextResult containing log entry or error

            """
            try:
                import uuid

                log_entry = FlextObservabilityModels.LogEntry(
                    log_id=str(uuid.uuid4()),
                    level=level,
                    message=message,
                    logger_name=logger_name,
                    source=source,
                    context=context or {},
                )
                return FlextResult[FlextObservabilityModels.LogEntry].ok(log_entry)
            except Exception as e:
                return FlextResult[FlextObservabilityModels.LogEntry].fail(
                    f"Log entry creation failed: {e}"
                )

        @staticmethod
        def filter_logs_by_level(
            logs: list[FlextObservabilityModels.LogEntry],
            min_level: str = "info",
        ) -> FlextResult[list[FlextObservabilityModels.LogEntry]]:
            """Filter logs by minimum level.

            Args:
                logs: List of log entries
                min_level: Minimum log level to include

            Returns:
                FlextResult containing filtered logs or error

            """
            try:
                level_values = {
                    "debug": 0,
                    "info": 1,
                    "warning": 2,
                    "error": 3,
                    "critical": 4,
                }
                min_value = level_values.get(min_level.lower(), 0)

                filtered_logs = [
                    log
                    for log in logs
                    if level_values.get(log.level.lower(), 0) >= min_value
                ]

                return FlextResult[list[FlextObservabilityModels.LogEntry]].ok(
                    filtered_logs
                )
            except Exception as e:
                return FlextResult[list[FlextObservabilityModels.LogEntry]].fail(
                    f"Log filtering failed: {e}"
                )

        @staticmethod
        def analyze_log_patterns(
            logs: list[FlextObservabilityModels.LogEntry],
            time_window_minutes: int = 60,
        ) -> FlextResult[dict[str, int]]:
            """Analyze log patterns within a time window.

            Args:
                logs: List of log entries
                time_window_minutes: Time window for pattern analysis

            Returns:
                FlextResult containing pattern analysis or error

            """
            try:
                now = datetime.now()
                cutoff_time = now - timedelta(minutes=time_window_minutes)

                # Filter logs within time window
                recent_logs = [log for log in logs if log.timestamp >= cutoff_time]

                # Count by level
                level_counts = {}
                for log in recent_logs:
                    level = log.level
                    level_counts[level] = level_counts.get(level, 0) + 1

                return FlextResult[dict[str, int]].ok(level_counts)
            except Exception as e:
                return FlextResult[dict[str, int]].fail(
                    f"Log pattern analysis failed: {e}"
                )

    class PerformanceMonitoring:
        """Performance monitoring utilities."""

        @staticmethod
        def create_performance_entry(
            operation: str,
            duration_ms: float,
            service: str,
            cpu_usage: float | None = None,
            memory_usage: float | None = None,
            success: bool = True,
        ) -> FlextResult[FlextObservabilityModels.PerformanceEntry]:
            """Create a new performance entry.

            Args:
                operation: Operation being monitored
                duration_ms: Operation duration in milliseconds
                service: Service name
                cpu_usage: Optional CPU usage percentage
                memory_usage: Optional memory usage in MB
                success: Operation success status

            Returns:
                FlextResult containing performance entry or error

            """
            try:
                import uuid

                performance = FlextObservabilityModels.PerformanceEntry(
                    performance_id=str(uuid.uuid4()),
                    operation=operation,
                    duration_ms=duration_ms,
                    service=service,
                    cpu_usage=cpu_usage,
                    memory_usage=memory_usage,
                    success=success,
                )
                return FlextResult[FlextObservabilityModels.PerformanceEntry].ok(
                    performance
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.PerformanceEntry].fail(
                    f"Performance entry creation failed: {e}"
                )

        @staticmethod
        def calculate_performance_statistics(
            entries: list[FlextObservabilityModels.PerformanceEntry],
        ) -> FlextResult[dict[str, float]]:
            """Calculate performance statistics from entries.

            Args:
                entries: List of performance entries

            Returns:
                FlextResult containing performance statistics or error

            """
            try:
                if not entries:
                    return FlextResult[dict[str, float]].fail("No performance entries")

                durations = [entry.duration_ms for entry in entries]
                success_count = sum(1 for entry in entries if entry.success)

                stats = {
                    "avg_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "success_rate": success_count / len(entries),
                    "total_operations": len(entries),
                }

                return FlextResult[dict[str, float]].ok(stats)
            except Exception as e:
                return FlextResult[dict[str, float]].fail(
                    f"Performance statistics calculation failed: {e}"
                )

    class DashboardManagement:
        """Dashboard management utilities."""

        @staticmethod
        def create_dashboard(
            name: str,
            description: str,
            created_by: str,
            widgets: list[dict[str, object]] | None = None,
            is_public: bool = False,
        ) -> FlextResult[FlextObservabilityModels.DashboardEntry]:
            """Create a new dashboard entry.

            Args:
                name: Dashboard name
                description: Dashboard description
                created_by: Dashboard creator
                widgets: Optional dashboard widgets
                is_public: Dashboard visibility

            Returns:
                FlextResult containing dashboard entry or error

            """
            try:
                import uuid

                dashboard = FlextObservabilityModels.DashboardEntry(
                    dashboard_id=str(uuid.uuid4()),
                    name=name,
                    description=description,
                    created_by=created_by,
                    widgets=widgets or [],
                    is_public=is_public,
                )
                return FlextResult[FlextObservabilityModels.DashboardEntry].ok(
                    dashboard
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.DashboardEntry].fail(
                    f"Dashboard creation failed: {e}"
                )

        @staticmethod
        def add_widget_to_dashboard(
            dashboard: FlextObservabilityModels.DashboardEntry,
            widget_config: dict[str, object],
        ) -> FlextResult[FlextObservabilityModels.DashboardEntry]:
            """Add a widget to an existing dashboard.

            Args:
                dashboard: Dashboard to modify
                widget_config: Widget configuration

            Returns:
                FlextResult containing updated dashboard or error

            """
            try:
                updated_dashboard = dashboard.model_copy()
                updated_dashboard.widgets.append(widget_config)

                return FlextResult[FlextObservabilityModels.DashboardEntry].ok(
                    updated_dashboard
                )
            except Exception as e:
                return FlextResult[FlextObservabilityModels.DashboardEntry].fail(
                    f"Widget addition failed: {e}"
                )

    async def execute_async(self) -> FlextResult[dict[str, Any]]:
        """Execute observability utilities service operation asynchronously."""
        return FlextResult[dict[str, Any]].ok({
            "status": "operational",
            "service": "flext-observability-utilities",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
        })


__all__ = ["FlextObservabilityUtilities"]
