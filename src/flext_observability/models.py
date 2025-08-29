"""Observability domain models following SOLID principles.

Core domain entities for metrics, traces, alerts, health checks, and logging.
Built on flext-core patterns with proper separation of concerns.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import override

from flext_core import (
    FlextModels.Entity,
    FlextModels.EntityId,
    FlextResult,
    FlextUtilities,
    FlextLogger,
)
from pydantic import ConfigDict, Field

from flext_observability.constants import ObservabilityConstants
from flext_observability.fields import (
    alert_message_field,
    metric_name_field,
    metric_unit_field,
    metric_value_field,
    timestamp_field,
    trace_name_field,
)

logger = FlextLogger(__name__)


class FlextMetric(FlextModels.Entity):
    """Domain entity for metrics collection and validation.

    Represents a single metric measurement with business rules and validation.
    """

    model_config = ConfigDict(
        frozen=False,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: FlextModels.EntityId = Field(
        default_factory=lambda: FlextModels.EntityId(FlextUtilities.generate_id())
    )
    name: str = metric_name_field
    value: float | Decimal = metric_value_field
    unit: str = metric_unit_field
    tags: dict[str, object] = Field(default_factory=dict)
    timestamp: datetime = timestamp_field
    metric_type: str = Field(default="gauge")

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate metric business rules."""
        try:
            if not self.name.strip():
                return FlextResult[None].fail("Metric name cannot be empty")

            if isinstance(self.value, (int, float)) and self.value < 0:
                return FlextResult[None].fail("Metric value cannot be negative")

            return FlextResult[None].ok(None)
        except Exception as e:
            logger.exception("Metric validation failed")
            return FlextResult[None].fail(f"Validation error: {e}")


class FlextTrace(FlextModels.Entity):
    """Domain entity for distributed tracing spans."""

    model_config = ConfigDict(
        frozen=False,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: FlextModels.EntityId = Field(
        default_factory=lambda: FlextModels.EntityId(FlextUtilities.generate_id())
    )
    operation_name: str = trace_name_field
    service_name: str = Field(min_length=1, max_length=255)
    span_id: str = Field(default="")
    trace_id: str = Field(default="")
    parent_span_id: str | None = Field(default=None)
    start_time: datetime = timestamp_field
    end_time: datetime | None = Field(default=None)
    status: str = Field(default=ObservabilityConstants.TRACE_STATUS_STARTED)
    tags: dict[str, object] = Field(default_factory=dict)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate trace business rules."""
        try:
            if not self.operation_name.strip():
                return FlextResult[None].fail("Operation name cannot be empty")

            if not self.service_name.strip():
                return FlextResult[None].fail("Service name cannot be empty")

            if self.end_time and self.end_time < self.start_time:
                return FlextResult[None].fail("End time cannot be before start time")

            return FlextResult[None].ok(None)
        except Exception as e:
            logger.exception("Trace validation failed")
            return FlextResult[None].fail(f"Validation error: {e}")


class FlextAlert(FlextModels.Entity):
    """Domain entity for alert management."""

    model_config = ConfigDict(
        frozen=False,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: FlextModels.EntityId = Field(
        default_factory=lambda: FlextModels.EntityId(FlextUtilities.generate_id())
    )
    message: str = alert_message_field
    level: str = Field(default=ObservabilityConstants.ALERT_LEVEL_INFO)
    service: str = Field(min_length=1, max_length=255)
    timestamp: datetime = timestamp_field
    resolved: bool = Field(default=False)
    tags: dict[str, object] = Field(default_factory=dict)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate alert business rules."""
        try:
            if not self.message.strip():
                return FlextResult[None].fail("Alert message cannot be empty")

            if not self.service.strip():
                return FlextResult[None].fail("Service name cannot be empty")

            valid_levels = {
                ObservabilityConstants.ALERT_LEVEL_INFO,
                ObservabilityConstants.ALERT_LEVEL_WARNING,
                ObservabilityConstants.ALERT_LEVEL_ERROR,
                ObservabilityConstants.ALERT_LEVEL_CRITICAL,
            }
            if self.level not in valid_levels:
                return FlextResult[None].fail(f"Invalid alert level: {self.level}")

            return FlextResult[None].ok(None)
        except Exception as e:
            logger.exception("Alert validation failed")
            return FlextResult[None].fail(f"Validation error: {e}")


class FlextHealthCheck(FlextModels.Entity):
    """Domain entity for health check monitoring."""

    model_config = ConfigDict(
        frozen=False,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: FlextModels.EntityId = Field(
        default_factory=lambda: FlextModels.EntityId(FlextUtilities.generate_id())
    )
    service_name: str = Field(min_length=1, max_length=255)
    status: str = Field(default=ObservabilityConstants.HEALTH_STATUS_HEALTHY)
    timestamp: datetime = timestamp_field
    details: dict[str, object] = Field(default_factory=dict)
    dependencies: list[str] = Field(default_factory=list)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate health check business rules."""
        try:
            if not self.service_name.strip():
                return FlextResult[None].fail("Service name cannot be empty")

            valid_statuses = {
                ObservabilityConstants.HEALTH_STATUS_HEALTHY,
                ObservabilityConstants.HEALTH_STATUS_DEGRADED,
                ObservabilityConstants.HEALTH_STATUS_UNHEALTHY,
            }
            if self.status not in valid_statuses:
                return FlextResult[None].fail(f"Invalid health status: {self.status}")

            return FlextResult[None].ok(None)
        except Exception as e:
            logger.exception("Health check validation failed")
            return FlextResult[None].fail(f"Validation error: {e}")


class FlextLogEntry(FlextModels.Entity):
    """Domain entity for structured logging."""

    model_config = ConfigDict(
        frozen=False,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: FlextModels.EntityId = Field(
        default_factory=lambda: FlextModels.EntityId(FlextUtilities.generate_id())
    )
    message: str = Field(min_length=1, max_length=2000)
    level: str = Field(default="INFO")
    service: str = Field(min_length=1, max_length=255)
    timestamp: datetime = timestamp_field
    correlation_id: str | None = Field(default=None)
    extra_data: dict[str, object] = Field(default_factory=dict)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate log entry business rules."""
        try:
            if not self.message.strip():
                return FlextResult[None].fail("Log message cannot be empty")

            if not self.service.strip():
                return FlextResult[None].fail("Service name cannot be empty")

            valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
            if self.level not in valid_levels:
                return FlextResult[None].fail(f"Invalid log level: {self.level}")

            return FlextResult[None].ok(None)
        except Exception as e:
            logger.exception("Log entry validation failed")
            return FlextResult[None].fail(f"Validation error: {e}")


# Factory functions for easy entity creation
def flext_metric(
    name: str,
    value: float | Decimal,
    unit: str = ObservabilityConstants.DEFAULT_METRIC_UNIT,
    *,
    tags: dict[str, object] | None = None,
    timestamp: datetime | None = None,
    metric_type: str | None = None,
) -> FlextMetric:
    """Create a FlextMetric entity."""
    return FlextMetric(
        name=name,
        value=value,
        unit=unit,
        tags=tags or {},
        timestamp=timestamp or datetime.now(tz=UTC),
        metric_type=metric_type or "gauge",
    )


def flext_trace(
    operation_name: str,
    service_name: str,
    *,
    start_time: datetime | None = None,
    tags: dict[str, object] | None = None,
    span_id: str | None = None,
    trace_id: str | None = None,
) -> FlextTrace:
    """Create a FlextTrace entity."""
    return FlextTrace(
        operation_name=operation_name,
        service_name=service_name,
        start_time=start_time or datetime.now(tz=UTC),
        tags=tags or {},
        span_id=span_id or "",
        trace_id=trace_id or "",
    )


def flext_alert(
    message: str,
    service: str,
    level: str = ObservabilityConstants.ALERT_LEVEL_INFO,
    *,
    timestamp: datetime | None = None,
    tags: dict[str, object] | None = None,
    resolved: bool = False,
) -> FlextAlert:
    """Create a FlextAlert entity."""
    return FlextAlert(
        message=message,
        service=service,
        level=level,
        timestamp=timestamp or datetime.now(tz=UTC),
        tags=tags or {},
        resolved=resolved,
    )


def flext_health_check(
    service_name: str,
    status: str = ObservabilityConstants.HEALTH_STATUS_HEALTHY,
    *,
    timestamp: datetime | None = None,
    details: dict[str, object] | None = None,
    dependencies: list[str] | None = None,
) -> FlextHealthCheck:
    """Create a FlextHealthCheck entity."""
    return FlextHealthCheck(
        service_name=service_name,
        status=status,
        timestamp=timestamp or datetime.now(tz=UTC),
        details=details or {},
        dependencies=dependencies or [],
    )


def flext_log_entry(
    message: str,
    service: str,
    level: str = "INFO",
    *,
    timestamp: datetime | None = None,
    correlation_id: str | None = None,
    extra_data: dict[str, object] | None = None,
) -> FlextLogEntry:
    """Create a FlextLogEntry entity."""
    return FlextLogEntry(
        message=message,
        service=service,
        level=level,
        timestamp=timestamp or datetime.now(tz=UTC),
        correlation_id=correlation_id,
        extra_data=extra_data or {},
    )


__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextTrace",
    "flext_alert",
    "flext_health_check",
    "flext_log_entry",
    "flext_metric",
    "flext_trace",
]
