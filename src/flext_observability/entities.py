"""FLEXT Observability Entities - Simplified using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Entities simplificadas usando apenas padrões essenciais do flext-core.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import (
    Decimal,  # noqa: TC003 - Required at runtime for Pydantic field definitions
)
from typing import ClassVar, cast

from flext_core import FlextEntity, FlextGenerators, FlextResult
from pydantic import Field

# ============================================================================
# CORE ENTITIES - Simplified using flext-core patterns
# ============================================================================


class FlextMetric(FlextEntity):
    """Simplified metric entity using flext-core base."""

    model_config: ClassVar[dict[str, object]] = {
        "frozen": False,  # Allow dynamic attributes
    }

    name: str = Field(..., description="Metric name")
    value: float | Decimal = Field(..., description="Metric value")
    unit: str = Field(default="", description="Metric unit")
    tags: dict[str, str] = Field(default_factory=dict, description="Metric tags")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metric_type: str = Field(default="gauge", description="Metric type")

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate metric domain rules."""
        if not self.name or not isinstance(self.name, str):
            return FlextResult.fail("Invalid metric name")
        # Type validation for metric value
        try:
            float(self.value)  # Test if it can be converted to float
        except (ValueError, TypeError):
            return FlextResult.fail("Invalid metric value")
        return FlextResult.ok(None)


class FlextLogEntry(FlextEntity):
    """Simplified log entry entity using flext-core base."""

    message: str = Field(..., description="Log message")
    level: str = Field(default="info", description="Log level")
    context: dict[str, object] = Field(default_factory=dict, description="Log context")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate log entry domain rules."""
        if not self.message or not isinstance(self.message, str):
            return FlextResult.fail("Invalid log message")
        if self.level not in {"debug", "info", "warning", "error", "critical"}:
            return FlextResult.fail("Invalid log level")
        return FlextResult.ok(None)


class FlextTrace(FlextEntity):
    """Simplified trace entity using flext-core base."""

    trace_id: str = Field(..., description="Trace ID")
    operation: str = Field(..., description="Operation name")
    span_id: str = Field(..., description="Span ID")
    span_attributes: dict[str, object] = Field(
        default_factory=dict,
        description="Span attributes",
    )
    duration_ms: int = Field(default=0, description="Duration in milliseconds")
    status: str = Field(default="pending", description="Trace status")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate trace domain rules."""
        if not self.trace_id or not isinstance(self.trace_id, str):
            return FlextResult.fail("Invalid trace ID")
        if not self.operation or not isinstance(self.operation, str):
            return FlextResult.fail("Invalid operation name")
        return FlextResult.ok(None)


class FlextAlert(FlextEntity):
    """Simplified alert entity using flext-core base."""

    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    severity: str = Field(default="low", description="Alert severity")
    status: str = Field(default="active", description="Alert status")
    tags: dict[str, str] = Field(default_factory=dict, description="Alert tags")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate alert domain rules."""
        if not self.title or not isinstance(self.title, str):
            return FlextResult.fail("Invalid alert title")
        if not self.message or not isinstance(self.message, str):
            return FlextResult.fail("Invalid alert message")
        if self.severity not in {"low", "medium", "high", "critical", "emergency"}:
            return FlextResult.fail("Invalid alert severity")
        return FlextResult.ok(None)


class FlextHealthCheck(FlextEntity):
    """Simplified health check entity using flext-core base."""

    component: str = Field(..., description="Component name")
    status: str = Field(default="unknown", description="Health status")
    message: str = Field(default="", description="Health message")
    metrics: dict[str, object] = Field(
        default_factory=dict,
        description="Health metrics",
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate health check domain rules."""
        if not self.component or not isinstance(self.component, str):
            return FlextResult.fail("Invalid component name")
        if self.status not in {"healthy", "unhealthy", "degraded", "unknown"}:
            return FlextResult.fail("Invalid health status")
        return FlextResult.ok(None)


# ============================================================================
# FACTORY FUNCTIONS - Create entities with proper validation
# ============================================================================


def flext_alert(
    title: str,
    message: str,
    severity: str = "low",
    status: str = "active",
    **kwargs: object,
) -> FlextAlert:
    """Create a FlextAlert entity with proper validation."""
    tags = cast("dict[str, str]", kwargs.get("tags", {}))
    timestamp = cast("datetime", kwargs.get("timestamp", datetime.now(UTC)))

    # Create with explicit kwargs for better type safety
    if "id" in kwargs and "version" in kwargs and "created_at" in kwargs:
        return FlextAlert(
            id=cast("str", kwargs["id"]),
            version=cast("int", kwargs["version"]),
            created_at=cast("datetime", kwargs["created_at"]),
            title=title,
            message=message,
            severity=severity,
            status=status,
            tags=tags,
            timestamp=timestamp,
        )
    if "id" in kwargs:
        return FlextAlert(
            id=cast("str", kwargs["id"]),
            title=title,
            message=message,
            severity=severity,
            status=status,
            tags=tags,
            timestamp=timestamp,
        )
    return FlextAlert(
        id=FlextGenerators.generate_entity_id(),
        title=title,
        message=message,
        severity=severity,
        status=status,
        tags=tags,
        timestamp=timestamp,
    )


def flext_trace(
    trace_id: str,
    operation: str,
    span_id: str,
    status: str = "pending",
    **kwargs: object,
) -> FlextTrace:
    """Create a FlextTrace entity with proper validation."""
    span_attributes = cast("dict[str, object]", kwargs.get("span_attributes", {}))
    duration_ms = cast("int", kwargs.get("duration_ms", 0))
    timestamp = cast("datetime", kwargs.get("timestamp", datetime.now(UTC)))

    # Create with explicit kwargs for better type safety
    if "id" in kwargs:
        return FlextTrace(
            id=cast("str", kwargs["id"]),
            trace_id=trace_id,
            operation=operation,
            span_id=span_id,
            span_attributes=span_attributes,
            duration_ms=duration_ms,
            status=status,
            timestamp=timestamp,
        )
    return FlextTrace(
        id=FlextGenerators.generate_entity_id(),
        trace_id=trace_id,
        operation=operation,
        span_id=span_id,
        span_attributes=span_attributes,
        duration_ms=duration_ms,
        status=status,
        timestamp=timestamp,
    )


def flext_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    metric_type: str = "gauge",
    **kwargs: object,
) -> FlextResult[FlextMetric]:
    """Create a FlextMetric entity with proper validation and type safety."""
    try:
        tags = cast("dict[str, str]", kwargs.get("tags", {}))
        timestamp = cast("datetime", kwargs.get("timestamp", datetime.now(UTC)))

        # Create with explicit kwargs for better type safety
        if "id" in kwargs and "version" in kwargs and "created_at" in kwargs:
            metric = FlextMetric(
                id=cast("str", kwargs["id"]),
                version=cast("int", kwargs["version"]),
                created_at=cast("datetime", kwargs["created_at"]),
                name=name,
                value=value,
                unit=unit,
                tags=tags,
                timestamp=timestamp,
            )
        elif "id" in kwargs:
            metric = FlextMetric(
                id=cast("str", kwargs["id"]),
                name=name,
                value=value,
                unit=unit,
                tags=tags,
                timestamp=timestamp,
            )
        else:
            metric = FlextMetric(
                id=FlextGenerators.generate_entity_id(),
                name=name,
                value=value,
                unit=unit,
                tags=tags,
                timestamp=timestamp,
            )

        # Set metric_type directly on the field
        metric.metric_type = metric_type

        # Validate domain rules
        validation_result = metric.validate_domain_rules()
        if validation_result.is_failure:
            return FlextResult.fail(
                validation_result.error or "Metric validation failed",
            )

        return FlextResult.ok(metric)

    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create metric: {e}")


def flext_health_check(
    component: str,
    status: str = "unknown",
    message: str = "",
    **kwargs: object,
) -> FlextHealthCheck:
    """Create a FlextHealthCheck entity with proper validation."""
    metrics = cast("dict[str, object]", kwargs.get("metrics", {}))
    timestamp = cast("datetime", kwargs.get("timestamp", datetime.now(UTC)))

    # Create with explicit kwargs for better type safety
    if "id" in kwargs:
        return FlextHealthCheck(
            id=cast("str", kwargs["id"]),
            component=component,
            status=status,
            message=message,
            metrics=metrics,
            timestamp=timestamp,
        )
    return FlextHealthCheck(
        id=FlextGenerators.generate_entity_id(),
        component=component,
        status=status,
        message=message,
        metrics=metrics,
        timestamp=timestamp,
    )


# ============================================================================
# PYDANTIC MODEL REBUILDING - Fix "not fully defined" errors
# ============================================================================

# Models are now properly defined with Decimal import at the top
FlextMetric.model_rebuild()
FlextTrace.model_rebuild()
FlextAlert.model_rebuild()
FlextLogEntry.model_rebuild()
FlextHealthCheck.model_rebuild()
