"""Declarative configuration for observability using flext-core unified patterns.

Copyright (c) 2025, ALGAR. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from decimal import Decimal

from flext_core import BaseConfig, EnvironmentLiteral, LogLevel
from flext_core.config.unified_config import (
    BaseConfigMixin,
    LoggingConfigMixin,
    MonitoringConfigMixin,
    PerformanceConfigMixin,
)
from flext_core.domain.constants import ConfigDefaults
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MetricsConfig(BaseConfig):
    """Configuration for metrics collection."""

    collection_interval_seconds: int = Field(
        default=30,
        description="Interval for metrics collection in seconds",
        ge=1,
        le=3600,
    )

    retention_days: int = Field(
        default=30,
        description="Number of days to retain metrics",
        ge=1,
        le=365,
    )

    max_metrics_per_name: int = Field(
        default=10000,
        description="Maximum number of metrics per metric name",
        ge=100,
        le=50000,
    )

    enable_anomaly_detection: bool = Field(
        default=True,
        description="Enable anomaly detection for metrics",
    )

    anomaly_threshold_std_dev: float = Field(
        default=2.0,
        description="Standard deviation threshold for anomaly detection",
        ge=1.0,
        le=5.0,
    )


class AlertingConfig(BaseConfig):
    """Configuration for alerting."""

    enable_alerts: bool = Field(
        default=True,
        description="Enable alert generation",
    )

    default_severity: str = Field(
        default="medium",
        description="Default alert severity",
    )

    notification_channels: list[str] = Field(
        default_factory=list,
        description="List of notification channels",
    )

    email_recipients: list[str] = Field(
        default_factory=list,
        description="Email recipients for alerts",
    )

    auto_resolve_after_seconds: int = Field(
        default=3600,
        description="Auto-resolve alerts after this many seconds",
        ge=300,
        le=86400,
    )


class HealthCheckConfig(BaseConfig):
    """Configuration for health checks."""

    check_interval_seconds: int = Field(
        default=30,
        description="Interval for health checks in seconds",
        ge=10,
        le=3600,
    )

    timeout_seconds: int = Field(
        default=5,
        description="Timeout for health check requests",
        ge=1,
        le=60,
    )

    failure_threshold: int = Field(
        default=3,
        description="Number of failures before marking unhealthy",
        ge=1,
        le=10,
    )

    success_threshold: int = Field(
        default=2,
        description="Number of successes before marking healthy",
        ge=1,
        le=10,
    )

    enable_dependency_checks: bool = Field(
        default=True,
        description="Enable dependency health checks",
    )


class LoggingConfig(BaseConfig):
    """Configuration for logging using flext-core types."""

    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Minimum log level to capture",
    )

    structured_logging: bool = Field(
        default=True,
        description="Use structured logging format",
    )

    log_to_file: bool = Field(
        default=False,
        description="Enable logging to file",
    )

    log_file_path: str = Field(
        default="./logs/flext-infrastructure.monitoring.flext-observability.log",
        description="Path to log file",
    )

    log_rotation_size_mb: int = Field(
        default=50,
        description="Log file rotation size in MB",
        ge=1,
        le=500,
    )

    max_log_size_mb: int = Field(
        default=100,
        description="Maximum log file size in MB",
        ge=1,
        le=1000,
    )

    retention_days: int = Field(
        default=7,
        description="Number of days to retain log files",
        ge=1,
        le=365,
    )


class TracingConfig(BaseConfig):
    """Configuration for distributed tracing."""

    enable_tracing: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )

    sampling_rate: float = Field(
        default=0.1,
        description="Trace sampling rate (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    max_trace_duration_seconds: int = Field(
        default=300,
        description="Maximum trace duration in seconds",
        ge=1,
        le=3600,
    )

    export_batch_size: int = Field(
        default=100,
        description="Batch size for trace export",
        ge=1,
        le=1000,
    )

    export_timeout_seconds: int = Field(
        default=30,
        description="Timeout for trace export",
        ge=1,
        le=300,
    )


class ExporterConfig(BaseConfig):
    """Configuration for metric and trace exporters."""

    prometheus_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics export",
    )

    prometheus_port: int = Field(
        default=9090,
        description="Port for Prometheus metrics endpoint",
        ge=1024,
        le=65535,
    )

    otlp_enabled: bool = Field(
        default=False,
        description="Enable OTLP trace export",
    )

    otlp_endpoint: str = Field(
        default="http://localhost:4317",
        description="OTLP endpoint URL",
    )

    export_interval_seconds: int = Field(
        default=10,
        description="Interval for exporting data",
        ge=1,
        le=300,
    )


class ThresholdConfig(BaseConfig):
    """Configuration for metric thresholds."""

    cpu_usage_warning: Decimal = Field(
        default=Decimal("80.0"),
        description="CPU usage warning threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    cpu_usage_critical: Decimal = Field(
        default=Decimal("90.0"),
        description="CPU usage critical threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    memory_usage_warning: Decimal = Field(
        default=Decimal("85.0"),
        description="Memory usage warning threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    memory_usage_critical: Decimal = Field(
        default=Decimal("95.0"),
        description="Memory usage critical threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    disk_usage_warning: Decimal = Field(
        default=Decimal("80.0"),
        description="Disk usage warning threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    disk_usage_critical: Decimal = Field(
        default=Decimal("90.0"),
        description="Disk usage critical threshold percentage",
        ge=Decimal("0.0"),
        le=Decimal("100.0"),
    )

    response_time_warning_ms: int = Field(
        default=1000,
        description="Response time warning threshold in milliseconds",
        ge=1,
        le=60000,
    )

    response_time_critical_ms: int = Field(
        default=5000,
        description="Response time critical threshold in milliseconds",
        ge=1,
        le=60000,
    )


class ObservabilitySettings(
    BaseConfigMixin,
    LoggingConfigMixin,
    MonitoringConfigMixin,
    PerformanceConfigMixin,
    BaseSettings,
):
    """Main observability settings using unified configuration mixins."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Override project info with observability-specific values
    project_name: str = Field(
        default="flext-infrastructure.monitoring.flext-observability",
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    project_version: str = Field(default="0.7.0")

    # Configuration sections using declarative patterns
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    alerting: AlertingConfig = Field(default_factory=AlertingConfig)
    health_checks: HealthCheckConfig = Field(default_factory=HealthCheckConfig)
    # Note: logging inherited from LoggingConfigMixin
    tracing: TracingConfig = Field(default_factory=TracingConfig)
    exporters: ExporterConfig = Field(default_factory=ExporterConfig)
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)

    # Global settings
    enable_observability: bool = Field(
        default=True,
        description="Master switch for observability features",
    )

    data_dir: str = Field(
        default="./data/flext-infrastructure.monitoring.flext-observability",
        description="Directory for storing observability data",
    )

    max_memory_usage_mb: int = Field(
        default=512,
        description="Maximum memory usage in MB",
        ge=64,
        le=4096,
    )

    cleanup_interval_hours: int = Field(
        default=24,
        description="Interval for cleanup operations in hours",
        ge=1,
        le=168,
    )

    # Note: Most common settings now inherited from mixins:
    # - BaseConfigMixin: project_name, project_version, environment, debug
    # - LoggingConfigMixin: log_level, log_file, log_format, log_rotation
    # - MonitoringConfigMixin: metrics_enabled, health_check_enabled, prometheus_port
    # - PerformanceConfigMixin: batch_size, timeout_seconds, retry_count


# Global configuration instance
_settings: ObservabilitySettings | None = None


def get_settings() -> ObservabilitySettings:
    """Get the settings.

    Returns:
        The settings.

    """
    global _settings
    if _settings is None:
        _settings = ObservabilitySettings()
    return _settings


def configure_observability(settings: ObservabilitySettings) -> None:
    """Configure the observability.

    Args:
        settings: The settings.

    """
    global _settings
    _settings = settings


# Helper functions for common configurations
def create_development_config() -> ObservabilitySettings:
    """Create a development configuration.

    Returns:
        The development configuration.

    """
    return ObservabilitySettings(
        project_name="flext-observability-dev",
        debug=True,
        environment="development",
        metrics=MetricsConfig(
            collection_interval_seconds=10,
            retention_days=1,
        ),
        alerting=AlertingConfig(
            enable_alerts=False,  # Disable alerts in development
        ),
        # Note: Logging settings now from LoggingConfigMixin
        log_level=LogLevel.DEBUG,  # From LoggingConfigMixin
        log_file="./logs/flext-observability-dev.log",  # From LoggingConfigMixin
        tracing=TracingConfig(
            sampling_rate=1.0,  # Sample all traces in development
        ),
    )


def create_production_config() -> ObservabilitySettings:
    """Create a production configuration.

    Returns:
        The production configuration.

    """
    return ObservabilitySettings(
        project_name="flext-observability-prod",
        debug=False,
        environment="production",
        metrics=MetricsConfig(
            collection_interval_seconds=60,
            retention_days=30,
        ),
        alerting=AlertingConfig(
            enable_alerts=True,
            auto_resolve_after_seconds=7200,
        ),
        # Note: Logging settings now from LoggingConfigMixin
        log_level=LogLevel.INFO,  # From LoggingConfigMixin
        log_file="./logs/flext-observability-prod.log",  # From LoggingConfigMixin
        tracing=TracingConfig(
            sampling_rate=0.01,  # Sample 1% of traces in production
        ),
    )


def create_testing_config() -> ObservabilitySettings:
    """Create a testing configuration.

    Returns:
        The testing configuration.

    """
    return ObservabilitySettings(
        project_name="flext-observability-test",
        debug=True,
        environment="test",
        metrics=MetricsConfig(
            collection_interval_seconds=1,
            retention_days=1,
            max_metrics_per_name=100,
        ),
        alerting=AlertingConfig(
            enable_alerts=False,  # Disable alerts in tests
        ),
        # Note: Logging settings now from LoggingConfigMixin
        log_level=LogLevel.WARNING,  # From LoggingConfigMixin
        log_file=None,  # No log file for tests
        tracing=TracingConfig(
            enable_tracing=False,  # Disable tracing in tests
        ),
        exporters=ExporterConfig(
            prometheus_enabled=False,
            otlp_enabled=False,
        ),
    )
