"""FlextSimple - Simple observability API for quick setup.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides simple factory functions for observability entities using flext-core.
"""

from __future__ import annotations

# Generate simple IDs without FlextEntityId dependency
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from flext_core import FlextResult

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
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
            entity_id=str(uuid.uuid4()),
            tags=tags or {},
            timestamp=timestamp or datetime.now(),
        )
        return FlextResult.ok(metric)
    except Exception as e:
        return FlextResult.error(f"Failed to create metric: {e}")


def flext_create_log_entry(
    message: str,
    level: str = "info",
    context: dict[str, Any] | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextLogEntry]:
    """Create observability log entry with simple parameters."""
    try:
        log_entry = FlextLogEntry(
            entity_id=str(uuid.uuid4()),
            level=level,
            message=message,
            context=context or {},
            timestamp=timestamp or datetime.now(),
        )
        return FlextResult.ok(log_entry)
    except Exception as e:
        return FlextResult.error(f"Failed to create log entry: {e}")


def flext_create_trace(
    trace_id: str,
    operation: str,
    span_id: str = "",
    duration_ms: int = 0,
    status: str = "pending",
    timestamp: datetime | None = None,
) -> FlextResult[FlextTrace]:
    """Create observability trace with simple parameters."""
    try:
        trace = FlextTrace(
            trace_id=trace_id,
            operation=operation,
            span_id=span_id or f"{trace_id}-span",
            entity_id=str(uuid.uuid4()),
            duration_ms=duration_ms,
            status=status,
            timestamp=timestamp or datetime.now(),
        )
        return FlextResult.ok(trace)
    except Exception as e:
        return FlextResult.error(f"Failed to create trace: {e}")


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
            entity_id=str(uuid.uuid4()),
            status=status,
            timestamp=timestamp or datetime.now(),
        )
        return FlextResult.ok(alert)
    except Exception as e:
        return FlextResult.error(f"Failed to create alert: {e}")


def flext_create_health_check(
    component: str,
    status: str = "unknown",
    message: str = "",
    timestamp: datetime | None = None,
) -> FlextResult[FlextHealthCheck]:
    """Create observability health check with simple parameters."""
    try:
        health_check = FlextHealthCheck(
            entity_id=str(uuid.uuid4()),
            component=component,
            status=status,
            message=message,
            timestamp=timestamp or datetime.now(),
        )
        return FlextResult.ok(health_check)
    except Exception as e:
        return FlextResult.error(f"Failed to create health check: {e}")


__all__ = [
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
]
