"""Configuration module for FLEXT Observability.

🚨 SIMPLE IMPORTS - Import directly from root:
✅ from flext_observability import configure_observability, ObservabilitySettings

This module provides configuration management for observability services
including OpenTelemetry, Prometheus metrics, and logging configuration.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings

# Issue deprecation warning for complex path access
warnings.warn(
    "🚨 DEPRECATED COMPLEX PATH: Importing from 'flext_observability.configuration' is deprecated.\n"
    "✅ SIMPLE SOLUTION: from flext_observability import configure_observability, ObservabilitySettings\n"
    "💡 ALL configuration functions are now available at root level for better productivity!\n"
    "📖 Complex paths will be removed in version 0.8.0.\n"
    "📚 Migration guide: https://docs.flext.dev/observability/simple-imports",
    DeprecationWarning,
    stacklevel=2,
)


class ObservabilitySettings(BaseSettings):
    """Settings for observability configuration."""

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json, plain)")
    log_file: str | None = Field(default=None, description="Log file path")

    # Metrics configuration
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    metrics_host: str = Field(default="0.0.0.0", description="Metrics server host")

    # Tracing configuration
    tracing_enabled: bool = Field(default=True, description="Enable distributed tracing")
    jaeger_endpoint: str = Field(default="http://localhost:14268/api/traces", description="Jaeger endpoint")
    trace_sample_rate: float = Field(default=1.0, description="Trace sampling rate")

    # Health monitoring
    health_enabled: bool = Field(default=True, description="Enable health monitoring")
    health_port: int = Field(default=8080, description="Health check port")

    # Service configuration
    service_name: str = Field(default="flext", description="Service name for observability")
    service_version: str = Field(default="0.7.0", description="Service version")
    environment: str = Field(default="development", description="Environment name")

    class Config:
        """Pydantic configuration."""

        env_prefix = "FLEXT_OBSERVABILITY_"
        case_sensitive = False


class DevelopmentConfig(ObservabilitySettings):
    """Development environment configuration."""

    log_level: str = "DEBUG"
    trace_sample_rate: float = 1.0
    environment: str = "development"


class ProductionConfig(ObservabilitySettings):
    """Production environment configuration."""

    log_level: str = "INFO"
    trace_sample_rate: float = 0.1
    environment: str = "production"
    log_format: str = "json"


class TestingConfig(ObservabilitySettings):
    """Testing environment configuration."""

    log_level: str = "WARNING"
    metrics_enabled: bool = False
    tracing_enabled: bool = False
    health_enabled: bool = False
    environment: str = "testing"


def configure_observability(
    settings: ObservabilitySettings | None = None,
    environment: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Configure observability for the application.

    Args:
        settings: Observability settings instance
        environment: Environment name (development, production, testing)
        **kwargs: Additional configuration options

    Returns:
        Configuration dictionary

    """
    if settings is None:
        if environment == "production":
            settings = ProductionConfig(**kwargs)
        elif environment == "testing":
            settings = TestingConfig(**kwargs)
        else:
            settings = DevelopmentConfig(**kwargs)

    return {
        "logging": {
            "level": settings.log_level,
            "format": settings.log_format,
            "file": settings.log_file,
        },
        "metrics": {
            "enabled": settings.metrics_enabled,
            "host": settings.metrics_host,
            "port": settings.metrics_port,
        },
        "tracing": {
            "enabled": settings.tracing_enabled,
            "jaeger_endpoint": settings.jaeger_endpoint,
            "sample_rate": settings.trace_sample_rate,
        },
        "health": {
            "enabled": settings.health_enabled,
            "port": settings.health_port,
        },
        "service": {
            "name": settings.service_name,
            "version": settings.service_version,
            "environment": settings.environment,
        },
    }


def create_development_config(**kwargs: Any) -> DevelopmentConfig:
    """Create development configuration.

    Args:
        **kwargs: Configuration overrides

    Returns:
        Development configuration instance

    """
    return DevelopmentConfig(**kwargs)


def create_production_config(**kwargs: Any) -> ProductionConfig:
    """Create production configuration.

    Args:
        **kwargs: Configuration overrides

    Returns:
        Production configuration instance

    """
    return ProductionConfig(**kwargs)


def create_testing_config(**kwargs: Any) -> TestingConfig:
    """Create testing configuration.

    Args:
        **kwargs: Configuration overrides

    Returns:
        Testing configuration instance

    """
    return TestingConfig(**kwargs)


def get_settings(environment: str | None = None) -> ObservabilitySettings:
    """Get observability settings for environment.

    Args:
        environment: Environment name

    Returns:
        Settings instance for the environment

    """
    if environment == "production":
        return ProductionConfig()
    if environment == "testing":
        return TestingConfig()
    return DevelopmentConfig()


__all__ = [
    "DevelopmentConfig",
    "ObservabilitySettings",
    "ProductionConfig",
    "TestingConfig",
    "configure_observability",
    "create_development_config",
    "create_production_config",
    "create_testing_config",
    "get_settings",
]
