"""FLEXT Observability Configuration - Unified monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings
from flext_observability import c, t


@FlextSettings.auto_register("observability")
class FlextObservabilitySettings(FlextSettings):
    """Runtime settings for observability components."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_",
        extra="ignore",
    )

    service_name: Annotated[
        str,
        Field(
            default=c.Observability.SettingsDefaults.SERVICE_NAME,
            description="Observability service name identifier",
        ),
    ]
    environment: Annotated[
        str,
        Field(
            default=c.Observability.SettingsDefaults.ENVIRONMENT,
            description="Deployment environment name",
        ),
    ]
    metrics_enabled: Annotated[
        bool,
        Field(
            default=c.Observability.SettingsDefaults.DEFAULT_METRICS_ENABLED,
            description="Enable metrics collection",
        ),
    ]
    traces_enabled: Annotated[
        bool,
        Field(
            default=c.Observability.SettingsDefaults.DEFAULT_TRACES_ENABLED,
            description="Enable distributed tracing",
        ),
    ]
    alerts_enabled: Annotated[
        bool,
        Field(
            default=c.Observability.SettingsDefaults.DEFAULT_ALERTS_ENABLED,
            description="Enable alert notifications",
        ),
    ]
    flush_interval_seconds: Annotated[
        int,
        Field(
            default=c.Observability.SettingsDefaults.DEFAULT_FLUSH_INTERVAL,
            ge=1,
            le=300,
            description="Interval in seconds between metric flushes",
        ),
    ]


__all__: t.StrSequence = ["FlextObservabilitySettings"]
