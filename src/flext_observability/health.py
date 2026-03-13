"""FLEXT Observability Health Domain Models.

Provides focused health monitoring models following the namespace class pattern.
Contains health check entities, configurations, and factory methods for health operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from flext_core import FlextModels, r, t
from pydantic import BaseModel, Field, ValidationError

from flext_observability import m


class _HealthCheckFactoryKwargs(BaseModel):
    metrics: m.Dict | None = None
    timestamp: datetime | None = None


class HealthCheckModel(BaseModel):
    component: Annotated[str, Field(min_length=1)]
    status: Annotated[str, Field(default="unknown", min_length=1)]
    message: Annotated[str, Field(default="")]
    metrics: Annotated[m.Dict, Field(default_factory=lambda: m.Dict({}))]
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
            valid_kwargs: dict[str, object] = {}
            try:
                parsed_kwargs = _HealthCheckFactoryKwargs.model_validate(kwargs)
                if parsed_kwargs.metrics is not None:
                    valid_kwargs["metrics"] = parsed_kwargs.metrics
                if parsed_kwargs.timestamp is not None:
                    valid_kwargs["timestamp"] = parsed_kwargs.timestamp
            except ValidationError:
                valid_kwargs = {}
            health_check = HealthCheckModel(
                component=component, status=status, message=message
            )
            if valid_kwargs.get("metrics") and isinstance(
                valid_kwargs["metrics"], m.Dict
            ):
                health_check.metrics = valid_kwargs["metrics"]
            if valid_kwargs.get("timestamp") and isinstance(
                valid_kwargs["timestamp"], datetime
            ):
                health_check.timestamp = valid_kwargs["timestamp"]
            return r[HealthCheckModel].ok(health_check)
        except (ValueError, TypeError, KeyError) as e:
            return r[HealthCheckModel].fail(f"Failed to create health check: {e}")


__all__ = ["FlextObservabilityHealth"]
