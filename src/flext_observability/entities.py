"""FLEXT Observability Entities - Simplified using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Entities simplificadas usando apenas padrões essenciais do flext-core.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from flext_core import FlextEntity, FlextResult
from flext_core.utilities import generate_id
from pydantic import Field

# ============================================================================
# CORE ENTITIES - Simplified using flext-core patterns
# ============================================================================


class FlextMetric(FlextEntity):
    """Simplified metric entity using flext-core base."""

    name: str = Field(..., description="Metric name")
    value: float | Decimal = Field(..., description="Metric value")
    unit: str = Field(default="", description="Metric unit")
    tags: dict[str, str] = Field(default_factory=dict, description="Metric tags")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __init__(self, name: str, value: float | Decimal, **kwargs: Any) -> None:
        """Initialize metric with flext-core pattern."""
        super().__init__(
            id=kwargs.get("id", generate_id()),
            name=name,
            value=value,
            unit=kwargs.get("unit", ""),
            tags=kwargs.get("tags", {}),
            timestamp=kwargs.get("timestamp", datetime.now(UTC)),
        )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate metric domain rules."""
        if not self.name or not isinstance(self.name, str):
            return FlextResult.error("Invalid metric name")
        if not isinstance(self.value, (int, float, Decimal)):
            return FlextResult.error("Invalid metric value")
        return FlextResult.ok(None)


class FlextLogEntry(FlextEntity):
    """Simplified log entry entity using flext-core base."""

    message: str = Field(..., description="Log message")
    level: str = Field(default="info", description="Log level")
    context: dict[str, Any] = Field(default_factory=dict, description="Log context")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __init__(self, message: str, level: str = "info", **kwargs: Any) -> None:
        """Initialize log entry with flext-core pattern."""
        super().__init__(
            id=kwargs.get("id", generate_id()),
            message=message,
            level=level,
            context=kwargs.get("context", {}),
            timestamp=kwargs.get("timestamp", datetime.now(UTC)),
        )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate log entry domain rules."""
        if not self.message or not isinstance(self.message, str):
            return FlextResult.error("Invalid log message")
        if self.level not in {"debug", "info", "warning", "error", "critical"}:
            return FlextResult.error("Invalid log level")
        return FlextResult.ok(None)


class FlextTrace(FlextEntity):
    """Simplified trace entity using flext-core base."""

    trace_id: str = Field(..., description="Trace ID")
    operation: str = Field(..., description="Operation name")
    span_id: str = Field(..., description="Span ID")
    span_attributes: dict[str, Any] = Field(default_factory=dict, description="Span attributes")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __init__(self, trace_id: str, operation: str, span_id: str = "", **kwargs: Any) -> None:
        """Initialize trace with flext-core pattern."""
        super().__init__(
            id=kwargs.get("id", generate_id()),
            trace_id=trace_id,
            operation=operation,
            span_id=span_id or f"{trace_id[:16]}-span",
            span_attributes=kwargs.get("span_attributes", {}),
            timestamp=kwargs.get("timestamp", datetime.now(UTC)),
        )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate trace domain rules."""
        if not self.trace_id or not isinstance(self.trace_id, str):
            return FlextResult.error("Invalid trace ID")
        if not self.operation or not isinstance(self.operation, str):
            return FlextResult.error("Invalid operation name")
        return FlextResult.ok(None)


class FlextAlert(FlextEntity):
    """Simplified alert entity using flext-core base."""

    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    severity: str = Field(default="low", description="Alert severity")
    status: str = Field(default="active", description="Alert status")
    tags: dict[str, str] = Field(default_factory=dict, description="Alert tags")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __init__(self, title: str, message: str, severity: str = "low", **kwargs: Any) -> None:
        """Initialize alert with flext-core pattern."""
        super().__init__(
            id=kwargs.get("id", generate_id()),
            title=title,
            message=message,
            severity=severity,
            status=kwargs.get("status", "active"),
            tags=kwargs.get("tags", {}),
            timestamp=kwargs.get("timestamp", datetime.now(UTC)),
        )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate alert domain rules."""
        if not self.title or not isinstance(self.title, str):
            return FlextResult.error("Invalid alert title")
        if not self.message or not isinstance(self.message, str):
            return FlextResult.error("Invalid alert message")
        if self.severity not in {"low", "medium", "high", "critical", "emergency"}:
            return FlextResult.error("Invalid alert severity")
        return FlextResult.ok(None)


class FlextHealthCheck(FlextEntity):
    """Simplified health check entity using flext-core base."""

    component: str = Field(..., description="Component name")
    status: str = Field(default="unknown", description="Health status")
    message: str = Field(default="", description="Health message")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Health metrics")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __init__(self, component: str, status: str = "unknown", message: str = "", **kwargs: Any) -> None:
        """Initialize health check with flext-core pattern."""
        super().__init__(
            id=kwargs.get("id", generate_id()),
            component=component,
            status=status,
            message=message,
            metrics=kwargs.get("metrics", {}),
            timestamp=kwargs.get("timestamp", datetime.now(UTC)),
        )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate health check domain rules."""
        if not self.component or not isinstance(self.component, str):
            return FlextResult.error("Invalid component name")
        if self.status not in {"healthy", "unhealthy", "degraded", "unknown"}:
            return FlextResult.error("Invalid health status")
        return FlextResult.ok(None)
