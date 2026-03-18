"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, ClassVar
from uuid import uuid4

from flext_core import FlextModels, t
from pydantic import ConfigDict, Field, computed_field


class FlextObservabilityModels(FlextModels):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class GenericObservabilityEntry(FlextModels.Value):
        """Generic base model for any observability entry using Pydantic."""

        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
        )

        id: Annotated[
            str,
            Field(
                default_factory=lambda: str(uuid4()),
                min_length=1,
                description="Unique entity identifier",
            ),
        ]
        name: Annotated[str, Field(min_length=1, description="Entity name")]
        type: Annotated[str, Field(min_length=1, description="Entity type")]
        timestamp: Annotated[
            datetime,
            Field(
                default_factory=datetime.now,
                description="Entry timestamp",
            ),
        ]
        data: Annotated[
            dict[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Generic data payload",
            ),
        ]
        metadata: Annotated[
            dict[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Generic metadata",
            ),
        ]

        @computed_field
        def age_seconds(self) -> float:
            """Computed age in seconds since creation."""
            return (datetime.now(tz=UTC) - self.timestamp).total_seconds()

        @computed_field
        def data_keys(self) -> list[str]:
            """List of data keys for introspection."""
            return list(self.data.keys()) if self.data else []

        @computed_field
        def has_data(self) -> bool:
            """Check if entry has any data."""
            return bool(self.data)

    class GenericObservabilityConfig(FlextModels.Value):
        """Generic configuration using Pydantic patterns."""

        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
        )

        enabled: Annotated[
            bool,
            Field(default=True, description="Enable observability"),
        ]
        interval_seconds: Annotated[
            float,
            Field(
                gt=0,
                default=60.0,
                description="Collection interval",
            ),
        ]
        retention_days: Annotated[
            int,
            Field(
                ge=1,
                le=365,
                default=30,
                description="Retention period",
            ),
        ]
        settings: Annotated[
            dict[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Type-specific settings",
            ),
        ]

        @computed_field
        def interval_minutes(self) -> float:
            """Computed interval in minutes."""
            return self.interval_seconds / 60.0

        @computed_field
        def retention_hours(self) -> float:
            """Computed retention in hours."""
            return self.retention_days * 24.0

    class Observability:
        """Metrics domain models."""

        class MetricEntry(FlextModels.Entity):
            """Metric entry model."""

            metric_id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            name: Annotated[str, Field(min_length=1)]
            value: float | int
            unit: str
            source: Annotated[str, Field(default="unknown")]


m = FlextObservabilityModels

__all__ = ["FlextObservabilityModels", "m"]
