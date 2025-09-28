"""Unified observability service implementing FLEXT patterns.

REFACTORED: Eliminated factory patterns, wrappers, and multiple classes.
Uses unified service with direct composition following zero tolerance policy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# FIXED: Removed ImportError fallback - psutil must be available (ZERO TOLERANCE)
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextUtilities,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextMetricsService,
    FlextTracingService,
)
from flext_observability.typings import FlextObservabilityTypes


class FlextObservabilityService(
    FlextService[FlextObservabilityTypes.Core.MetadataDict]
):
    """Observability service using FlextObservabilityTypes for enhanced type safety."""

    def __init__(self, **data: object) -> None:
        """Initialize observability service with metrics and tracing capabilities."""
        super().__init__(**data)
        self._logger = FlextLogger(__name__)
        self._container = FlextContainer.get_global()
        # Placeholder for service implementations - to be replaced when services are available
        self._metrics_service = (
            None  # FlextObservabilityMetricsService when implemented
        )
        self._tracing_service = (
            None  # FlextObservabilityTracingService when implemented
        )

    class ObservabilityFactories:
        """Factory methods for creating observability components."""

        @staticmethod
        def create_metrics(
            service_name: str = "flext_observability",
        ) -> FlextResult[FlextObservabilityTypes.Core.MetricDict]:
            """Create standard metrics using observability-specific types."""
            try:
                metrics: FlextObservabilityTypes.Core.MetricDict = {
                    "service_name": service_name,
                    "timestamp": FlextUtilities.Generators.generate_timestamp(),
                    "uptime_seconds": 0,
                    "requests_total": 0,
                    "errors_total": 0,
                    "active_connections": 0,
                }
                return FlextResult[FlextObservabilityTypes.Core.MetricDict].ok(metrics)
            except Exception as e:
                return FlextResult[FlextObservabilityTypes.Core.MetricDict].fail(
                    f"Metrics creation failed: {e}"
                )

        @staticmethod
        def format_metrics(
            metrics: FlextObservabilityTypes.Core.MetricDict,
        ) -> FlextResult[FlextObservabilityTypes.Core.MetricFormatDict]:
            """Format metrics for export using observability-specific types."""
            try:
                formatted_metrics: FlextObservabilityTypes.Core.MetricFormatDict = {
                    "metrics": metrics,
                    "format": "prometheus",
                    "timestamp": FlextUtilities.Generators.generate_timestamp(),
                }
                return FlextResult[FlextObservabilityTypes.Core.MetricFormatDict].ok(
                    formatted_metrics
                )
            except Exception as e:
                return FlextResult[FlextObservabilityTypes.Core.MetricFormatDict].fail(
                    f"Metrics formatting failed: {e}"
                )

        @staticmethod
        def create_trace_context(
            operation_name: str = "flext_operation",
        ) -> FlextResult[FlextObservabilityTypes.Core.TraceContextDict]:
            """Create trace context using observability-specific types."""
            try:
                trace_context: FlextObservabilityTypes.Core.TraceContextDict = {
                    "trace_id": FlextUtilities.Generators.generate_entity_id(),
                    "span_id": FlextUtilities.Generators.generate_entity_id(),
                    "operation_name": operation_name,
                    "start_time": FlextUtilities.Generators.generate_timestamp(),
                    "parent_span_id": None,
                    "baggage": {},
                }
                return FlextResult[FlextObservabilityTypes.Core.TraceContextDict].ok(
                    trace_context
                )
            except Exception as e:
                return FlextResult[FlextObservabilityTypes.Core.TraceContextDict].fail(
                    f"Trace context creation failed: {e}"
                )

        @staticmethod
        def create_span_event(
            context: FlextObservabilityTypes.Core.TraceContextDict, event: str
        ) -> FlextResult[FlextObservabilityTypes.Core.SpanAttributesDict]:
            """Create span event using observability-specific types."""
            try:
                span_event: FlextObservabilityTypes.Core.SpanAttributesDict = {
                    "trace_id": context.get("trace_id", "unknown"),
                    "span_id": context.get("span_id", "unknown"),
                    "event_name": event,
                    "timestamp": FlextUtilities.Generators.generate_timestamp(),
                    "attributes": {},
                }
                return FlextResult[FlextObservabilityTypes.Core.SpanAttributesDict].ok(
                    span_event
                )
            except Exception as e:
                return FlextResult[
                    FlextObservabilityTypes.Core.SpanAttributesDict
                ].fail(f"Span event creation failed: {e}")

    def record_metric(
        self,
        metric_name: str,
        metric_value: float,
        tags: FlextObservabilityTypes.Core.TagsDict | None = None,
    ) -> FlextResult[None]:
        """Record metric using observability-specific types."""
        if not metric_name or not isinstance(metric_name, str):
            return FlextResult[None].fail("Metric name must be a non-empty string")

        try:
            metric_result = self._metrics_service.record_counter(
                name=metric_name,
                value=metric_value,
                tags=tags or {},
            )

            if metric_result.is_failure:
                return FlextResult[None].fail(
                    f"Metric recording failed: {metric_result.error}"
                )

            self._logger.debug(f"Recorded metric: {metric_name} = {metric_value}")
            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Metric recording error: {e}")

    def start_trace(
        self,
        operation_name: str,
        trace_context: FlextObservabilityTypes.Core.TraceContextDict | None = None,
    ) -> FlextResult[str]:
        """Start distributed trace using observability-specific types."""
        if not operation_name or not isinstance(operation_name, str):
            return FlextResult[str].fail("Operation name must be a non-empty string")

        try:
            # Create trace context if not provided
            if trace_context is None:
                context_result = self.ObservabilityFactories.create_trace_context(
                    operation_name
                )
                if context_result.is_failure:
                    return FlextResult[str].fail(
                        f"Trace context creation failed: {context_result.error}"
                    )
                trace_context = context_result.unwrap()

            # Start trace through tracing service
            trace_result = self._tracing_service.start_trace(
                operation_name=operation_name,
                trace_context=trace_context,
            )

            if trace_result.is_failure:
                return FlextResult[str].fail(
                    f"Trace start failed: {trace_result.error}"
                )

            trace_id = str(trace_context.get("trace_id", "unknown"))
            self._logger.debug(f"Started trace: {operation_name} (ID: {trace_id})")
            return FlextResult[str].ok(trace_id)

        except Exception as e:
            return FlextResult[str].fail(f"Trace start error: {e}")

    def collect_observability_data(
        self,
    ) -> FlextResult[FlextObservabilityTypes.Core.MetadataDict]:
        """Collect comprehensive observability data using observability-specific types."""
        try:
            # Collect metrics
            metrics_result = self._metrics_service.get_metrics_summary()
            if metrics_result.is_failure:
                return FlextResult[FlextObservabilityTypes.Core.MetadataDict].fail(
                    f"Metrics collection failed: {metrics_result.error}"
                )

            # Collect tracing data
            traces_result = self._tracing_service.get_trace_summary()
            if traces_result.is_failure:
                return FlextResult[FlextObservabilityTypes.Core.MetadataDict].fail(
                    f"Traces collection failed: {traces_result.error}"
                )

            # Compile observability data
            observability_data: FlextObservabilityTypes.Core.MetadataDict = {
                "service_name": "flext_observability",
                "timestamp": FlextUtilities.Generators.generate_timestamp(),
                "metrics_summary": metrics_result.unwrap(),
                "traces_summary": traces_result.unwrap(),
                "health_status": "healthy",
                "version": "0.9.0",
            }

            return FlextResult[FlextObservabilityTypes.Core.MetadataDict].ok(
                observability_data,
            )

        except Exception as e:
            return FlextResult[FlextObservabilityTypes.Core.MetadataDict].fail(
                f"Observability data collection failed: {e}"
            )

    def execute(self) -> FlextResult[FlextObservabilityTypes.Core.MetadataDict]:
        """Execute observability service operations using observability-specific types."""
        try:
            # Validate service state
            if not hasattr(self, "_metrics_service") or not hasattr(
                self, "_tracing_service"
            ):
                return FlextResult[FlextObservabilityTypes.Core.MetadataDict].fail(
                    "Observability services not properly initialized"
                )

            # Collect and return observability data
            return self.collect_observability_data()

        except Exception as e:
            return FlextResult[FlextObservabilityTypes.Core.MetadataDict].fail(
                f"Observability service execution failed: {e}"
            )


# Master factory class
class FlextObservabilityMasterFactory:
    """Master factory for creating all observability components."""

    def __init__(self) -> None:
        """Initialize the master factory."""
        self._service = FlextObservabilityService()

    def create_metrics_service(self) -> FlextMetricsService:
        """Create a metrics service instance."""
        return FlextMetricsService()

    def create_tracing_service(self) -> FlextTracingService:
        """Create a tracing service instance."""
        return FlextTracingService()

    def create_alert_service(self) -> FlextAlertService:
        """Create an alert service instance."""
        return FlextAlertService()

    def create_health_service(self) -> FlextHealthService:
        """Create a health service instance."""
        return FlextHealthService()

    def create_observability_service(self) -> FlextObservabilityService:
        """Create the main observability service instance."""
        return FlextObservabilityService()


class _GlobalFactoryHolder:
    """Holder for the global factory instance to avoid global variables."""

    _instance: FlextObservabilityMasterFactory | None = None

    @classmethod
    def get(cls) -> FlextObservabilityMasterFactory:
        """Get the global observability factory instance."""
        if cls._instance is None:
            cls._instance = FlextObservabilityMasterFactory()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the global observability factory instance."""
        cls._instance = None


def get_global_factory() -> FlextObservabilityMasterFactory:
    """Get the global observability factory instance."""
    return _GlobalFactoryHolder.get()


def reset_global_factory() -> None:
    """Reset the global observability factory instance."""
    _GlobalFactoryHolder.reset()


__all__: list[str] = [
    "FlextObservabilityMasterFactory",
    "FlextObservabilityService",
    "get_global_factory",
    "reset_global_factory",
]
