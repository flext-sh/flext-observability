"""FLEXT Observability Configuration - Unified monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings
from flext_observability import t


class FlextObservabilitySettings(FlextSettings):
    """Runtime settings for observability components."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")

    service_name: Annotated[str, Field(default="flext-observability")]
    environment: Annotated[str, Field(default="development")]
    metrics_enabled: Annotated[bool, Field(default=True)]
    traces_enabled: Annotated[bool, Field(default=True)]
    alerts_enabled: Annotated[bool, Field(default=True)]
    flush_interval_seconds: Annotated[int, Field(default=30, ge=1, le=300)]


__all__: t.StrSequence = ["FlextObservabilitySettings"]
