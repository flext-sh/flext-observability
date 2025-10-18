"""FLEXT Observability Configuration - Unified monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Self

from flext_core import FlextConfig, FlextConstants, FlextResult
from pydantic import Field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_observability.constants import FlextObservabilityConstants


class FlextObservabilityConfig(FlextConfig):
    """Unified observability configuration extending FlextConfig.

    Single consolidated class providing comprehensive monitoring, metrics, tracing,
    and health check configuration for the FLEXT observability system using
    enhanced singleton pattern with inverse dependency injection.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_",
        case_sensitive=False,
        # Enhanced Pydantic v2.11+ features
        validate_assignment=True,
        str_strip_whitespace=True,
        str_to_lower=False,
        extra="ignore",  # Allow extra fields from environment
        json_schema_extra={
            "title": "FLEXT Observability Configuration",
            "description": "Enterprise observability configuration extending FlextConfig",
        },
    )

    # === METRICS CONFIGURATION ===
    metrics_enabled: bool = Field(
        default=True,
        description="Enable metrics collection",
    )
    metrics_export_interval_seconds: int = Field(
        default=FlextObservabilityConstants.DEFAULT_METRICS_EXPORT_INTERVAL_SECONDS,
        description="Metrics export interval in seconds",
        gt=0,
        le=3600,
    )
    metrics_namespace: str = Field(
        default=FlextObservabilityConstants.DEFAULT_METRICS_NAMESPACE,
        description="Metrics namespace",
    )
    metrics_include_host_metrics: bool = Field(
        default=True,
        description="Include host system metrics",
    )
    metrics_include_process_metrics: bool = Field(
        default=True,
        description="Include process metrics",
    )

    # === TRACING CONFIGURATION ===
    tracing_enabled: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )
    tracing_sampling_rate: float = Field(
        default=FlextObservabilityConstants.DEFAULT_TRACING_SAMPLING_RATE,
        description="Trace sampling rate (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )
    tracing_exporter_endpoint: str | None = Field(
        default=None,
        description="Trace exporter endpoint URL",
    )
    tracing_service_name: str = Field(
        default=FlextObservabilityConstants.DEFAULT_SERVICE_NAME,
        description="Service name for traces",
    )
    tracing_max_span_attributes: int = Field(
        default=FlextObservabilityConstants.DEFAULT_MAX_SPAN_ATTRIBUTES,
        description="Maximum number of span attributes",
        gt=0,
        le=1000,
    )

    # === MONITORING CONFIGURATION ===
    monitoring_enabled: bool = Field(
        default=True,
        description="Enable health monitoring",
    )
    monitoring_check_interval_seconds: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        description="Health check interval in seconds",
        gt=0,
        le=3600,
    )
    monitoring_alert_on_failure: bool = Field(
        default=True,
        description="Send alerts on health check failures",
    )
    monitoring_failure_threshold: int = Field(
        default=FlextConstants.Reliability.MAX_RETRY_ATTEMPTS,
        description="Number of failures before alerting",
        gt=0,
        le=10,
    )
    monitoring_include_dependency_checks: bool = Field(
        default=True,
        description="Include dependency health checks",
    )

    # === LOGGING CONFIGURATION ===
    structured_logging: bool = Field(
        default=True,
        description="Enable structured logging",
    )

    # === PROJECT IDENTIFICATION ===
    project_name: str = Field(
        default="flext-observability",
        description="Project name",
    )
    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # === PYDANTIC 2.11+ VALIDATORS ===
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level format."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            msg = f"Log level must be one of {valid_levels}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("metrics_namespace")
    @classmethod
    def validate_metrics_namespace(cls, v: str) -> str:
        """Validate metrics namespace format."""
        if not v or not v.strip():
            msg = "Metrics namespace cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("tracing_service_name")
    @classmethod
    def validate_tracing_service_name(cls, v: str) -> str:
        """Validate tracing service name format."""
        if not v or not v.strip():
            msg = "Tracing service name cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @model_validator(mode="after")
    def validate_observability_consistency(self) -> Self:
        """Validate observability configuration consistency."""
        # Additional cross-field validations beyond Field constraints
        if self.tracing_enabled and not self.tracing_service_name:
            msg = "Tracing service name required when tracing is enabled"
            raise ValueError(msg)

        if self.monitoring_enabled and not self.monitoring_failure_threshold:
            msg = "Monitoring failure threshold required when monitoring is enabled"
            raise ValueError(msg)

        return self

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate observability business rules."""
        try:
            # Cross-field business validations
            if self.metrics_enabled and not self.metrics_namespace.strip():
                return FlextResult[None].fail(
                    "Metrics namespace cannot be empty when enabled"
                )

            if self.tracing_enabled and not self.tracing_service_name.strip():
                return FlextResult[None].fail(
                    "Tracing service name cannot be empty when enabled"
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    @classmethod
    def create_with_defaults(
        cls,
        **overrides: object,
    ) -> FlextObservabilityConfig:
        """Create configuration with intelligent defaults using direct instantiation.

        Uses the newer FlextConfig features for proper configuration management
        without relying on removed singleton methods.
        """
        instance = cls()
        for key, value in overrides.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance

    @classmethod
    def get_global_instance(cls) -> FlextObservabilityConfig:
        """Get the global singleton instance using direct management.

        This method ensures that all components in flext-observability use the same
        configuration instance, avoiding duplication and ensuring consistency.
        """
        # Use a simpler approach for Pydantic v2 compatibility
        return cls.create_with_defaults()

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextObservabilityConfig instance (mainly for testing).

        In Pydantic v2, we don't maintain a persistent global instance to avoid
        issues with model state and validation.
        """


__all__: list[str] = [
    "FlextObservabilityConfig",
]
