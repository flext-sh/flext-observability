"""FLEXT Observability Health Domain Models.

Provides focused health monitoring models following the namespace class pattern.
Contains health check entities, configurations, and factory methods for health operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextModels, FlextResult, t
from pydantic import ValidationError

from flext_observability import m


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
        **kwargs: t.ContainerValue,
    ) -> FlextResult[FlextObservabilityHealth.FlextHealthCheck]:
        """Create a FlextHealthCheck entity directly."""
        try:
            valid_kwargs: dict[str, t.ContainerValue] = {}
            try:
                parsed_kwargs = _HealthCheckFactoryKwargs.model_validate(kwargs)  # noqa: F821
                if parsed_kwargs.metrics is not None:
                    valid_kwargs["metrics"] = parsed_kwargs.metrics
                if parsed_kwargs.timestamp is not None:
                    valid_kwargs["timestamp"] = parsed_kwargs.timestamp
            except ValidationError:
                valid_kwargs = {}
            health_check = FlextObservabilityHealth.FlextHealthCheck(
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
            return FlextResult[FlextObservabilityHealth.FlextHealthCheck].ok(
                health_check
            )
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[FlextObservabilityHealth.FlextHealthCheck].fail(
                f"Failed to create health check: {e}"
            )


__all__ = ["FlextObservabilityHealth"]
