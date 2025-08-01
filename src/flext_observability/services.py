"""FLEXT Observability Services - Real observability functionality with SOLID.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade observability services implementing OpenTelemetry, Prometheus,
and structured logging with SOLID principles and real functionality.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from typing import TYPE_CHECKING, cast

import psutil
from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.validation import create_observability_result_error

# Health check constants
MEMORY_WARNING_THRESHOLD = 80
MEMORY_CRITICAL_THRESHOLD = 95
DISK_WARNING_THRESHOLD = 80
DISK_CRITICAL_THRESHOLD = 95
THREAD_WARNING_THRESHOLD = 50
THREAD_CRITICAL_THRESHOLD = 100
MAX_METRICS_STORE_SIZE = 1000
METRICS_STORE_CLEANUP_SIZE = 500

if TYPE_CHECKING:
    from flext_observability.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )

# ============================================================================
# CORE SERVICES - Simplified using flext-core patterns
# ============================================================================


class FlextMetricsService:
    """Real metrics service implementing Prometheus-compatible metrics with SOLID.

    Implements Single Responsibility (metrics collection),
    Open/Closed (extensible metric types),
    Liskov Substitution (interface compliance),
    Interface Segregation (focused interfaces),
    and Dependency Inversion (depends on abstractions).
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize metrics service with real storage and aggregation."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

        # Real metrics storage with thread safety (Single Responsibility)
        self._metrics_store: dict[str, list[dict[str, object]]] = defaultdict(list)
        self._metrics_lock = threading.RLock()
        self._metric_counters: dict[str, float] = defaultdict(float)
        self._metric_gauges: dict[str, float] = {}
        self._metric_histograms: dict[str, list[float]] = defaultdict(list)

        # Service health tracking
        self._start_time = time.time()
        self._metrics_recorded = 0

    def record_metric(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Record metric with real storage and validation using SOLID principles."""
        try:
            # Input validation (defensive programming)
            if (
                not metric
                or not hasattr(metric, "name")
                or not hasattr(metric, "value")
            ):
                return FlextResult.fail("Invalid metric: missing name or value")

            if not metric.name or not isinstance(metric.name, str):
                return FlextResult.fail("Metric name must be a non-empty string")

            # Type-safe metric recording with thread safety
            with self._metrics_lock:
                timestamp = time.time()

                # Store raw metric data
                metric_data = {
                    "name": metric.name,
                    "value": metric.value,
                    "timestamp": timestamp,
                    "labels": getattr(metric, "labels", {}),
                    "unit": getattr(metric, "unit", None),
                    "type": getattr(metric, "metric_type", "gauge"),
                }

                self._metrics_store[metric.name].append(metric_data)

                # Update aggregated metrics based on type
                metric_type = metric_data.get("type", "gauge")

                if metric_type == "counter":
                    self._metric_counters[metric.name] += float(metric.value)
                elif metric_type == "gauge":
                    self._metric_gauges[metric.name] = float(metric.value)
                elif metric_type == "histogram":
                    self._metric_histograms[metric.name].append(float(metric.value))

                # Maintain metrics store size (prevent memory leaks)
                if len(self._metrics_store[metric.name]) > MAX_METRICS_STORE_SIZE:
                    self._metrics_store[metric.name] = self._metrics_store[metric.name][
                        -METRICS_STORE_CLEANUP_SIZE:
                    ]

                self._metrics_recorded += 1

            # Structured logging with metric context
            self.logger.info(
                "Metric recorded successfully",
                metric_name=metric.name,
                metric_value=metric.value,
                metric_type=metric_type,
                timestamp=timestamp,
            )

            return FlextResult.ok(metric)

        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "metrics",
                f"Failed to record metric: {e}",
                metric_name=getattr(metric, "name", "unknown"),
                metric_value=getattr(metric, "value", "unknown"),
            )
            return FlextResult.fail(error_result.error or "Unknown error")

    def get_metric_value(self, metric_name: str) -> FlextResult[float]:
        """Get current metric value with type-safe retrieval."""
        try:
            with self._metrics_lock:
                # Try gauge first (most common)
                if metric_name in self._metric_gauges:
                    return FlextResult.ok(self._metric_gauges[metric_name])

                # Try counter
                if metric_name in self._metric_counters:
                    return FlextResult.ok(self._metric_counters[metric_name])

                # Try histogram (return mean)
                if metric_name in self._metric_histograms:
                    values = self._metric_histograms[metric_name]
                    if values:
                        mean_value = sum(values) / len(values)
                        return FlextResult.ok(mean_value)

                return FlextResult.fail(f"Metric '{metric_name}' not found")

        except (ValueError, TypeError, ArithmeticError) as e:
            return FlextResult.fail(f"Failed to retrieve metric '{metric_name}': {e}")

    def get_metrics_summary(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive metrics summary with statistics."""
        try:
            with self._metrics_lock:
                summary = {
                    "service_info": {
                        "uptime_seconds": time.time() - self._start_time,
                        "metrics_recorded": self._metrics_recorded,
                        "unique_metrics": len(self._metrics_store),
                    },
                    "counters": dict(self._metric_counters),
                    "gauges": dict(self._metric_gauges),
                    "histograms": {
                        name: {
                            "count": len(values),
                            "sum": sum(values) if values else 0,
                            "min": min(values) if values else 0,
                            "max": max(values) if values else 0,
                            "mean": sum(values) / len(values) if values else 0,
                        }
                        for name, values in self._metric_histograms.items()
                    },
                }

                return FlextResult.ok(summary)

        except (ValueError, TypeError, ArithmeticError) as e:
            return FlextResult.fail(f"Failed to generate metrics summary: {e}")

    def export_prometheus_format(self) -> FlextResult[str]:
        """Export metrics in Prometheus format for real integration."""
        try:
            with self._metrics_lock:
                prometheus_lines: list[str] = []

                # Export counters
                for name, value in self._metric_counters.items():
                    prometheus_lines.extend(
                        (f"# TYPE {name} counter", f"{name} {value}"),
                    )

                # Export gauges
                for name, value in self._metric_gauges.items():
                    prometheus_lines.extend((f"# TYPE {name} gauge", f"{name} {value}"))

                # Export histograms (simplified)
                for name, values in self._metric_histograms.items():
                    if values:
                        prometheus_lines.extend(
                            (
                                f"# TYPE {name} histogram",
                                f"{name}_count {len(values)}",
                                f"{name}_sum {sum(values)}",
                            ),
                        )

                prometheus_output = "\n".join(prometheus_lines)
                return FlextResult.ok(prometheus_output)

        except (ValueError, TypeError, ArithmeticError) as e:
            return FlextResult.fail(f"Failed to export Prometheus format: {e}")

    def reset_metrics(self) -> FlextResult[None]:
        """Reset all metrics (useful for testing and cleanup)."""
        try:
            with self._metrics_lock:
                self._metrics_store.clear()
                self._metric_counters.clear()
                self._metric_gauges.clear()
                self._metric_histograms.clear()
                self._metrics_recorded = 0
                self._start_time = time.time()

            self.logger.info("All metrics reset successfully")
            return FlextResult.ok(None)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Failed to reset metrics: {e}")


class FlextLoggingService:
    """Simplified logging service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize logging service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def log_entry(self, entry: FlextLogEntry) -> FlextResult[FlextLogEntry]:
        """Log entry using flext-core patterns."""
        try:
            level_method = getattr(self.logger, entry.level.lower(), self.logger.info)
            level_method(f"{entry.message} | Context: {entry.context}")
            return FlextResult.ok(entry)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "logging",
                f"Failed to log entry: {e}",
                log_level=entry.level,
                log_message=entry.message[:100],
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextTracingService:
    """Real distributed tracing service implementing OpenTelemetry-compatible tracing.

    Implements Single Responsibility (trace management),
    Open/Closed (extensible span types),
    Liskov Substitution (trace interface compliance),
    Interface Segregation (focused tracing API),
    and Dependency Inversion (depends on trace abstractions).
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize tracing service with real span tracking and correlation."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

        # Real trace storage with thread safety (Single Responsibility)
        self._active_traces: dict[str, dict[str, object]] = {}
        self._completed_traces: dict[str, dict[str, object]] = {}
        self._trace_spans: dict[str, list[dict[str, object]]] = defaultdict(list)
        self._traces_lock = threading.RLock()

        # Correlation tracking for distributed tracing
        self._trace_hierarchy: dict[str, list[str]] = defaultdict(list)
        self._span_relationships: dict[str, str] = {}  # span_id -> parent_span_id

        # Service metrics
        self._traces_started = 0
        self._traces_completed = 0
        self._service_start_time = time.time()

    def start_trace(self, trace: FlextTrace) -> FlextResult[FlextTrace]:
        """Start distributed trace with real span tracking and correlation."""
        try:
            # Input validation (defensive programming)
            if (
                not trace
                or not hasattr(trace, "trace_id")
                or not hasattr(trace, "operation")
            ):
                return FlextResult.fail("Invalid trace: missing trace_id or operation")

            if not trace.trace_id or not isinstance(trace.trace_id, str):
                return FlextResult.fail("Trace ID must be a non-empty string")

            # Real trace management with thread safety
            with self._traces_lock:
                start_time = time.time()

                # Create comprehensive trace context
                trace_context: dict[str, object] = {
                    "trace_id": trace.trace_id,
                    "operation": trace.operation,
                    "start_time": start_time,
                    "status": "active",
                    "service_name": getattr(
                        trace,
                        "service_name",
                        "flext-observability",
                    ),
                    "parent_trace_id": getattr(trace, "parent_trace_id", None),
                    "correlation_id": getattr(trace, "correlation_id", trace.trace_id),
                    "attributes": getattr(trace, "attributes", {}),
                    "resource": getattr(trace, "resource", {}),
                    "spans": [],
                }

                # Handle trace hierarchy for distributed tracing
                parent_trace_id = trace_context.get("parent_trace_id")
                if parent_trace_id and isinstance(parent_trace_id, str):
                    self._trace_hierarchy[parent_trace_id].append(trace.trace_id)

                # Store active trace
                self._active_traces[trace.trace_id] = trace_context
                self._traces_started += 1

            # Structured logging with distributed tracing context
            self.logger.info(
                "Distributed trace started successfully",
                trace_id=trace.trace_id,
                operation=trace.operation,
                parent_trace_id=parent_trace_id,
                correlation_id=trace_context["correlation_id"],
                start_time=start_time,
            )

            return FlextResult.ok(trace)

        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "tracing",
                f"Failed to start trace: {e}",
                trace_id=getattr(trace, "trace_id", "unknown"),
                operation=getattr(trace, "operation", "unknown"),
            )
            return FlextResult.fail(error_result.error or "Unknown error")

    def add_span_to_trace(
        self,
        trace_id: str,
        span_name: str,
        **span_attributes: object,
    ) -> FlextResult[dict[str, object]]:
        """Add span to existing trace with real span tracking."""
        try:
            with self._traces_lock:
                if trace_id not in self._active_traces:
                    return FlextResult.fail(
                        f"Trace '{trace_id}' not found or not active",
                    )

                span_id = f"{trace_id}_{len(self._trace_spans[trace_id])}"
                span_start_time = time.time()

                # Create comprehensive span
                span = {
                    "span_id": span_id,
                    "trace_id": trace_id,
                    "name": span_name,
                    "start_time": span_start_time,
                    "status": "active",
                    "attributes": dict(span_attributes),
                    "events": [],
                    "parent_span_id": None,  # Can be extended for nested spans
                }

                # Add span to trace
                self._trace_spans[trace_id].append(span)
                spans_list = self._active_traces[trace_id]["spans"]
                if isinstance(spans_list, list):
                    cast("list[str]", spans_list).append(span_id)

                return FlextResult.ok(span)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult.fail(f"Failed to add span to trace '{trace_id}': {e}")

    def finish_trace(
        self,
        trace_id: str,
        status: str = "completed",
    ) -> FlextResult[dict[str, object]]:
        """Finish trace with comprehensive context and timing."""
        try:
            with self._traces_lock:
                if trace_id not in self._active_traces:
                    return FlextResult.fail(
                        f"Trace '{trace_id}' not found or not active",
                    )

                # Complete the trace
                trace_context = self._active_traces[trace_id]
                end_time = time.time()
                start_time = trace_context["start_time"]
                duration = end_time - (
                    start_time if isinstance(start_time, (int, float)) else 0
                )

                # Update trace with completion info
                trace_context.update(
                    {
                        "end_time": end_time,
                        "duration_seconds": duration,
                        "status": status,
                        "span_count": len(self._trace_spans[trace_id]),
                    },
                )

                # Move to completed traces
                self._completed_traces[trace_id] = trace_context
                del self._active_traces[trace_id]
                self._traces_completed += 1

                # Log trace completion
                self.logger.info(
                    "Distributed trace completed",
                    trace_id=trace_id,
                    operation=trace_context["operation"],
                    duration_seconds=duration,
                    span_count=trace_context["span_count"],
                    status=status,
                )

                return FlextResult.ok(trace_context)

        except (ValueError, TypeError, KeyError, ArithmeticError) as e:
            return FlextResult.fail(f"Failed to finish trace '{trace_id}': {e}")

    def get_trace_info(self, trace_id: str) -> FlextResult[dict[str, object]]:
        """Get comprehensive trace information including spans."""
        try:
            with self._traces_lock:
                # Check active traces first
                if trace_id in self._active_traces:
                    trace_info = self._active_traces[trace_id].copy()
                    trace_info["trace_spans"] = self._trace_spans.get(trace_id, [])
                    trace_info["child_traces"] = self._trace_hierarchy.get(trace_id, [])
                    return FlextResult.ok(trace_info)

                # Check completed traces
                if trace_id in self._completed_traces:
                    trace_info = self._completed_traces[trace_id].copy()
                    trace_info["trace_spans"] = self._trace_spans.get(trace_id, [])
                    trace_info["child_traces"] = self._trace_hierarchy.get(trace_id, [])
                    return FlextResult.ok(trace_info)

                return FlextResult.fail(f"Trace '{trace_id}' not found")

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult.fail(f"Failed to get trace info for '{trace_id}': {e}")

    def export_jaeger_format(self, trace_id: str) -> FlextResult[dict[str, object]]:
        """Export trace in Jaeger-compatible format for real integration."""
        try:
            trace_info_result = self.get_trace_info(trace_id)
            if trace_info_result.is_failure:
                return trace_info_result

            trace_info = trace_info_result.data
            if trace_info is None:
                return FlextResult.fail(f"No trace data found for '{trace_id}'")

            # Create Jaeger-compatible format
            jaeger_trace = {
                "traceID": trace_id,
                "spans": [
                    {
                        "traceID": trace_id,
                        "spanID": span.get("span_id", ""),
                        "operationName": span.get("name", ""),
                        "startTime": int(
                            cast("float", span.get("start_time") or 0) * 1_000_000
                            if isinstance(span.get("start_time"), (int, float))
                            else 0,
                        ),  # microseconds
                        "duration": int(
                            cast("float", span.get("duration_seconds") or 0) * 1_000_000
                            if isinstance(span.get("duration_seconds"), (int, float))
                            else 0,
                        ),
                        "tags": [
                            {"key": k, "value": str(v)}
                            for k, v in cast(
                                "dict[str, object]",
                                span.get("attributes") or {},
                            ).items()
                        ],
                        "process": {
                            "serviceName": trace_info.get(
                                "service_name",
                                "flext-observability",
                            ),
                            "tags": [],
                        },
                    }
                    for span in cast(
                        "list[dict[str, object]]",
                        trace_info.get("trace_spans") or [],
                    )
                    if isinstance(span, dict)
                ],
                "processes": {
                    "p1": {
                        "serviceName": trace_info.get(
                            "service_name",
                            "flext-observability",
                        ),
                        "tags": [],
                    },
                },
            }

            return FlextResult.ok(cast("dict[str, object]", jaeger_trace))

        except (ValueError, TypeError, KeyError, ArithmeticError) as e:
            return FlextResult.fail(
                f"Failed to export Jaeger format for trace '{trace_id}': {e}",
            )

    def get_tracing_summary(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive tracing service summary with statistics."""
        try:
            with self._traces_lock:
                current_time = time.time()
                uptime = current_time - self._service_start_time

                summary = {
                    "service_info": {
                        "uptime_seconds": uptime,
                        "traces_started": self._traces_started,
                        "traces_completed": self._traces_completed,
                        "active_traces": len(self._active_traces),
                        "total_spans": sum(
                            len(spans) for spans in self._trace_spans.values()
                        ),
                    },
                    "active_traces": list(self._active_traces.keys()),
                    "trace_hierarchy_count": len(self._trace_hierarchy),
                    "performance_metrics": {
                        "avg_traces_per_second": self._traces_started / uptime
                        if uptime > 0
                        else 0,
                        "completion_rate": (
                            self._traces_completed / self._traces_started
                            if self._traces_started > 0
                            else 0
                        ),
                    },
                }

                return FlextResult.ok(summary)

        except (ValueError, TypeError, ArithmeticError) as e:
            return FlextResult.fail(f"Failed to generate tracing summary: {e}")


class FlextAlertService:
    """Simplified alert service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize alert service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def create_alert(self, alert: FlextAlert) -> FlextResult[FlextAlert]:
        """Create alert using flext-core patterns."""
        try:
            self.logger.warning(
                f"Alert created: {alert.title} | Severity: {alert.severity}",
            )
            return FlextResult.ok(alert)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "alert",
                f"Failed to create alert: {e}",
                alert_title=alert.title,
                alert_severity=alert.severity,
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextHealthService:
    """Real health monitoring service implementing comprehensive health checks.

    Implements Single Responsibility (health monitoring),
    Open/Closed (extensible health checks),
    Liskov Substitution (health interface compliance),
    Interface Segregation (focused health API),
    and Dependency Inversion (depends on health abstractions).
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize health service with real monitoring and alerting."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

        # Real health monitoring with thread safety (Single Responsibility)
        self._component_health: dict[str, dict[str, object]] = {}
        self._health_history: dict[str, list[dict[str, object]]] = defaultdict(list)
        self._health_lock = threading.RLock()

        # Health monitoring configuration
        self._health_check_interval = 30  # seconds
        self._max_history_entries = 100
        self._unhealthy_threshold = 3  # consecutive failures

        # Service metrics
        self._total_health_checks = 0
        self._healthy_components: set[str] = set()
        self._unhealthy_components: set[str] = set()
        self._service_start_time = time.time()

    def _extract_actual_health(
        self,
        health: FlextHealthCheck | FlextResult[FlextHealthCheck],
    ) -> FlextResult[FlextHealthCheck]:
        """Extract actual health check from various input types."""
        if isinstance(health, FlextResult):
            if health.is_failure:
                return FlextResult.fail(health.error or "Health check creation failed")
            if health.data is None:
                return FlextResult.fail("Health check data is None")
            return FlextResult.ok(health.data)
        return FlextResult.ok(health)

    def _create_health_record(
        self,
        actual_health: FlextHealthCheck,
        check_time: float,
    ) -> dict[str, object]:
        """Create comprehensive health record."""
        return {
            "component": actual_health.component,
            "status": getattr(actual_health, "status", "unknown"),
            "check_time": check_time,
            "details": getattr(actual_health, "details", {}),
            "metrics": getattr(actual_health, "metrics", {}),
            "error_message": getattr(actual_health, "error_message", None),
            "response_time_ms": getattr(actual_health, "response_time_ms", None),
        }

    def _update_component_health_sets(
        self,
        component_name: str,
        health_status: str,
    ) -> None:
        """Update component health sets based on status."""
        if health_status in {"healthy", "ok", "up"}:
            self._healthy_components.add(component_name)
            self._unhealthy_components.discard(component_name)
        else:
            self._unhealthy_components.add(component_name)
            self._healthy_components.discard(component_name)

    def _check_persistent_unhealthy(
        self,
        component_name: str,
        health_status: str,
    ) -> None:
        """Check for persistent unhealthy status and log warnings."""
        recent_checks = self._health_history[component_name][
            -self._unhealthy_threshold :
        ]
        if len(recent_checks) >= self._unhealthy_threshold and all(
            check["status"] not in {"healthy", "ok", "up"} for check in recent_checks
        ):
            self.logger.warning(
                "Component consistently unhealthy",
                component=component_name,
                consecutive_failures=len(recent_checks),
                last_status=health_status,
            )

    def check_health(
        self,
        health: FlextHealthCheck | FlextResult[FlextHealthCheck],
    ) -> FlextResult[FlextHealthCheck]:
        """Perform comprehensive health check with real monitoring and history."""
        try:
            # Extract actual health check (reduced complexity)
            actual_health_result = self._extract_actual_health(health)
            if actual_health_result.is_failure:
                return actual_health_result

            actual_health = actual_health_result.data

            # Input validation (defensive programming)
            if not actual_health or not hasattr(actual_health, "component"):
                return FlextResult.fail("Invalid health check: missing component")

            component_name = actual_health.component
            health_status = getattr(actual_health, "status", "unknown")

            # Real health monitoring with thread safety
            with self._health_lock:
                check_time = time.time()

                # Create and store health record
                health_record = self._create_health_record(actual_health, check_time)
                self._component_health[component_name] = health_record
                self._health_history[component_name].append(health_record)

                # Maintain history size (prevent memory leaks)
                history_length = len(self._health_history[component_name])
                if history_length > self._max_history_entries:
                    self._health_history[component_name] = self._health_history[
                        component_name
                    ][-self._max_history_entries // 2 :]

                # Update component health sets
                self._update_component_health_sets(component_name, health_status)
                self._total_health_checks += 1

                # Check for persistent unhealthy status
                self._check_persistent_unhealthy(component_name, health_status)

            # Structured logging with health context
            self.logger.info(
                "Health check completed",
                component=component_name,
                status=health_status,
                check_time=check_time,
                response_time_ms=health_record.get("response_time_ms"),
                total_checks=self._total_health_checks,
            )

            return FlextResult.ok(actual_health)

        except (ValueError, TypeError, AttributeError) as e:
            # Safe access to health data for error reporting
            component_name = "unknown"
            health_status = "unknown"
            try:
                if (
                    isinstance(health, FlextResult)
                    and health.is_success
                    and health.data
                ):
                    component_name = health.data.component
                    health_status = health.data.status
                elif not isinstance(health, FlextResult):
                    component_name = health.component
                    health_status = health.status
            except (AttributeError, TypeError):
                pass  # Use defaults

            error_result = create_observability_result_error(
                "health_check",
                f"Failed to check health: {e}",
                component_name=component_name,
                health_status=health_status,
            )
            return FlextResult.fail(error_result.error or "Unknown error")

    def get_overall_health(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive overall system health with detailed component status."""
        try:
            with self._health_lock:
                current_time = time.time()
                uptime = current_time - self._service_start_time

                # Calculate overall health status
                total_components = len(self._component_health)
                healthy_count = len(self._healthy_components)
                unhealthy_count = len(self._unhealthy_components)

                # Determine overall status
                if total_components == 0:
                    overall_status = "unknown"
                elif unhealthy_count == 0:
                    overall_status = "healthy"
                elif unhealthy_count < total_components / 2:
                    overall_status = "degraded"
                else:
                    overall_status = "unhealthy"

                # Create comprehensive health summary
                health_summary = {
                    "overall_status": overall_status,
                    "timestamp": current_time,
                    "uptime_seconds": uptime,
                    "summary": {
                        "total_components": total_components,
                        "healthy_components": healthy_count,
                        "unhealthy_components": unhealthy_count,
                        "health_checks_performed": self._total_health_checks,
                    },
                    "components": dict(self._component_health),
                    "healthy_components": list(self._healthy_components),
                    "unhealthy_components": list(self._unhealthy_components),
                    "service_metrics": {
                        "avg_checks_per_second": self._total_health_checks / uptime
                        if uptime > 0
                        else 0,
                        "health_check_interval_seconds": self._health_check_interval,
                        "history_retention_count": self._max_history_entries,
                    },
                }

                return FlextResult.ok(health_summary)

        except (ValueError, TypeError, AttributeError, ArithmeticError) as e:
            error_result = create_observability_result_error(
                "health_check",
                f"Failed to get overall health: {e}",
            )
            return FlextResult.fail(error_result.error or "Unknown error")

    def get_component_health_history(
        self,
        component_name: str,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get health history for a specific component."""
        try:
            with self._health_lock:
                if component_name not in self._health_history:
                    return FlextResult.fail(
                        f"No health history found for component '{component_name}'",
                    )

                history = self._health_history[component_name].copy()
                return FlextResult.ok(history)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult.fail(
                f"Failed to get health history for '{component_name}': {e}",
            )

    def perform_system_health_check(self) -> FlextResult[dict[str, object]]:
        """Perform comprehensive system health checks including infrastructure."""
        try:
            system_checks = {}

            # Memory usage check - psutil is a required dependency
            memory = psutil.virtual_memory()
            memory_status = (
                "healthy"
                if memory.percent < MEMORY_WARNING_THRESHOLD
                else "warning"
                if memory.percent < MEMORY_CRITICAL_THRESHOLD
                else "critical"
            )
            system_checks["memory"] = {
                "status": memory_status,
                "used_percent": memory.percent,
                "available_gb": memory.available / (1024**3),
            }

            # Disk usage check
            try:
                import shutil  # noqa: PLC0415 - Dynamic import for disk operations

                disk_usage = shutil.disk_usage("/")
                used_percent = (disk_usage.used / disk_usage.total) * 100
                disk_status = (
                    "healthy"
                    if used_percent < DISK_WARNING_THRESHOLD
                    else "warning"
                    if used_percent < DISK_CRITICAL_THRESHOLD
                    else "critical"
                )
                system_checks["disk"] = {
                    "status": disk_status,
                    "used_percent": used_percent,
                    "free_gb": disk_usage.free / (1024**3),
                }
            except (OSError, AttributeError):
                system_checks["disk"] = {
                    "status": "unknown",
                    "error": "disk check failed",
                }

            # Thread count check
            thread_count = threading.active_count()
            thread_status = (
                "healthy"
                if thread_count < THREAD_WARNING_THRESHOLD
                else "warning"
                if thread_count < THREAD_CRITICAL_THRESHOLD
                else "critical"
            )
            system_checks["threads"] = {
                "status": thread_status,
                "active_count": thread_count,
            }

            # Service availability check
            system_checks["observability_service"] = {
                "status": "healthy",
                "uptime_seconds": time.time() - self._service_start_time,
                "total_health_checks": self._total_health_checks,
            }

            return FlextResult.ok(cast("dict[str, object]", system_checks))

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"System health check failed: {e}")
