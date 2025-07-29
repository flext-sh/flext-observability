"""FLEXT Observability Entities - Simplified using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Entities simplificadas usando apenas padrões essenciais do flext-core.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

# Note: Removed Any import - using object instead for better type safety
from flext_core import FlextEntity, FlextResult
from pydantic import Field

if TYPE_CHECKING:
    from decimal import Decimal

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
        default_factory=dict, description="Span attributes",
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
        default_factory=dict, description="Health metrics",
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
# PYDANTIC MODEL REBUILDING - Fix "not fully defined" errors
# ============================================================================

# Rebuild all models after Decimal import to fix Pydantic forward reference issues
FlextMetric.model_rebuild()
FlextLogEntry.model_rebuild()
FlextAlert.model_rebuild()
FlextTrace.model_rebuild()
FlextHealthCheck.model_rebuild()
