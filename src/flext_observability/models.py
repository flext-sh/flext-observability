"""Generic FLEXT Observability Models.

Minimal, generic Pydantic models following FLEXT principles with zero domain-specific logic.
Single unified class for all observability entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from flext_core import FlextModels
from pydantic import BaseModel, ConfigDict, Field


class FlextObservabilityModels(FlextModels):
    """Generic observability models extending FlextModels.

    Single class providing generic base models for any observability entity type.
    No domain-specific validation or computed fields - pure generic foundation.
    """

    class GenericObservabilityEntry(FlextModels.Value):
        """Generic base model for any observability entry."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
        )

        id: str = Field(
            default_factory=lambda: str(uuid4()), description="Unique entity identifier"
        )
        name: str = Field(description="Entity name")
        type: str = Field(description="Entity type (metric, trace, alert, health, log)")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Entry timestamp"
        )
        data: dict[str, Any] = Field(
            default_factory=dict, description="Generic data payload"
        )
        metadata: dict[str, Any] = Field(
            default_factory=dict, description="Generic metadata"
        )

    class GenericObservabilityConfig(BaseModel):
        """Generic configuration model for observability settings."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        enabled: bool = Field(default=True, description="Enable observability")
        interval_seconds: float = Field(
            default=60.0, description="Collection/check interval"
        )
        retention_days: int = Field(default=30, description="Data retention period")
        settings: dict[str, Any] = Field(
            default_factory=dict, description="Type-specific settings"
        )


__all__ = ["FlextObservabilityModels"]
