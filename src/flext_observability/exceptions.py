"""FLEXT Observability Exceptions - Complete Observability Error Handling.

This module implements comprehensive exception handling for the FLEXT observability,
monitoring, metrics, tracing, and alerting operations. Extends flext-core exception
foundation with domain-specific error types for production observability needs.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextCore


class FlextObservabilityExceptions(FlextCore.Exceptions):
    """Single CONSOLIDATED class containing ALL observability exceptions."""

    class ObservabilityErrorCodes(Enum):
        """Error codes for observability domain operations."""

        OBSERVABILITY_ERROR = "OBSERVABILITY_ERROR"
        METRICS_ERROR = "METRICS_ERROR"
        METRICS_COLLECTION_ERROR = "METRICS_COLLECTION_ERROR"
        METRICS_RECORDING_ERROR = "METRICS_RECORDING_ERROR"
        TRACING_ERROR = "TRACING_ERROR"
        TRACE_START_ERROR = "TRACE_START_ERROR"
        TRACE_COMPLETE_ERROR = "TRACE_COMPLETE_ERROR"
        ALERTING_ERROR = "ALERTING_ERROR"
        ALERT_CREATION_ERROR = "ALERT_CREATION_ERROR"
        ALERT_ESCALATION_ERROR = "ALERT_ESCALATION_ERROR"
        HEALTH_CHECK_ERROR = "HEALTH_CHECK_ERROR"
        HEALTH_MONITOR_ERROR = "HEALTH_MONITOR_ERROR"
        MONITORING_ERROR = "MONITORING_ERROR"
        MONITORING_SETUP_ERROR = "MONITORING_SETUP_ERROR"
        OBSERVABILITY_CONFIG_ERROR = "OBSERVABILITY_CONFIG_ERROR"

    # Base observability exception classes as nested classes
    class ObservabilityBaseError(FlextCore.Exceptions.BaseError):
        """Base exception for all observability domain errors."""

        def _extract_common_kwargs(
            self, kwargs: FlextCore.Types.Dict
        ) -> tuple[FlextCore.Types.Dict, str | None, str | None]:
            """Extract common kwargs for error construction."""
            context_value = kwargs.get("context", {})
            context: FlextCore.Types.Dict = (
                context_value if isinstance(context_value, dict) else {}
            )
            correlation_id_value = kwargs.get("correlation_id")
            correlation_id: str | None = (
                correlation_id_value if isinstance(correlation_id_value, str) else None
            )
            error_code_value = kwargs.get("error_code")
            error_code: str | None = (
                error_code_value if isinstance(error_code_value, str) else None
            )
            return context, correlation_id, error_code

        def _build_context(
            self, base_context: FlextCore.Types.Dict, **extra_fields: object
        ) -> FlextCore.Types.Dict:
            """Build context with additional fields."""
            context = dict[str, object](base_context)
            context.update(extra_fields)
            return context

        @override
        def __init__(
            self,
            message: str,
            *,
            component: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize observability error with context using helpers.

            Args:
                message: Error message
                component: Observability component that caused the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store component before extracting common kwargs
            self.component = component

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with observability-specific fields
            context = self._build_context(
                base_context,
                component=component,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "OBSERVABILITY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MetricsError(ObservabilityBaseError):
        """Metrics collection and recording errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metric_name: str | None = None,
            metric_value: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metrics error using helpers.

            Args:
                message: Error message
                metric_name: Name of the metric
                metric_value: Value of the metric
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store metrics attributes before extracting common kwargs
            self.metric_name = metric_name
            self.metric_value = metric_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with metrics-specific fields
            context = self._build_context(
                base_context,
                metric_name=metric_name,
                metric_value=metric_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="metrics",
                code=error_code or "METRICS_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MetricsCollectionError(MetricsError):
        """Metrics collection specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metric_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metrics collection error using helpers.

            Args:
                message: Error message
                metric_name: Name of the metric being collected
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with collection-specific fields
            context = self._build_context(
                base_context,
                metric_name=metric_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                metric_name=metric_name,
                code=error_code or "METRICS_COLLECTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MetricsRecordingError(MetricsError):
        """Metrics recording specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metric_name: str | None = None,
            metric_value: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metrics recording error using helpers.

            Args:
                message: Error message
                metric_name: Name of the metric being recorded
                metric_value: Value of the metric being recorded
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with recording-specific fields
            context = self._build_context(
                base_context,
                metric_name=metric_name,
                metric_value=metric_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                metric_name=metric_name,
                metric_value=metric_value,
                code=error_code or "METRICS_RECORDING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class TracingError(ObservabilityBaseError):
        """Distributed tracing errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            trace_id: str | None = None,
            operation_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize tracing error using helpers.

            Args:
                message: Error message
                trace_id: Distributed trace identifier
                operation_name: Name of the traced operation
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store tracing attributes before extracting common kwargs
            self.trace_id = trace_id
            self.operation_name = operation_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with tracing-specific fields
            context = self._build_context(
                base_context,
                trace_id=trace_id,
                operation_name=operation_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="tracing",
                code=error_code or "TRACING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class TraceStartError(TracingError):
        """Trace start operation specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            trace_id: str | None = None,
            operation_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize trace start error using helpers.

            Args:
                message: Error message
                trace_id: Distributed trace identifier
                operation_name: Name of the operation being traced
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with trace start fields
            context = self._build_context(
                base_context,
                trace_id=trace_id,
                operation_name=operation_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                trace_id=trace_id,
                operation_name=operation_name,
                code=error_code or "TRACE_START_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class TraceCompleteError(TracingError):
        """Trace completion specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            trace_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize trace complete error using helpers.

            Args:
                message: Error message
                trace_id: Distributed trace identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with trace completion fields
            context = self._build_context(
                base_context,
                trace_id=trace_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                trace_id=trace_id,
                code=error_code or "TRACE_COMPLETE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AlertingError(ObservabilityBaseError):
        """Alert management and escalation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            alert_id: str | None = None,
            alert_severity: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize alerting error using helpers.

            Args:
                message: Error message
                alert_id: Alert identifier
                alert_severity: Severity level of the alert
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store alerting attributes before extracting common kwargs
            self.alert_id = alert_id
            self.alert_severity = alert_severity

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with alerting-specific fields
            context = self._build_context(
                base_context,
                alert_id=alert_id,
                alert_severity=alert_severity,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="alerting",
                code=error_code or "ALERTING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AlertCreationError(AlertingError):
        """Alert creation specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            alert_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize alert creation error using helpers.

            Args:
                message: Error message
                alert_id: Alert identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with alert creation fields
            context = self._build_context(
                base_context,
                alert_id=alert_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                alert_id=alert_id,
                code=error_code or "ALERT_CREATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AlertEscalationError(AlertingError):
        """Alert escalation specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            alert_id: str | None = None,
            escalation_level: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize alert escalation error using helpers.

            Args:
                message: Error message
                alert_id: Alert identifier
                escalation_level: Current escalation level
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store escalation attributes before extracting common kwargs
            self.escalation_level = escalation_level

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with escalation fields
            context = self._build_context(
                base_context,
                alert_id=alert_id,
                escalation_level=escalation_level,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                alert_id=alert_id,
                code=error_code or "ALERT_ESCALATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class HealthCheckError(ObservabilityBaseError):
        """Health check execution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            check_name: str | None = None,
            check_status: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize health check error using helpers.

            Args:
                message: Error message
                check_name: Name of the health check
                check_status: Current health check status
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store health check attributes before extracting common kwargs
            self.check_name = check_name
            self.check_status = check_status

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with health check fields
            context = self._build_context(
                base_context,
                check_name=check_name,
                check_status=check_status,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="health_check",
                code=error_code or "HEALTH_CHECK_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class HealthMonitorError(HealthCheckError):
        """Health monitoring system errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            check_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize health monitor error using helpers.

            Args:
                message: Error message
                check_name: Name of the health check being monitored
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with health monitor fields
            context = self._build_context(
                base_context,
                check_name=check_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                check_name=check_name,
                code=error_code or "HEALTH_MONITOR_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MonitoringError(ObservabilityBaseError):
        """General monitoring operation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            monitoring_target: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize monitoring error using helpers.

            Args:
                message: Error message
                monitoring_target: Target being monitored
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store monitoring attributes before extracting common kwargs
            self.monitoring_target = monitoring_target

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with monitoring fields
            context = self._build_context(
                base_context,
                monitoring_target=monitoring_target,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="monitoring",
                code=error_code or "MONITORING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MonitoringSetupError(MonitoringError):
        """Monitoring system setup errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            setup_component: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize monitoring setup error using helpers.

            Args:
                message: Error message
                setup_component: Component being set up
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store setup attributes before extracting common kwargs
            self.setup_component = setup_component

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with setup fields
            context = self._build_context(
                base_context,
                setup_component=setup_component,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                monitoring_target=setup_component,
                code=error_code or "MONITORING_SETUP_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ObservabilityConfigError(ObservabilityBaseError):
        """Observability configuration errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            config_key: str | None = None,
            config_value: object = None,
            **kwargs: object,
        ) -> None:
            """Initialize observability configuration error using helpers.

            Args:
                message: Error message
                config_key: Configuration key that failed
                config_value: Invalid configuration value
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store config attributes before extracting common kwargs
            self.config_key = config_key
            self.config_value = config_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with config fields
            context = self._build_context(
                base_context,
                config_key=config_key,
                config_value=config_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="configuration",
                code=error_code or "OBSERVABILITY_CONFIG_ERROR",
                context=context,
                correlation_id=correlation_id,
            )


# Backward compatibility aliases - property-based exports
FlextObservabilityError = FlextObservabilityExceptions.ObservabilityBaseError
FlextObservabilityErrorCodes = FlextObservabilityExceptions.ObservabilityErrorCodes
FlextMetricsError = FlextObservabilityExceptions.MetricsError
FlextMetricsCollectionError = FlextObservabilityExceptions.MetricsCollectionError
FlextMetricsRecordingError = FlextObservabilityExceptions.MetricsRecordingError
FlextTracingError = FlextObservabilityExceptions.TracingError
FlextTraceStartError = FlextObservabilityExceptions.TraceStartError
FlextTraceCompleteError = FlextObservabilityExceptions.TraceCompleteError
FlextAlertingError = FlextObservabilityExceptions.AlertingError
FlextAlertCreationError = FlextObservabilityExceptions.AlertCreationError
FlextAlertEscalationError = FlextObservabilityExceptions.AlertEscalationError
FlextHealthCheckError = FlextObservabilityExceptions.HealthCheckError
FlextHealthMonitorError = FlextObservabilityExceptions.HealthMonitorError
FlextMonitoringError = FlextObservabilityExceptions.MonitoringError
FlextMonitoringSetupError = FlextObservabilityExceptions.MonitoringSetupError
FlextObservabilityConfigError = FlextObservabilityExceptions.ObservabilityConfigError

__all__ = [
    "FlextAlertCreationError",
    "FlextAlertEscalationError",
    "FlextAlertingError",
    "FlextHealthCheckError",
    "FlextHealthMonitorError",
    "FlextMetricsCollectionError",
    "FlextMetricsError",
    "FlextMetricsRecordingError",
    "FlextMonitoringError",
    "FlextMonitoringSetupError",
    "FlextObservabilityConfigError",
    "FlextObservabilityError",
    "FlextObservabilityErrorCodes",
    "FlextObservabilityExceptions",
    "FlextTraceCompleteError",
    "FlextTraceStartError",
    "FlextTracingError",
]
