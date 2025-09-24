"""FLEXT Observability Configuration - Monitoring and observability settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextModels, FlextResult, FlextTypes


class FlextObservabilityMetricsConfig(FlextModels.Config):
    """Metrics collection configuration."""

    enabled: bool = Field(
        default=True,
        description="Enable metrics collection",
    )
    export_interval_seconds: int = Field(
        default=60,
        description="Metrics export interval in seconds",
        gt=0,
        le=3600,
    )
    namespace: str = Field(
        default="flext",
        description="Metrics namespace",
    )
    include_host_metrics: bool = Field(
        default=True,
        description="Include host system metrics",
    )
    include_process_metrics: bool = Field(
        default=True,
        description="Include process metrics",
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate metrics configuration business rules."""
        if self.export_interval_seconds < 1:
            return FlextResult[None].fail("Export interval must be positive")
        if not self.namespace or not self.namespace.strip():
            return FlextResult[None].fail("Metrics namespace cannot be empty")
        return FlextResult[None].ok(None)


class FlextObservabilityTracingConfig(FlextModels.Config):
    """Distributed tracing configuration."""

    enabled: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )
    sampling_rate: float = Field(
        default=1.0,
        description="Trace sampling rate (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )
    exporter_endpoint: str | None = Field(
        default=None,
        description="Trace exporter endpoint URL",
    )
    service_name: str = Field(
        default="flext-service",
        description="Service name for traces",
    )
    max_span_attributes: int = Field(
        default=128,
        description="Maximum number of span attributes",
        gt=0,
        le=1000,
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate tracing configuration business rules."""
        if self.sampling_rate < 0.0 or self.sampling_rate > 1.0:
            return FlextResult[None].fail("Sampling rate must be between 0.0 and 1.0")
        if not self.service_name or not self.service_name.strip():
            return FlextResult[None].fail("Service name cannot be empty")
        return FlextResult[None].ok(None)


class FlextObservabilityMonitoringConfig(FlextModels.Config):
    """Health monitoring configuration."""

    enabled: bool = Field(
        default=True,
        description="Enable health monitoring",
    )
    check_interval_seconds: int = Field(
        default=30,
        description="Health check interval in seconds",
        gt=0,
        le=3600,
    )
    alert_on_failure: bool = Field(
        default=True,
        description="Send alerts on health check failures",
    )
    failure_threshold: int = Field(
        default=3,
        description="Number of failures before alerting",
        gt=0,
        le=10,
    )
    include_dependency_checks: bool = Field(
        default=True,
        description="Include dependency health checks",
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate monitoring configuration business rules."""
        if self.check_interval_seconds < 1:
            return FlextResult[None].fail("Check interval must be positive")
        if self.failure_threshold < 1:
            return FlextResult[None].fail("Failure threshold must be positive")
        return FlextResult[None].ok(None)


class FlextObservabilityConfig(FlextConfig):
    """Complete observability configuration using FlextConfig patterns.

    Provides comprehensive monitoring, metrics, tracing, and health check
    configuration for the FLEXT observability system.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_",
        case_sensitive=False,
    )

    # Structured configuration using value objects
    metrics: FlextObservabilityMetricsConfig = Field(
        default_factory=FlextObservabilityMetricsConfig,
        description="Metrics collection configuration",
    )
    tracing: FlextObservabilityTracingConfig = Field(
        default_factory=FlextObservabilityTracingConfig,
        description="Distributed tracing configuration",
    )
    monitoring: FlextObservabilityMonitoringConfig = Field(
        default_factory=FlextObservabilityMonitoringConfig,
        description="Health monitoring configuration",
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Observability logging level",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
    )
    structured_logging: bool = Field(
        default=True,
        description="Enable structured logging",
    )

    # Project identification
    project_name: str = Field(
        default="flext-observability",
        description="Project name",
    )
    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    def validate_domain_rules(self: object) -> FlextResult[None]:
        """Validate complete observability configuration."""
        validations = [
            ("Metrics", self.metrics.validate_business_rules()),
            ("Tracing", self.tracing.validate_business_rules()),
            ("Monitoring", self.monitoring.validate_business_rules()),
        ]

        for section_name, validation_result in validations:
            if not validation_result.success:
                return FlextResult[None].fail(
                    f"{section_name} validation failed: {validation_result.error}",
                )

        return FlextResult[None].ok(None)

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Alias to validate_domain_rules for business rule validation."""
        return self.validate_domain_rules()

    @classmethod
    def create_with_defaults(
        cls,
        **overrides: FlextTypes.Core.Dict,
    ) -> FlextObservabilityConfig:
        """Create configuration with intelligent defaults."""
        defaults = {
            "metrics": FlextObservabilityMetricsConfig(),
            "tracing": FlextObservabilityTracingConfig(),
            "monitoring": FlextObservabilityMonitoringConfig(),
            "log_level": "INFO",
            "structured_logging": True,
            "project_name": "flext-observability",
            "project_version": "0.9.0",
        }
        defaults.update(overrides)
        return cls.model_validate(defaults)


__all__: FlextTypes.Core.StringList = [
    "FlextObservabilityConfig",
    "FlextObservabilityMetricsConfig",
    "FlextObservabilityMonitoringConfig",
    "FlextObservabilityTracingConfig",
]
