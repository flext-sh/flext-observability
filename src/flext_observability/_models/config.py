"""flext-observability config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/observability.yaml`` business-rule
SSOT. The ``_config.py`` facade validates the model-less YAML slice into these
classes and exposes the ready objects under ``config.Observability``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextObservabilityConfigModels:
    """Namespace of typed flext-observability config models."""

    class Service(BaseModel):
        """Service identity defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_name: str = Field(description="Default service name.")
        default_settings_name: str = Field(description="Default settings service name.")
        default_environment: str = Field(description="Default deployment environment.")

    class Defaults(BaseModel):
        """Default observability feature flags and units."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        log_level: str = Field(description="Default log level.")
        metric_unit: str = Field(description="Default metric unit.")
        flush_interval_seconds: int = Field(
            ge=1, description="Default flush interval in seconds."
        )
        metrics_enabled: bool = Field(
            description="Default metrics collection enabled flag."
        )
        traces_enabled: bool = Field(description="Default tracing enabled flag.")
        alerts_enabled: bool = Field(description="Default alerting enabled flag.")

    class Thresholds(BaseModel):
        """Observability thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        http_error_status: int = Field(
            ge=100,
            le=599,
            description="HTTP status code threshold for error classification.",
        )

    class Validation(BaseModel):
        """Observability payload validation limits."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        metric_name_max_length: int = Field(
            ge=1, description="Maximum metric name length."
        )
        trace_name_max_length: int = Field(
            ge=1, description="Maximum trace name length."
        )
        alert_message_max_length: int = Field(
            ge=1, description="Maximum alert message length."
        )
        log_message_max_length: int = Field(
            ge=1, description="Maximum log message length."
        )
        valid_metric_units: frozenset[str] = Field(
            description="Allowed metric unit strings."
        )

    class Observability(BaseModel):
        """Root observability business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        service: FlextObservabilityConfigModels.Service = Field(
            description="Service identity defaults."
        )
        defaults: FlextObservabilityConfigModels.Defaults = Field(
            description="Default observability feature flags and units."
        )
        thresholds: FlextObservabilityConfigModels.Thresholds = Field(
            description="Observability thresholds."
        )
        validation: FlextObservabilityConfigModels.Validation = Field(
            description="Observability payload validation limits."
        )

    class Root(BaseModel):
        """Root flext-observability config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        Observability: FlextObservabilityConfigModels.Observability = Field(
            description="Observability business-rule config namespace."
        )


__all__: list[str] = ["FlextObservabilityConfigModels"]
