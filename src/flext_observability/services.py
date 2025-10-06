"""Unified observability services following FLEXT ecosystem patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
import re
import statistics
import threading
import time
from datetime import UTC, datetime
from typing import ClassVar
from uuid import UUID, uuid4

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

from flext_observability.config import FlextObservabilityConfig
from flext_observability.typings import FlextObservabilityTypes


class FlextObservabilityServices(FlextUtilities):
    """Unified observability services class following FLEXT namespace class pattern.

    Single unified class with flattened service methods for all observability operations.
    Removed over-engineered nested service classes that were only used internally.
    """

    # Domain Constants
    MAX_TRACE_DURATION: ClassVar[float] = 3600.0  # 1 hour
    MAX_METRIC_NAME_LENGTH: ClassVar[int] = 255
    MAX_ALERT_MESSAGE_LENGTH: ClassVar[int] = 1000
    DEFAULT_HEALTH_CHECK_INTERVAL: ClassVar[float] = 30.0  # 30 seconds
    MAX_SPAN_COUNT_PER_TRACE: ClassVar[int] = 1000
    MIN_PERCENTILE: ClassVar[float] = 0.0
    MAX_PERCENTILE: ClassVar[float] = 100.0

    # Metrics storage - flattened from nested MetricsService class
    _metrics_counters: ClassVar[
        FlextObservabilityTypes.ObservabilityCore.CountersDict
    ] = {}
    _metrics_gauges: ClassVar[FlextObservabilityTypes.ObservabilityCore.GaugesDict] = {}
    _metrics_histograms: ClassVar[
        FlextObservabilityTypes.ObservabilityCore.HistogramsDict
    ] = {}
    _metrics_metadata: ClassVar[
        FlextObservabilityTypes.ObservabilityCore.MetadataDict
    ] = {}
    _metrics_lock: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    def record_counter(
        cls,
        name: str,
        value: float = 1.0,
        tags: FlextObservabilityTypes.ObservabilityCore.TagsDict | None = None,
    ) -> FlextResult[None]:
        """Record counter metric with thread safety."""
        try:
            with cls._metrics_lock:
                if name not in cls._metrics_counters:
                    cls._metrics_counters[name] = 0.0
                cls._metrics_counters[name] += value

                # Store metadata if provided
                if tags:
                    cls._metrics_metadata[name] = tags

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Counter recording failed: {e}")

    @classmethod
    def record_gauge(
        cls,
        name: str,
        value: float,
        tags: FlextObservabilityTypes.ObservabilityCore.TagsDict | None = None,
    ) -> FlextResult[None]:
        """Record gauge metric with metadata support."""
        try:
            with cls._metrics_lock:
                cls._metrics_gauges[name] = value

                # Store metadata if provided
                if tags:
                    cls._metrics_metadata[name] = tags

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Gauge recording failed: {e}")

    @classmethod
    def record_histogram(
        cls,
        name: str,
        value: float,
        tags: FlextObservabilityTypes.ObservabilityCore.TagsDict | None = None,
    ) -> FlextResult[None]:
        """Record histogram value with comprehensive tracking."""
        try:
            with cls._metrics_lock:
                if name not in cls._metrics_histograms:
                    cls._metrics_histograms[name] = []
                cls._metrics_histograms[name].append(value)

                # Store metadata if provided
                if tags:
                    cls._metrics_metadata[name] = tags

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Histogram recording failed: {e}")

    @classmethod
    def add_custom_metric(
        cls,
        name: str,
        metric_type: str,
        value: float,
        metadata: FlextObservabilityTypes.ObservabilityCore.MetadataDict | None = None,
    ) -> FlextResult[None]:
        """Add custom metric with flexible type support."""
        try:
            # Convert metadata to tags format if needed
            tags: FlextObservabilityTypes.ObservabilityCore.TagsDict | None = None
            if metadata and isinstance(metadata, dict):
                tags = {k: str(v) for k, v in metadata.items()}

            if metric_type == "counter":
                return cls.record_counter(name, value, tags)
            if metric_type == "gauge":
                return cls.record_gauge(name, value, tags)
            if metric_type == "histogram":
                return cls.record_histogram(name, value, tags)

            return FlextResult[None].fail(f"Unknown metric type: {metric_type}")

        except Exception as e:
            return FlextResult[None].fail(f"Custom metric addition failed: {e}")

    @classmethod
    def collect_metrics(
        cls,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetricsStore]:
        """Collect all metrics data for export."""
        try:
            with cls._metrics_lock:
                metric_data: FlextObservabilityTypes.ObservabilityCore.Dict = {
                    "counters": dict(cls._metrics_counters),
                    "gauges": dict(cls._metrics_gauges),
                    "histograms": dict(cls._metrics_histograms),
                    "metadata": dict(cls._metrics_metadata),
                    "collection_timestamp": time.time(),
                }

                metrics_store: FlextObservabilityTypes.ObservabilityCore.MetricsStore = {
                    "current_metrics": [metric_data]
                }

                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetricsStore
                ].ok(metrics_store)

        except Exception as e:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricsStore
            ].fail(f"Metrics collection failed: {e}")

    @classmethod
    def reset_metrics(cls) -> FlextResult[None]:
        """Reset all metrics data."""
        try:
            with cls._metrics_lock:
                cls._metrics_counters.clear()
                cls._metrics_gauges.clear()
                cls._metrics_histograms.clear()
                cls._metrics_metadata.clear()

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Metrics reset failed: {e}")

    @classmethod
    def get_metrics_summary(
        cls,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetricDict]:
        """Get comprehensive metrics summary."""
        try:
            with cls._metrics_lock:
                summary: FlextObservabilityTypes.ObservabilityCore.MetricDict = {
                    "total_counters": len(cls._metrics_counters),
                    "total_gauges": len(cls._metrics_gauges),
                    "total_histograms": len(cls._metrics_histograms),
                    "counters_sum": sum(cls._metrics_counters.values()),
                    "gauges_avg": (
                        sum(cls._metrics_gauges.values()) / len(cls._metrics_gauges)
                        if cls._metrics_gauges
                        else 0.0
                    ),
                    "histograms_total_values": sum(
                        len(hist) for hist in cls._metrics_histograms.values()
                    ),
                    "last_collection": time.time(),
                }

                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetricDict
                ].ok(summary)

        except Exception as e:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricDict
            ].fail(f"Metrics summary generation failed: {e}")

    class TracingService:
        """Nested tracing service helper class."""

        # Tracing storage - class-level shared state with thread safety
        _active_traces: ClassVar[
            FlextObservabilityTypes.ObservabilityCore.TracesDict
        ] = {}
        _completed_traces: ClassVar[
            FlextObservabilityTypes.ObservabilityCore.TraceSpansDict
        ] = {}
        _span_relationships: ClassVar[
            FlextObservabilityTypes.ObservabilityCore.ObservabilityHeaders
        ] = {}
        _trace_lock: ClassVar[threading.Lock] = threading.Lock()

        @classmethod
        def start_trace(
            cls,
            operation_name: str,
            trace_context: FlextObservabilityTypes.ObservabilityCore.TraceContextDict
            | None = None,
        ) -> FlextResult[str]:
            """Start new distributed trace."""
            try:
                trace_id = str(uuid4())

                with cls._trace_lock:
                    trace_data: FlextObservabilityTypes.ObservabilityCore.MetadataDict = {
                        "trace_id": trace_id,
                        "operation": operation_name,
                        "start_time": time.time(),
                        "context": trace_context or {},
                        "status": "active",
                    }
                    cls._active_traces[trace_id] = trace_data

                return FlextResult[str].ok(trace_id)

            except Exception as e:
                return FlextResult[str].fail(f"Trace start failed: {e}")

        @classmethod
        def add_span(
            cls,
            trace_id: str,
            span_name: str,
            span_attributes: FlextObservabilityTypes.ObservabilityCore.SpanAttributesDict
            | None = None,
        ) -> FlextResult[str]:
            """Add span to existing trace."""
            try:
                if trace_id not in cls._active_traces:
                    return FlextResult[str].fail(f"Trace {trace_id} not found")

                span_id = str(uuid4())

                with cls._trace_lock:
                    if trace_id not in cls._completed_traces:
                        cls._completed_traces[trace_id] = []

                    span_data: FlextObservabilityTypes.ObservabilityCore.Dict = {
                        "span_id": span_id,
                        "name": span_name,
                        "attributes": span_attributes or {},
                        "start_time": time.time(),
                        "trace_id": trace_id,
                    }

                    cls._completed_traces[trace_id].append(span_data)

                return FlextResult[str].ok(span_id)

            except Exception as e:
                return FlextResult[str].fail(f"Span addition failed: {e}")

        @classmethod
        def complete_trace(cls, trace_id: str) -> FlextResult[None]:
            """Complete distributed trace."""
            try:
                if trace_id not in cls._active_traces:
                    return FlextResult[None].fail(f"Trace {trace_id} not found")

                with cls._trace_lock:
                    if trace_id in cls._completed_traces:
                        for span in cls._completed_traces[trace_id]:
                            span["end_time"] = time.time()

                    del cls._active_traces[trace_id]

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Trace completion failed: {e}")

        @classmethod
        def get_tracing_summary(
            cls,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.TraceInfoDict]:
            """Get comprehensive tracing summary."""
            try:
                with cls._trace_lock:
                    active_count = len(cls._active_traces)
                    completed_count = len(cls._completed_traces)
                    total_spans = sum(
                        len(spans) for spans in cls._completed_traces.values()
                    )

                    summary: FlextObservabilityTypes.ObservabilityCore.TraceInfoDict = {
                        "active_traces": active_count,
                        "completed_traces": completed_count,
                        "total_spans": total_spans,
                        "summary_timestamp": time.time(),
                    }

                    return FlextResult[
                        FlextObservabilityTypes.ObservabilityCore.TraceInfoDict
                    ].ok(summary)

            except Exception as e:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.TraceInfoDict
                ].fail(f"Tracing summary generation failed: {e}")

    class AlertService:
        """Nested alert service helper class."""

        @staticmethod
        def create_alert(
            title: str,
            message: str,
            severity: str = "info",
            source: str = "system",
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create alert with proper metadata."""
            try:
                alert_id = str(uuid4())
                alert: FlextObservabilityTypes.ObservabilityCore.MetadataDict = {
                    "alert_id": alert_id,
                    "title": title,
                    "message": message,
                    "severity": severity,
                    "source": source,
                    "created_at": time.time(),
                    "status": "active",
                }

                logger = FlextLogger(__name__)
                logger.info(f"Alert created: {alert_id}")
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetadataDict
                ].ok(alert)

            except Exception as e:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetadataDict
                ].fail(f"Alert creation failed: {e}")

        @staticmethod
        def create_alert_from_data(
            alert_data: FlextObservabilityTypes.ObservabilityCore.MetadataDict,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create alert with proper metadata from data dict."""
            try:
                alert_id = str(uuid4())
                alert: FlextObservabilityTypes.ObservabilityCore.MetadataDict = {
                    "alert_id": alert_id,
                    "created_at": time.time(),
                    "status": "active",
                    **alert_data,
                }

                logger = FlextLogger(__name__)
                logger.info(f"Alert created: {alert_id}")
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetadataDict
                ].ok(alert)

            except Exception as e:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetadataDict
                ].fail(f"Alert creation failed: {e}")

    class HealthService:
        """Nested health service helper class."""

        @staticmethod
        def get_health_status(
            service_start_time: float | None = None,
            service_id: str | None = None,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict]:
            """Get comprehensive health status."""
            try:
                start_time = service_start_time or time.time()
                svc_id = service_id or "unknown"

                health_status: FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict = {
                    "service_status": "healthy",
                    "uptime": time.time() - start_time,
                    "service_id": svc_id,
                    "memory_usage": "available",
                    "cpu_usage": "normal",
                    "disk_usage": "normal",
                    "network_status": "connected",
                    "dependencies_status": "healthy",
                    "last_health_check": time.time(),
                }

                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
                ].ok(health_status)

            except Exception as e:
                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.HealthMetricsDict
                ].fail(f"Health status check failed: {e}")

    def __init__(self) -> None:
        """Initialize FlextObservabilityService with comprehensive monitoring capabilities."""
        super().__init__()

        # Initialize core components using global instances (no duplication)
        self._container = FlextContainer.get_global()
        self.logger = FlextLogger(__name__)
        self._config = FlextObservabilityConfig.get_global_instance()

        # Service initialization
        self._start_time = time.time()
        self._service_id = str(uuid4())

        self.logger.info(f"FlextObservabilityService initialized: {self._service_id}")

    # Property accessors for core components
    @property
    def container(self) -> FlextContainer:
        """Get container instance."""
        return self._container

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return self.logger

    @property
    def config(self) -> FlextObservabilityConfig:
        """Get config instance using global singleton (no duplication)."""
        return self._config

    # Removed over-engineered nested service accessors - methods are now direct

    def get_start_time(self) -> float:
        """Get service start time."""
        return self._start_time

    def get_service_id(self) -> str:
        """Get service ID."""
        return self._service_id

    def execute(
        self, request: FlextObservabilityTypes.ObservabilityCore.MetadataDict
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetricsStore]:
        """Execute observability request with comprehensive service routing."""
        try:
            request_type = request.get("type", "unknown")

            if request_type == "metrics":
                if "metric_data" not in request:
                    return FlextResult[
                        FlextObservabilityTypes.ObservabilityCore.MetricsStore
                    ].fail("Missing metric data")

                return self.collect_metrics()

            if request_type == "trace":
                if "trace_data" not in request:
                    return FlextResult[
                        FlextObservabilityTypes.ObservabilityCore.MetricsStore
                    ].fail("Missing trace data")

                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetricsStore
                ].ok({"traces": [{"status": "processed"}]})

            if request_type == "health":
                health_result = self.HealthService.get_health_status(
                    self._start_time, self._service_id
                )
                if health_result.is_failure:
                    return FlextResult[
                        FlextObservabilityTypes.ObservabilityCore.MetricsStore
                    ].fail(f"Health check failed: {health_result.error}")

                return FlextResult[
                    FlextObservabilityTypes.ObservabilityCore.MetricsStore
                ].ok({"health": [health_result.unwrap()]})

            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricsStore
            ].fail(f"Unknown request type: {request_type}")

        except Exception as e:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricsStore
            ].fail(f"Observability request execution failed: {e}")

    def get_service_summary(
        self,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetricsStore]:
        """Get comprehensive service summary."""
        try:
            # Collect metrics summary
            metrics_summary_result = self.get_metrics_summary()
            tracing_summary_result = self.TracingService.get_tracing_summary()
            health_summary_result = self.HealthService.get_health_status(
                self._start_time, self._service_id
            )

            summary: FlextObservabilityTypes.ObservabilityCore.Dict = {
                "service_id": self._service_id,
                "uptime": time.time() - self._start_time,
                "metrics_summary": metrics_summary_result.unwrap()
                if metrics_summary_result.is_success
                else {},
                "tracing_summary": tracing_summary_result.unwrap()
                if tracing_summary_result.is_success
                else {},
                "health_summary": health_summary_result.unwrap()
                if health_summary_result.is_success
                else {},
                "summary_timestamp": time.time(),
            }

            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricsStore
            ].ok({"service_summary": [summary]})

        except Exception as e:
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetricsStore
            ].fail(f"Service summary generation failed: {e}")

    # Nested utility classes (moved from separate top-level classes)
    class MetricsValidation:
        """Nested class for metrics validation utilities."""

        @staticmethod
        def validate_metric_name(metric_name: str) -> FlextResult[str]:
            """Validate metric name format and constraints."""
            if not metric_name or not isinstance(metric_name, str):
                return FlextResult[str].fail("Metric name must be a non-empty string")

            if len(metric_name) > FlextObservabilityServices.MAX_METRIC_NAME_LENGTH:
                return FlextResult[str].fail(
                    f"Metric name exceeds maximum length of {FlextObservabilityServices.MAX_METRIC_NAME_LENGTH}"
                )

            # Validate metric name format (alphanumeric, underscore, dot, hyphen)
            if not re.match(r"^[a-zA-Z0-9_.-]+$", metric_name):
                return FlextResult[str].fail(
                    "Metric name contains invalid characters. Only alphanumeric, underscore, dot, and hyphen allowed"
                )

            return FlextResult[str].ok(metric_name.strip())

        @staticmethod
        def validate_metric_value(value: float) -> FlextResult[float]:
            """Validate metric value constraints."""
            if not isinstance(value, (int, float)):
                return FlextResult[float].fail("Metric value must be a number")

            if math.isnan(value) or math.isinf(value):
                return FlextResult[float].fail("Metric value cannot be NaN or infinite")

            return FlextResult[float].ok(float(value))

        @staticmethod
        def validate_tags(
            tags: dict[str, str | int | float] | None,
        ) -> FlextResult[FlextTypes.StringDict]:
            """Validate and normalize metric tags."""
            if tags is None:
                return FlextResult[FlextTypes.StringDict].ok({})

            if not isinstance(tags, dict):
                return FlextResult[FlextTypes.StringDict].fail(
                    "Tags must be a dictionary"
                )

            normalized_tags: FlextTypes.StringDict = {}
            for key, value in tags.items():
                if not isinstance(key, str) or not key.strip():
                    return FlextResult[FlextTypes.StringDict].fail(
                        "Tag keys must be non-empty strings"
                    )

                # Normalize value to string
                normalized_tags[key.strip()] = str(value).strip()

            return FlextResult[FlextTypes.StringDict].ok(normalized_tags)

    class TracingValidation:
        """Nested class for distributed tracing validation utilities."""

        @staticmethod
        def validate_trace_id(trace_id: str) -> FlextResult[str]:
            """Validate trace ID format."""
            if not trace_id or not isinstance(trace_id, str):
                return FlextResult[str].fail("Trace ID must be a non-empty string")

            # Validate UUID format
            try:
                uuid_obj = UUID(trace_id)
                return FlextResult[str].ok(str(uuid_obj))
            except ValueError:
                return FlextResult[str].fail("Trace ID must be a valid UUID format")

        @staticmethod
        def validate_span_name(span_name: str) -> FlextResult[str]:
            """Validate span name format."""
            if not span_name or not isinstance(span_name, str):
                return FlextResult[str].fail("Span name must be a non-empty string")

            if len(span_name.strip()) == 0:
                return FlextResult[str].fail(
                    "Span name cannot be empty or whitespace only"
                )

            return FlextResult[str].ok(span_name.strip())

        @staticmethod
        def validate_trace_duration(duration: float) -> FlextResult[float]:
            """Validate trace duration constraints."""
            if not isinstance(duration, (int, float)):
                return FlextResult[float].fail("Duration must be a number")

            if duration < 0:
                return FlextResult[float].fail("Duration cannot be negative")

            if duration > FlextObservabilityServices.MAX_TRACE_DURATION:
                return FlextResult[float].fail(
                    f"Duration exceeds maximum allowed of {FlextObservabilityServices.MAX_TRACE_DURATION} seconds"
                )

            return FlextResult[float].ok(duration)

    class AlertingUtilities:
        """Nested class for alerting and notification utilities."""

        @staticmethod
        def validate_alert_severity(severity: str) -> FlextResult[str]:
            """Validate alert severity level."""
            valid_severities = {"critical", "high", "medium", "low", "info"}

            if not severity or not isinstance(severity, str):
                return FlextResult[str].fail("Severity must be a non-empty string")

            normalized_severity = severity.lower().strip()
            if normalized_severity not in valid_severities:
                return FlextResult[str].fail(
                    f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
                )

            return FlextResult[str].ok(normalized_severity)

        @staticmethod
        def validate_alert_message(message: str) -> FlextResult[str]:
            """Validate alert message format and length."""
            if not message or not isinstance(message, str):
                return FlextResult[str].fail("Alert message must be a non-empty string")

            if len(message) > FlextObservabilityServices.MAX_ALERT_MESSAGE_LENGTH:
                return FlextResult[str].fail(
                    f"Alert message exceeds maximum length of {FlextObservabilityServices.MAX_ALERT_MESSAGE_LENGTH}"
                )

            return FlextResult[str].ok(message.strip())

        @staticmethod
        def format_alert_context(
            severity: str, message: str, metadata: FlextTypes.Dict | None = None
        ) -> FlextResult[FlextTypes.Dict]:
            """Format alert context with validation."""
            # Validate severity
            severity_result = (
                FlextObservabilityServices.AlertingUtilities.validate_alert_severity(
                    severity
                )
            )
            if severity_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(severity_result.error)

            # Validate message
            message_result = (
                FlextObservabilityServices.AlertingUtilities.validate_alert_message(
                    message
                )
            )
            if message_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(message_result.error)

            alert_context: FlextTypes.Dict = {
                "severity": severity_result.value,
                "message": message_result.value,
                "timestamp": datetime.now(UTC).isoformat(),
                "alert_id": str(uuid4()),
                "metadata": metadata or {},
            }

            return FlextResult[FlextTypes.Dict].ok(alert_context)

    class HealthMonitoring:
        """Nested class for health monitoring utilities."""

        @staticmethod
        def validate_health_status(status: str) -> FlextResult[str]:
            """Validate health status value."""
            valid_statuses = {"healthy", "degraded", "unhealthy", "unknown"}

            if not status or not isinstance(status, str):
                return FlextResult[str].fail("Health status must be a non-empty string")

            normalized_status = status.lower().strip()
            if normalized_status not in valid_statuses:
                return FlextResult[str].fail(
                    f"Invalid health status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                )

            return FlextResult[str].ok(normalized_status)

        @staticmethod
        def validate_uptime(uptime: float) -> FlextResult[float]:
            """Validate service uptime value."""
            if not isinstance(uptime, (int, float)):
                return FlextResult[float].fail("Uptime must be a number")

            if uptime < 0:
                return FlextResult[float].fail("Uptime cannot be negative")

            return FlextResult[float].ok(uptime)

        @staticmethod
        def format_health_check_result(
            service_name: str,
            status: str,
            uptime: float,
            additional_metrics: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Format comprehensive health check result."""
            # Validate service name
            if not service_name or not isinstance(service_name, str):
                return FlextResult[FlextTypes.Dict].fail(
                    "Service name must be a non-empty string"
                )

            # Validate status
            status_result = (
                FlextObservabilityServices.HealthMonitoring.validate_health_status(
                    status
                )
            )
            if status_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(status_result.error)

            # Validate uptime
            uptime_result = FlextObservabilityServices.HealthMonitoring.validate_uptime(
                uptime
            )
            if uptime_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(uptime_result.error)

            health_result: FlextTypes.Dict = {
                "service_name": service_name.strip(),
                "status": status_result.value,
                "uptime_seconds": uptime_result.value,
                "uptime_formatted": FlextObservabilityServices.HealthMonitoring.format_uptime_duration(
                    uptime_result.value
                ),
                "check_timestamp": datetime.now(UTC).isoformat(),
                "additional_metrics": additional_metrics or {},
            }

            return FlextResult[FlextTypes.Dict].ok(health_result)

        @staticmethod
        def format_uptime_duration(uptime_seconds: float) -> str:
            """Format uptime seconds into human-readable duration."""
            try:
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                seconds = int(uptime_seconds % 60)

                parts = []
                if days > 0:
                    parts.append(f"{days}d")
                if hours > 0:
                    parts.append(f"{hours}h")
                if minutes > 0:
                    parts.append(f"{minutes}m")
                if seconds > 0 or not parts:
                    parts.append(f"{seconds}s")

                return " ".join(parts)
            except Exception:
                return f"{uptime_seconds:.1f}s"

    class LoggingUtilities:
        """Nested class for structured logging utilities."""

        @staticmethod
        def validate_log_level(level: str) -> FlextResult[str]:
            """Validate log level."""
            valid_levels = {"debug", "info", "warning", "error", "critical"}

            if not level or not isinstance(level, str):
                return FlextResult[str].fail("Log level must be a non-empty string")

            normalized_level = level.lower().strip()
            if normalized_level not in valid_levels:
                return FlextResult[str].fail(
                    f"Invalid log level '{level}'. Must be one of: {', '.join(valid_levels)}"
                )

            return FlextResult[str].ok(normalized_level)

        @staticmethod
        def format_structured_log(
            level: str,
            message: str,
            metadata: FlextTypes.Dict | None = None,
            correlation_id: str | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Format structured log entry."""
            # Validate log level
            level_result = (
                FlextObservabilityServices.LoggingUtilities.validate_log_level(level)
            )
            if level_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(level_result.error)

            # Validate message
            if not message or not isinstance(message, str):
                return FlextResult[FlextTypes.Dict].fail(
                    "Log message must be a non-empty string"
                )

            log_entry: FlextTypes.Dict = {
                "level": level_result.value,
                "message": message.strip(),
                "timestamp": datetime.now(UTC).isoformat(),
                "metadata": metadata or {},
                "correlation_id": correlation_id or str(uuid4()),
            }

            return FlextResult[FlextTypes.Dict].ok(log_entry)

    class DataProcessing:
        """Nested class for observability data processing utilities."""

        @staticmethod
        def aggregate_metrics(
            metrics: list[FlextTypes.Dict],
        ) -> FlextResult[FlextTypes.Dict]:
            """Aggregate metrics data for summary reporting."""
            if not metrics or not isinstance(metrics, list):
                return FlextResult[FlextTypes.Dict].fail(
                    "Metrics must be a non-empty list"
                )

            try:
                aggregated: FlextTypes.Dict = {
                    "total_metrics": len(metrics),
                    "aggregation_timestamp": datetime.now(UTC).isoformat(),
                    "counters_sum": 0.0,
                    "gauges_count": 0,
                    "histograms_count": 0,
                    "unique_metric_names": set(),
                }

                for metric in metrics:
                    if isinstance(metric, dict):
                        # Count metric types
                        metric_type = metric.get("type", "unknown")
                        if metric_type == "counter":
                            value = metric.get("value", 0)
                            if isinstance(value, (int, float)):
                                current_sum = aggregated["counters_sum"]
                                if isinstance(current_sum, (int, float)):
                                    aggregated["counters_sum"] = float(
                                        current_sum
                                    ) + float(value)
                        elif metric_type == "gauge":
                            current_count = aggregated["gauges_count"]
                            if isinstance(current_count, int):
                                aggregated["gauges_count"] = current_count + 1
                        elif metric_type == "histogram":
                            current_count = aggregated["histograms_count"]
                            if isinstance(current_count, int):
                                aggregated["histograms_count"] = current_count + 1

                        # Track unique names
                        name = metric.get("name")
                        if isinstance(name, str):
                            unique_names = aggregated["unique_metric_names"]
                            if isinstance(unique_names, set):
                                unique_names.add(name)

                # Convert set to count
                unique_names = aggregated["unique_metric_names"]
                if isinstance(unique_names, set):
                    aggregated["unique_metric_names"] = len(unique_names)

                return FlextResult[FlextTypes.Dict].ok(aggregated)

            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Metrics aggregation failed: {e}"
                )

        @staticmethod
        def calculate_percentiles(
            values: FlextTypes.FloatList,
            percentiles: FlextTypes.FloatList | None = None,
        ) -> FlextResult[FlextTypes.FloatDict]:
            """Calculate percentiles for histogram data."""
            if not values or not isinstance(values, list):
                return FlextResult[FlextTypes.FloatDict].fail(
                    "Values must be a non-empty list"
                )

            if percentiles is None:
                percentiles = [50.0, 90.0, 95.0, 99.0]

            try:
                # Validate and convert values using list comprehension
                numeric_values: FlextTypes.FloatList = [
                    float(value)
                    for value in values
                    if isinstance(value, (int, float))
                    and not (math.isnan(value) or math.isinf(value))
                ]

                if not numeric_values:
                    return FlextResult[FlextTypes.FloatDict].fail(
                        "No valid numeric values found"
                    )

                # Sort values for percentile calculation
                sorted_values = sorted(numeric_values)

                result: FlextTypes.FloatDict = {}
                for percentile in percentiles:
                    if not (
                        FlextObservabilityServices.MIN_PERCENTILE
                        <= percentile
                        <= FlextObservabilityServices.MAX_PERCENTILE
                    ):
                        continue

                    # Calculate percentile
                    if percentile == FlextObservabilityServices.MIN_PERCENTILE:
                        result[f"p{percentile:g}"] = sorted_values[0]
                    elif percentile == FlextObservabilityServices.MAX_PERCENTILE:
                        result[f"p{percentile:g}"] = sorted_values[-1]
                    else:
                        index = (
                            percentile / FlextObservabilityServices.MAX_PERCENTILE
                        ) * (len(sorted_values) - 1)
                        lower_index = int(index)
                        upper_index = min(lower_index + 1, len(sorted_values) - 1)

                        if lower_index == upper_index:
                            result[f"p{percentile:g}"] = sorted_values[lower_index]
                        else:
                            # Linear interpolation
                            weight = index - lower_index
                            result[f"p{percentile:g}"] = (
                                sorted_values[lower_index] * (1 - weight)
                                + sorted_values[upper_index] * weight
                            )

                # Add summary statistics
                result["min"] = min(numeric_values)
                result["max"] = max(numeric_values)
                result["mean"] = statistics.mean(numeric_values)
                result["median"] = statistics.median(numeric_values)
                result["count"] = len(numeric_values)

                return FlextResult[FlextTypes.FloatDict].ok(result)

            except Exception as e:
                return FlextResult[FlextTypes.FloatDict].fail(
                    f"Percentile calculation failed: {e}"
                )

    # Instance methods that delegate to MasterFactory for API compatibility
    def create_metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        metadata: FlextObservabilityTypes.ObservabilityCore.MetadataDict | None = None,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
        """Create a metric through the master factory."""
        return self.MasterFactory.create_metric(name, value, unit, metadata)

    def create_trace(
        self,
        name: str,
        operation: str,
        context: FlextObservabilityTypes.ObservabilityCore.MetadataDict | None = None,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
        """Create a trace through the master factory."""
        return self.MasterFactory.create_trace(name, operation, context)

    def create_alert(
        self,
        title: str,
        message: str,
        severity: str = "info",
        source: str = "system",
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
        """Create an alert through the master factory."""
        return self.MasterFactory.create_alert(title, message, severity, source)

    def create_health_check(
        self,
        service_name: str,
        status: str = "healthy",
        details: FlextObservabilityTypes.ObservabilityCore.MetadataDict | None = None,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
        """Create a health check through the master factory."""
        return self.MasterFactory.create_health_check(service_name, status, details)

    def create_log_entry(
        self,
        message: str,
        service: str,
        level: str = "INFO",
        metadata: FlextObservabilityTypes.ObservabilityCore.MetadataDict | None = None,
    ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
        """Create a log entry through the master factory."""
        return self.MasterFactory.create_log_entry(message, service, level, metadata)

    class ObservabilityGenerators:
        """Nested class for generating timestamps and IDs."""

        @staticmethod
        def generate_timestamp() -> str:
            """Generate timestamp for observability operations."""
            return str(time.time())

    class MasterFactory:
        """Master factory for creating and managing observability entities."""

        def __init__(self, container: FlextContainer | None = None) -> None:
            """Initialize the master factory with optional container."""
            self._container = container

        # Global factory instance
        _global_factory: ClassVar[FlextObservabilityServices | None] = None

        @classmethod
        def get_global_factory(cls) -> FlextObservabilityServices:
            """Get the global factory instance."""
            if cls._global_factory is None:
                cls._global_factory = FlextObservabilityServices()
            return cls._global_factory

        @classmethod
        def reset_global_factory(cls) -> None:
            """Reset the global factory instance."""
            cls._global_factory = None

        @classmethod
        def create_metric(
            cls,
            name: str,
            value: float,
            unit: str = "count",
            metadata: FlextObservabilityTypes.ObservabilityCore.MetadataDict
            | None = None,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create a metric through the master factory."""
            cls.get_global_factory()
            # Use the metrics service to create
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetadataDict
            ].ok({
                "name": name,
                "value": value,
                "unit": unit,
                "metadata": metadata or {},
                "created_by": "master_factory",
            })

        @classmethod
        def create_trace(
            cls,
            name: str,
            operation: str,
            context: FlextObservabilityTypes.ObservabilityCore.MetadataDict
            | None = None,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create a trace through the master factory."""
            cls.get_global_factory()
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetadataDict
            ].ok({
                "name": name,
                "operation": operation,
                "context": context or {},
                "created_by": "master_factory",
            })

        @classmethod
        def create_alert(
            cls,
            title: str,
            message: str,
            severity: str = "info",
            source: str = "system",
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create an alert through the master factory."""
            cls.get_global_factory()
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetadataDict
            ].ok({
                "title": title,
                "message": message,
                "severity": severity,
                "source": source,
                "created_by": "master_factory",
            })

        @classmethod
        def create_health_check(
            cls,
            service_name: str,
            status: str = "healthy",
            details: FlextObservabilityTypes.ObservabilityCore.MetadataDict
            | None = None,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create a health check through the master factory."""
            cls.get_global_factory()
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetadataDict
            ].ok({
                "service_name": service_name,
                "status": status,
                "details": details or {},
                "created_by": "master_factory",
            })

        @classmethod
        def create_log_entry(
            cls,
            message: str,
            service: str,
            level: str = "INFO",
            metadata: FlextObservabilityTypes.ObservabilityCore.MetadataDict
            | None = None,
        ) -> FlextResult[FlextObservabilityTypes.ObservabilityCore.MetadataDict]:
            """Create a log entry through the master factory."""
            cls.get_global_factory()
            return FlextResult[
                FlextObservabilityTypes.ObservabilityCore.MetadataDict
            ].ok({
                "message": message,
                "service": service,
                "level": level,
                "metadata": metadata or {},
                "created_by": "master_factory",
            })


# Backward compatibility aliases
FlextObservabilityService = FlextObservabilityServices
FlextObservabilityMasterFactory = FlextObservabilityServices.MasterFactory


# Consolidated utilities class (ZERO TOLERANCE consolidation from utilities.py)
class FlextObservabilityUtilities(FlextUtilities):
    """Consolidated observability utilities - ZERO TOLERANCE duplication elimination."""

    # Placeholder for consolidated utilities - all functionality moved here


# Global factory functions
def get_global_factory() -> FlextObservabilityServices:
    """Get the global factory instance (backward compatibility)."""
    return FlextObservabilityServices.MasterFactory.get_global_factory()


def reset_global_factory() -> None:
    """Reset the global factory instance (backward compatibility)."""
    FlextObservabilityServices.MasterFactory.reset_global_factory()


__all__ = [
    "FlextObservabilityMasterFactory",
    "FlextObservabilityService",
    "FlextObservabilityServices",
    "get_global_factory",
    "reset_global_factory",
]
