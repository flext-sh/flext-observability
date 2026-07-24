"""FLEXT Observability Configuration - namespaced under ``settings.Observability``.

Layer-0: imports only stdlib + pydantic + ``FlextSettings``. The universal
runtime fields (``debug``/``trace``/``log_level``/``timezone``/``async_logging``)
come from ``FlextSettings`` by MRO and are NOT redeclared here. Every project
field lives inside the ``Observability`` namespace group with simple scalar types
so each is settable via ``.env`` / env vars / params
(``FLEXT_OBSERVABILITY_OBSERVABILITY__SERVICE_NAME`` …). Defaults are inlined
from ``flext_observability.constants`` (SSOT).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings


class FlextObservabilitySettings(FlextSettings):
    """Observability settings; all project fields under ``settings.Observability.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_", env_nested_delimiter="__", extra="ignore"
    )

    class _Observability(BaseModel):
        """Namespaced observability settings (metrics + traces + alerts)."""

        service_name: Annotated[
            str,
            Field(
                default="flext-observability",
                description="Observability service name identifier",
            ),
        ]
        environment: Annotated[
            str, Field(default="development", description="Deployment environment name")
        ]
        metrics_enabled: Annotated[
            bool, Field(default=True, description="Enable metrics collection")
        ]
        traces_enabled: Annotated[
            bool, Field(default=True, description="Enable distributed tracing")
        ]
        alerts_enabled: Annotated[
            bool, Field(default=True, description="Enable alert notifications")
        ]
        flush_interval_seconds: Annotated[
            int,
            Field(
                default=30,
                ge=1,
                le=300,
                description="Interval in seconds between metric flushes",
            ),
        ]

    if TYPE_CHECKING:
        Observability: _Observability
    else:
        Observability: _Observability = Field(
            default_factory=_Observability,
            description="Namespaced observability settings.",
        )


settings: FlextObservabilitySettings = FlextObservabilitySettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_observability import settings``."""

__all__: list[str] = ["FlextObservabilitySettings", "settings"]
