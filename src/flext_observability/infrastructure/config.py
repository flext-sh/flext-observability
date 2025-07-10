"""Configuration for observability infrastructure.

REFACTORED: Uses flext-core BaseSettings with @singleton() decorator and DI.
Zero tolerance for duplication.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core.config import BaseSettings
from flext_core.config import get_container
from flext_core.config import singleton
from flext_core.domain.types import FlextConstants
from flext_core.domain.types import LogLevelLiteral
from flext_core.domain.types import ProjectName
from flext_core.domain.types import Version


@singleton()
class ObservabilitySettings(BaseSettings):
    """FLEXT Observability configuration settings with environment variable support.

    All settings can be overridden via environment variables with the
    prefix FLEXT_OBSERVABILITY_ (e.g., FLEXT_OBSERVABILITY_METRICS_PORT).

    Uses flext-core BaseSettings foundation with DI support.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_OBSERVABILITY_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    # Project identification using flext-core types
    project_name: ProjectName = Field("flext-observability", description="Project name")
    project_version: Version = Field(FlextConstants.FRAMEWORK_VERSION, description="Project version")

    # Metrics Configuration
    metrics_enabled: bool = Field(True, description="Enable metrics collection")
    metrics_port: int = Field(9090, description="Metrics endpoint port", ge=1024, le=65535)
    metrics_host: str = Field("0.0.0.0", description="Metrics endpoint host")
    metrics_path: str = Field("/metrics", description="Metrics endpoint path")
    metrics_interval: int = Field(15, description="Metrics collection interval (seconds)", ge=1, le=3600)
    metrics_retention_days: int = Field(30, description="Metrics retention period (days)", ge=1, le=365)

    # Tracing Configuration
    tracing_enabled: bool = Field(True, description="Enable distributed tracing")
    tracing_service_name: str = Field("flext-observability", description="Service name for tracing")
    tracing_service_version: str = Field(FlextConstants.FRAMEWORK_VERSION, description="Service version")
    tracing_environment: str = Field("production", description="Tracing environment")
    sampling_rate: float = Field(0.1, description="Trace sampling rate", ge=0.0, le=1.0)
    export_endpoint: str = Field("http://localhost:4317", description="OTLP export endpoint")
    export_timeout: int = Field(30, description="Export timeout (seconds)", ge=1, le=300)

    # Logging Configuration
    log_level: LogLevelLiteral = Field("INFO", description="Logging level")
    log_format: str = Field("json", description="Log output format")
    structured_logging: bool = Field(True, description="Use structured logging format")
    include_trace_info: bool = Field(True, description="Include trace information in logs")

    # Health Check Configuration
    health_enabled: bool = Field(True, description="Enable health checks")
    health_port: int = Field(8080, description="Health check port", ge=1024, le=65535)
    health_host: str = Field("0.0.0.0", description="Health check host")
    health_path: str = Field("/health", description="Health check endpoint path")
    health_interval: int = Field(30, description="Health check interval (seconds)", ge=10, le=3600)
    check_timeout: int = Field(5, description="Health check timeout (seconds)", ge=1, le=60)

    # Alerting Configuration
    alerting_enabled: bool = Field(False, description="Enable alerting")
    alert_cooldown_seconds: int = Field(300, description="Alert cooldown period (seconds)", ge=60, le=3600)
    webhook_enabled: bool = Field(False, description="Enable webhook notifications")
    webhook_url: str | None = Field(None, description="Webhook URL for notifications")
    webhook_timeout: int = Field(30, description="Webhook timeout (seconds)", ge=1, le=300)

    # Dashboard Configuration
    dashboard_enabled: bool = Field(True, description="Enable dashboard")
    dashboard_port: int = Field(8080, description="Dashboard port", ge=1024, le=65535)
    dashboard_host: str = Field("0.0.0.0", description="Dashboard host")
    dashboard_auto_refresh: bool = Field(True, description="Auto-refresh dashboard")
    dashboard_refresh_interval: int = Field(30, description="Dashboard refresh interval (seconds)", ge=5, le=300)

    # Performance thresholds
    cpu_threshold_percent: float = Field(80.0, description="CPU usage threshold (%)", ge=0.0, le=100.0)
    memory_threshold_percent: float = Field(80.0, description="Memory usage threshold (%)", ge=0.0, le=100.0)
    disk_threshold_percent: float = Field(80.0, description="Disk usage threshold (%)", ge=0.0, le=100.0)
    response_time_threshold_ms: int = Field(1000, description="Response time threshold (ms)", ge=1, le=60000)

    def configure_dependencies(self, container=None) -> None:
        """Configure dependencies using flext-core DI container."""
        if container is None:
            container = get_container()

        # Register this settings instance
        container.register(ObservabilitySettings, self)

        # Call parent configuration
        super().configure_dependencies(container)


# Cache for settings instance
_settings_instance: ObservabilitySettings | None = None


# Convenience function for getting settings
def get_observability_settings() -> ObservabilitySettings:
    """Get ObservabilitySettings instance with lazy initialization."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = ObservabilitySettings()
        container = get_container()
        _settings_instance.configure_dependencies(container)
    return _settings_instance


# Convenience export for backward compatibility
def get_settings() -> ObservabilitySettings:
    """Alias for get_observability_settings for backward compatibility."""
    return get_observability_settings()
