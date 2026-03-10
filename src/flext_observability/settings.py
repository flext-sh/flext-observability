"""FLEXT Observability Configuration - Unified monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings
from pydantic import ConfigDict, Field


class FlextObservabilitySettings(FlextSettings):
    """Runtime settings for observability components."""

    model_config = ConfigDict(extra="ignore")

    service_name: str = Field(default="flext-observability")
    environment: str = Field(default="development")
    metrics_enabled: bool = Field(default=True)
    traces_enabled: bool = Field(default=True)
    alerts_enabled: bool = Field(default=True)
    flush_interval_seconds: int = Field(default=30, ge=1, le=300)


__all__: list[str] = ["FlextObservabilitySettings"]
