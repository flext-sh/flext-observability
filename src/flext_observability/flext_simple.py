"""FlextSimple - Simple observability API for quick setup.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides simple factory functions for observability entities using flext-core.
"""

from __future__ import annotations

# Generate simple IDs without FlextEntityId dependency
import uuid
from datetime import UTC, datetime
from decimal import Decimal

from flext_core import FlextResult

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,  # Import for DRY principle - reuse existing function
    flext_health_check,  # Import for DRY principle - reuse existing function
    flext_trace,  # Import for DRY principle - reuse existing function
)

# ============================================================================
# SIMPLE FACTORY FUNCTIONS FOR OBSERVABILITY ENTITIES
# ============================================================================


def flext_create_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    tags: dict[str, str] | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextMetric]:
    """Create observability metric with simple parameters."""
    try:
        metric = FlextMetric(
            name=name,
            value=Decimal(str(value)),
            unit=unit,
            id=str(uuid.uuid4()),
            tags=tags or {},
            timestamp=timestamp or datetime.now(UTC),
        )
        return FlextResult.ok(metric)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create metric: {e}")


def flext_create_log_entry(
    message: str,
    level: str = "info",
    context: dict[str, object] | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextLogEntry]:
    """Create observability log entry with simple parameters."""
    try:
        log_entry = FlextLogEntry(
            id=str(uuid.uuid4()),
            level=level,
            message=message,
            context=context or {},
            timestamp=timestamp or datetime.now(UTC),
        )
        return FlextResult.ok(log_entry)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create log entry: {e}")


def flext_create_trace(
    trace_id: str,
    operation: str,
    *,
    config: dict[str, object] | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextTrace]:
    """Create observability trace with simple parameters."""
    try:
        config = config or {}
        trace = FlextTrace(
            trace_id=trace_id,
            operation=operation,
            span_id=str(config.get("span_id", f"{trace_id}-span")),
            id=str(uuid.uuid4()),
            duration_ms=int(str(config.get("duration_ms", 0))),
            status=str(config.get("status", "pending")),
            timestamp=timestamp or datetime.now(UTC),
        )
        return FlextResult.ok(trace)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create trace: {e}")


def flext_create_alert(
    title: str,
    message: str,
    severity: str = "low",
    status: str = "active",
    timestamp: datetime | None = None,
) -> FlextResult[FlextAlert]:
    """Create observability alert with simple parameters."""
    try:
        alert = FlextAlert(
            title=title,
            message=message,
            severity=severity,
            id=str(uuid.uuid4()),
            status=status,
            timestamp=timestamp or datetime.now(UTC),
        )
        return FlextResult.ok(alert)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create alert: {e}")


def flext_create_health_check(
    component: str,
    status: str = "unknown",
    message: str = "",
    timestamp: datetime | None = None,
    *,
    id: str | None = None,  # Add optional id parameter for compatibility
) -> FlextResult[FlextHealthCheck]:
    """Create observability health check with simple parameters."""
    try:
        health_check = FlextHealthCheck(
            id=id or str(uuid.uuid4()),  # Use provided id or generate new one
            component=component,
            status=status,
            message=message,
            timestamp=timestamp or datetime.now(UTC),
        )
        return FlextResult.ok(health_check)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to create health check: {e}")


__all__ = [
    "flext_alert",  # Re-expose from entities for DRY principle
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",  # Re-expose from entities for DRY principle
    "flext_trace",  # Re-expose from entities for DRY principle
]
