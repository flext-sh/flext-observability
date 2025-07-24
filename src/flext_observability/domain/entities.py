"""Domain Entities - Core business entities using flext-core bases.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Domain Layer
Following SOLID, KISS, DRY principles using flext-core as foundation.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from flext_core import BaseEntity, EntityId

if TYPE_CHECKING:
    from typing import Any


class Metric(BaseEntity):
    """Metric entity - Single Responsibility for metric domain logic."""

    def __init__(
        self,
        entity_id: EntityId | None = None,
        name: str = "",
        value: Decimal = Decimal(0),
        unit: str = "",
        timestamp: datetime | None = None,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Initialize metric entity."""
        super().__init__(entity_id)
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = timestamp or datetime.now()
        self.tags = tags or {}

    def validate(self) -> bool:
        """Validate metric entity state."""
        return bool(self.name and self.unit)


class LogEntry(BaseEntity):
    """Log entry entity - Single Responsibility for log domain logic."""

    def __init__(
        self,
        entity_id: EntityId | None = None,
        level: str = "info",
        message: str = "",
        timestamp: datetime | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize log entry entity."""
        super().__init__(entity_id)
        self.level = level
        self.message = message
        self.timestamp = timestamp or datetime.now()
        self.context = context or {}

    def validate(self) -> bool:
        """Validate log entry entity state."""
        return bool(self.message and self.level)


class Trace(BaseEntity):
    """Trace entity - Single Responsibility for tracing domain logic."""

    def __init__(
        self,
        entity_id: EntityId | None = None,
        trace_id: str = "",
        span_id: str = "",
        operation: str = "",
        duration_ms: int = 0,
        status: str = "pending",
        timestamp: datetime | None = None,
    ) -> None:
        """Initialize trace entity."""
        super().__init__(entity_id)
        self.trace_id = trace_id
        self.span_id = span_id
        self.operation = operation
        self.duration_ms = duration_ms
        self.status = status
        self.timestamp = timestamp or datetime.now()

    def validate(self) -> bool:
        """Validate trace entity state."""
        return bool(self.trace_id and self.operation)


class Alert(BaseEntity):
    """Alert entity - Single Responsibility for alert domain logic."""

    def __init__(
        self,
        entity_id: EntityId | None = None,
        title: str = "",
        message: str = "",
        severity: str = "low",
        status: str = "active",
        timestamp: datetime | None = None,
    ) -> None:
        """Initialize alert entity."""
        super().__init__(entity_id)
        self.title = title
        self.message = message
        self.severity = severity
        self.status = status
        self.timestamp = timestamp or datetime.now()

    def validate(self) -> bool:
        """Validate alert entity state."""
        return bool(self.title and self.message)


class HealthCheck(BaseEntity):
    """Health check entity - Single Responsibility for health domain logic."""

    def __init__(
        self,
        entity_id: EntityId | None = None,
        component: str = "",
        status: str = "unknown",
        message: str = "",
        timestamp: datetime | None = None,
    ) -> None:
        """Initialize health check entity."""
        super().__init__(entity_id)
        self.component = component
        self.status = status
        self.message = message
        self.timestamp = timestamp or datetime.now()

    def validate(self) -> bool:
        """Validate health check entity state."""
        return bool(self.component)
