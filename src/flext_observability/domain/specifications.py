"""Domain specifications for observability - business rules and validation."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from flext_core.domain.types import AlertSeverity
from flext_core.domain.types import LogLevel
from flext_core.domain.types import MetricType
from flext_core.domain.types import TraceStatus
from flext_observability.domain.entities import Alert
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.entities import LogEntry
from flext_observability.domain.entities import Metric
from flext_observability.domain.entities import Trace
from flext_observability.domain.value_objects import HealthStatus


class Specification[T](ABC):
    """Base specification class for domain rules."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the candidate satisfies this specification."""

    def and_(self, other: Specification[T]) -> Specification[T]:
        """Combine with another specification using AND logic."""
        return AndSpecification(self, other)

    def or_(self, other: Specification[T]) -> Specification[T]:
        """Combine with another specification using OR logic."""
        return OrSpecification(self, other)

    def not_(self) -> Specification[T]:
        """Negate this specification."""
        return NotSpecification(self)


class AndSpecification[T](Specification[T]):
    """Specification that combines two specifications with AND logic."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(
            candidate,
        )


class OrSpecification[T](Specification[T]):
    """Specification that combines two specifications with OR logic."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(
            candidate,
        )


class NotSpecification[T](Specification[T]):
    """Specification that negates another specification."""

    def __init__(self, spec: Specification[T]) -> None:
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)


# Metric Specifications
class MetricValidationSpec(Specification[Metric]):
    """Specification for validating metrics."""

    def is_satisfied_by(self, metric: Metric) -> bool:
        """Check if metric is valid."""
        # Basic validation rules
        if not metric.name or not metric.name.strip():
            return False

        return not (metric.value < 0 and metric.type == MetricType.COUNTER)


class MetricTypeSpec(Specification[Metric]):
    """Specification for filtering metrics by type."""

    def __init__(self, metric_type: MetricType) -> None:
        self.metric_type = metric_type

    def is_satisfied_by(self, metric: Metric) -> bool:
        return metric.type == self.metric_type


class MetricValueRangeSpec(Specification[Metric]):
    """Specification for filtering metrics by value range."""

    def __init__(
        self, min_value: float | None = None, max_value: float | None = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def is_satisfied_by(self, metric: Metric) -> bool:
        value = float(metric.value)

        if self.min_value is not None and value < self.min_value:
            return False

        return not (self.max_value is not None and value > self.max_value)


class MetricAgeSpec(Specification[Metric]):
    """Specification for filtering metrics by age."""

    def __init__(self, max_age_seconds: int) -> None:
        self.max_age_seconds = max_age_seconds

    def is_satisfied_by(self, metric: Metric) -> bool:
        from datetime import UTC
        from datetime import datetime

        age = (datetime.now(UTC) - metric.timestamp).total_seconds()
        return age <= self.max_age_seconds


# Alert Specifications
class AlertThresholdSpec(Specification[Alert]):
    """Specification for alert threshold validation."""

    def is_satisfied_by(self, alert: Alert) -> bool:
        """Check if alert threshold is properly configured."""
        if not alert.threshold:
            return False

        # Check if threshold comparison makes sense
        return alert.threshold is not None


class AlertSeveritySpec(Specification[Alert]):
    """Specification for filtering alerts by severity."""

    def __init__(self, min_severity: AlertSeverity) -> None:
        self.min_severity = min_severity

    def is_satisfied_by(self, alert: Alert) -> bool:
        severity_order = {
            AlertSeverity.LOW: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.HIGH: 3,
            AlertSeverity.CRITICAL: 4,
        }

        return severity_order[alert.severity] >= severity_order[self.min_severity]


class ActiveAlertSpec(Specification[Alert]):
    """Specification for active (unresolved) alerts."""

    def is_satisfied_by(self, alert: Alert) -> bool:
        return not alert.is_resolved


class AcknowledgedAlertSpec(Specification[Alert]):
    """Specification for acknowledged alerts."""

    def is_satisfied_by(self, alert: Alert) -> bool:
        return alert.is_acknowledged


# Health Check Specifications
class HealthStatusSpec(Specification[HealthCheck]):
    """Specification for filtering health checks by status."""

    def __init__(self, status: HealthStatus) -> None:
        self.status = status

    def is_satisfied_by(self, health_check: HealthCheck) -> bool:
        return health_check.health_status == self.status


class HealthyComponentSpec(Specification[HealthCheck]):
    """Specification for healthy components."""

    def is_satisfied_by(self, health_check: HealthCheck) -> bool:
        return health_check.is_healthy


class SlowHealthCheckSpec(Specification[HealthCheck]):
    """Specification for slow health checks."""

    def __init__(self, threshold_ms: int = 5000) -> None:
        self.threshold_ms = threshold_ms

    def is_satisfied_by(self, health_check: HealthCheck) -> bool:
        return (
            health_check.response_time_ms is not None
            and health_check.response_time_ms > self.threshold_ms
        )


class ComponentNamespaceSpec(Specification[HealthCheck]):
    """Specification for filtering health checks by component namespace."""

    def __init__(self, namespace: str) -> None:
        self.namespace = namespace

    def is_satisfied_by(self, health_check: HealthCheck) -> bool:
        return health_check.name.startswith(self.namespace)


# Log Entry Specifications
class LogLevelSpec(Specification[LogEntry]):
    """Specification for filtering log entries by level."""

    def __init__(self, min_level: LogLevel) -> None:
        self.min_level = min_level

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        level_order = {
            LogLevel.DEBUG: 1,
            LogLevel.INFO: 2,
            LogLevel.WARNING: 3,
            LogLevel.ERROR: 4,
            LogLevel.CRITICAL: 5,
        }

        return level_order[log_entry.level] >= level_order[self.min_level]


class ErrorLogSpec(Specification[LogEntry]):
    """Specification for error log entries."""

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        return log_entry.is_error


class LogWithExceptionSpec(Specification[LogEntry]):
    """Specification for log entries with exceptions."""

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        return log_entry.error_message is not None


class LogWithTraceSpec(Specification[LogEntry]):
    """Specification for log entries with trace information."""

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        return log_entry.correlation_id is not None


class LogMessageContainsSpec(Specification[LogEntry]):
    """Specification for log entries containing specific text."""

    def __init__(self, text: str, case_sensitive: bool = False) -> None:
        self.text = text
        self.case_sensitive = case_sensitive

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        message = log_entry.message
        text = self.text

        if not self.case_sensitive:
            message = message.lower()
            text = text.lower()

        return text in message


# Trace Specifications
class TraceStatusSpec(Specification[Trace]):
    """Specification for filtering traces by status."""

    def __init__(self, status: str) -> None:
        self.status = status

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.trace_status.value == self.status


class CompletedTraceSpec(Specification[Trace]):
    """Specification for completed traces."""

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.trace_status == TraceStatus.COMPLETED


class FailedTraceSpec(Specification[Trace]):
    """Specification for failed traces."""

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.trace_status == TraceStatus.FAILED


class SlowTraceSpec(Specification[Trace]):
    """Specification for slow traces."""

    def __init__(self, threshold_ms: int = 1000) -> None:
        self.threshold_ms = threshold_ms

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.duration_ms is not None and trace.duration_ms > self.threshold_ms


class TraceOperationSpec(Specification[Trace]):
    """Specification for filtering traces by operation name."""

    def __init__(self, operation_name: str) -> None:
        self.operation_name = operation_name

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.operation_name == self.operation_name


class ActiveTraceSpec(Specification[Trace]):
    """Specification for active traces."""

    def is_satisfied_by(self, trace: Trace) -> bool:
        return trace.trace_status == TraceStatus.IN_PROGRESS


# Composite Specifications for Common Use Cases
class CriticalSystemIssuesSpec(Specification[Alert]):
    """Specification for critical system issues."""

    def __init__(self) -> None:
        self.critical_spec = AlertSeveritySpec(AlertSeverity.CRITICAL)
        self.active_spec = ActiveAlertSpec()

    def is_satisfied_by(self, alert: Alert) -> bool:
        return self.critical_spec.is_satisfied_by(
            alert,
        ) and self.active_spec.is_satisfied_by(alert)


class UnhealthyComponentsSpec(Specification[HealthCheck]):
    """Specification for unhealthy components."""

    def __init__(self) -> None:
        self.unhealthy_spec = HealthStatusSpec(HealthStatus.UNHEALTHY)
        self.degraded_spec = HealthStatusSpec(HealthStatus.DEGRADED)

    def is_satisfied_by(self, health_check: HealthCheck) -> bool:
        return self.unhealthy_spec.is_satisfied_by(
            health_check,
        ) or self.degraded_spec.is_satisfied_by(health_check)


class RecentErrorsSpec(Specification[LogEntry]):
    """Specification for recent error log entries."""

    def __init__(self, max_age_seconds: int = 3600) -> None:
        self.error_spec = ErrorLogSpec()
        self.max_age_seconds = max_age_seconds

    def is_satisfied_by(self, log_entry: LogEntry) -> bool:
        from datetime import UTC
        from datetime import datetime

        if not self.error_spec.is_satisfied_by(log_entry):
            return False

        age = (datetime.now(UTC) - log_entry.timestamp).total_seconds()
        return age <= self.max_age_seconds


class PerformanceIssuesSpec(Specification[Trace]):
    """Specification for performance issues in traces."""

    def __init__(self, slow_threshold_ms: int = 5000) -> None:
        self.slow_spec = SlowTraceSpec(slow_threshold_ms)
        self.failed_spec = FailedTraceSpec()

    def is_satisfied_by(self, trace: Trace) -> bool:
        return self.slow_spec.is_satisfied_by(
            trace,
        ) or self.failed_spec.is_satisfied_by(trace)
