"""FLEXT Observability Health Domain Models.

Provides focused health monitoring models following the namespace class pattern.
Contains health check entities, configurations, and factory methods for health operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from flext_core import FlextModels, r
from flext_core.typings import t
from pydantic import BaseModel, Field, ValidationError


class _HealthCheckFactoryKwargs(BaseModel):
    metrics: t.Dict | None = None
    timestamp: datetime | None = None


class HealthCheckModel(BaseModel):
    component: Annotated[str, Field(min_length=1)]
    status: Annotated[str, Field(default="unknown", min_length=1)]
    message: Annotated[str, Field(default="")]
    metrics: Annotated[t.Dict, Field(default_factory=lambda: t.Dict({}))]
    timestamp: Annotated[datetime, Field(default_factory=datetime.now)]


class FlextObservabilityHealth(FlextModels):
    """Focused health monitoring models for observability operations extending FlextModels.

    Provides complete health check entities, configurations, and operations
    for service health monitoring, status tracking, and health validation within the FLEXT ecosystem.
    """

    @staticmethod
    def flext_health_check(
        component: str,
        status: str = "unknown",
        message: str = "",
        **kwargs: t.Scalar,
    ) -> r[HealthCheckModel]:
        """Create a FlextHealthCheck entity directly."""
        try:
            valid_metrics: t.Dict | None = None
            valid_timestamp: datetime | None = None
            try:
                parsed_kwargs = _HealthCheckFactoryKwargs.model_validate(obj=kwargs)
                if parsed_kwargs.metrics is not None:
                    valid_metrics = parsed_kwargs.metrics
                if parsed_kwargs.timestamp is not None:
                    valid_timestamp = parsed_kwargs.timestamp
            except ValidationError:
                valid_metrics = None
                valid_timestamp = None
            health_check = HealthCheckModel(
                component=component,
                status=status,
                message=message,
                metrics=t.Dict({}),
                timestamp=datetime.now(UTC),
            )
            if valid_metrics is not None:
                health_check.metrics = valid_metrics
            if valid_timestamp is not None:
                health_check.timestamp = valid_timestamp
            return r[HealthCheckModel].ok(health_check)
        except (ValueError, TypeError, KeyError) as e:
            return r[HealthCheckModel].fail(f"Failed to create health check: {e}")


__all__ = ["FlextObservabilityHealth"]
