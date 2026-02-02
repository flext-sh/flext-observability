"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from flext_core import FlextTypes as t, m as m_core
from flext_core.utilities import u as flext_u
from pydantic import BaseModel, ConfigDict, Field, computed_field


class FlextObservabilityModels(m_core):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextObservabilityModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        flext_u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextObservabilityModels is deprecated. Use FlextModels directly with composition instead.",
        )

    class GenericObservabilityEntry(m_core.Value):
        """Generic base model for any observability entry using Pydantic."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
            json_encoders={datetime: lambda v: v.isoformat()},
        )

        id: str = Field(
            default_factory=lambda: str(uuid4()),
            min_length=1,
            description="Unique entity identifier",
        )
        name: str = Field(min_length=1, description="Entity name")
        type: str = Field(min_length=1, description="Entity type")
        timestamp: datetime = Field(
            default_factory=datetime.now,
            description="Entry timestamp",
        )
        data: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Generic data payload",
        )
        metadata: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Generic metadata",
        )

        @computed_field
        @property
        def age_seconds(self) -> float:
            """Computed age in seconds since creation."""
            return (datetime.now(tz=UTC) - self.timestamp).total_seconds()

        @computed_field
        @property
        def has_data(self) -> bool:
            """Check if entry has any data."""
            return bool(self.data)

        @computed_field
        @property
        def data_keys(self) -> list[str]:
            """List of data keys for introspection."""
            return list(self.data.keys()) if self.data else []

    class GenericObservabilityConfig(BaseModel):
        """Generic configuration using Pydantic patterns."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
        )

        enabled: bool = Field(default=True, description="Enable observability")
        interval_seconds: float = Field(
            gt=0,
            default=60.0,
            description="Collection interval",
        )
        retention_days: int = Field(
            ge=1,
            le=365,
            default=30,
            description="Retention period",
        )
        settings: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Type-specific settings",
        )

        @computed_field
        @property
        def interval_minutes(self) -> float:
            """Computed interval in minutes."""
            return self.interval_seconds / 60.0

        @computed_field
        @property
        def retention_hours(self) -> float:
            """Computed retention in hours."""
            return self.retention_days * 24.0

    class Observability:
        """Metrics domain models."""

        class MetricEntry(m_core.Entity):
            """Metric entry model."""

            metric_id: str = Field(default_factory=lambda: str(uuid4()))
            name: str = Field(min_length=1)
            value: float | int
            unit: str
            source: str = Field(default="unknown")


m = FlextObservabilityModels
m_observability = FlextObservabilityModels

__all__ = ["FlextObservabilityModels", "m", "m_observability"]
