"""FLEXT Observability Configuration - Unified monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import FlextSettings
from flext_observability import c, m, u


@FlextSettings.auto_register("observability")
class FlextObservabilitySettings(FlextSettings):
    """Runtime settings for observability components."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_", extra="ignore"
    )

    service_name: Annotated[
        str,
        u.Field(
            description="Observability service name identifier",
        ),
    ] = c.Observability.DEFAULT_SETTINGS_SERVICE_NAME
    environment: Annotated[
        str,
        u.Field(
            description="Deployment environment name",
        ),
    ] = c.Observability.DEFAULT_ENVIRONMENT
    metrics_enabled: Annotated[
        bool,
        u.Field(
            description="Enable metrics collection",
        ),
    ] = c.Observability.DEFAULT_METRICS_ENABLED
    traces_enabled: Annotated[
        bool,
        u.Field(
            description="Enable distributed tracing",
        ),
    ] = c.Observability.DEFAULT_TRACES_ENABLED
    alerts_enabled: Annotated[
        bool,
        u.Field(
            description="Enable alert notifications",
        ),
    ] = c.Observability.DEFAULT_ALERTS_ENABLED
    flush_interval_seconds: Annotated[
        int,
        u.Field(
            ge=1,
            le=300,
            description="Interval in seconds between metric flushes",
        ),
    ] = c.Observability.DEFAULT_FLUSH_INTERVAL
