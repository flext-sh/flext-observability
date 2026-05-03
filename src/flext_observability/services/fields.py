"""FLEXT Observability u.Observability.Fields - Unified field validation and definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar

from flext_observability import c, m, u


class FlextObservabilityFields:
    """Unified observability fields class with validation logic.

    Single unified class containing all field validation and definition logic
    for observability entities. Follows FLEXT namespace class pattern.
    """

    METRIC_VALID_UNITS: ClassVar[frozenset[str]] = frozenset({
        "count",
        "percent",
        "bytes",
        "seconds",
        "milliseconds",
        "requests",
        "errors",
        "connections",
        "memory",
        "cpu",
    })

    @classmethod
    def create_alert_message_field(cls) -> m.FieldInfo:
        """Create alert message field."""
        field: m.FieldInfo = u.Field(
            min_length=1,
            max_length=1000,
            description="Alert message",
        )
        return field

    @classmethod
    def create_metric_name_field(cls) -> m.FieldInfo:
        """Create metric name field."""
        field: m.FieldInfo = u.Field(
            min_length=1,
            max_length=255,
            description="Metric name",
        )
        return field

    @classmethod
    def create_metric_unit_field(cls) -> m.FieldInfo:
        """Create metric unit field."""
        field: m.FieldInfo = u.Field(
            c.Observability.DEFAULT_METRIC_UNIT,
            description="Metric unit",
            validate_default=True,
        )
        return field

    @classmethod
    def create_metric_value_field(cls) -> m.FieldInfo:
        """Create metric value field."""
        field: m.FieldInfo = u.Field(ge=0.0, description="Metric value (non-negative)")
        return field

    @classmethod
    def create_timestamp_field(cls) -> m.FieldInfo:
        """Create timestamp field."""
        return m.FieldInfo(
            default_factory=lambda: datetime.now(UTC),
            description="Timestamp",
        )

    @classmethod
    def create_trace_name_field(cls) -> m.FieldInfo:
        """Create trace name field."""
        field: m.FieldInfo = u.Field(
            min_length=1,
            max_length=255,
            description="Trace operation name",
        )
        return field


__all__: list[str] = ["FlextObservabilityFields"]
