"""Unit tests for flext_observability.config module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityConfig


class TestFlextObservabilityConfig:
    """Test the FlextObservabilityConfig class."""

    def test_inherits_from_flext_config(self) -> None:
        """Test that FlextObservabilityConfig inherits from FlextConfig."""
        from flext_core import FlextConfig

        assert issubclass(FlextObservabilityConfig, FlextConfig)

    def test_configuration_attributes(self) -> None:
        """Test configuration attributes are properly defined."""
        # Test that key configuration attributes exist
        config_attrs = [
            "service_name",
            "environment",
            "debug_mode",
            "metrics_enabled",
            "tracing_enabled",
            "alerting_enabled",
            "health_check_enabled",
            "logging_enabled",
        ]
        for attr in config_attrs:
            assert hasattr(FlextObservabilityConfig, attr)

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = FlextObservabilityConfig()
        assert config.service_name == "flext-observability"
        assert config.environment == "development"
        assert config.debug_mode is False
        assert config.metrics_enabled is True
        assert config.tracing_enabled is True
        assert config.alerting_enabled is True
        assert config.health_check_enabled is True
        assert config.logging_enabled is True

    def test_validation_methods(self) -> None:
        """Test configuration validation methods exist."""
        validation_methods = [
            "validate_service_name",
            "validate_environment",
            "validate_endpoints",
            "validate_credentials",
        ]
        for method in validation_methods:
            assert hasattr(FlextObservabilityConfig, method)
            assert callable(getattr(FlextObservabilityConfig, method))

    def test_endpoint_configuration(self) -> None:
        """Test endpoint configuration attributes."""
        config = FlextObservabilityConfig()
        endpoint_attrs = [
            "prometheus_url",
            "grafana_url",
            "jaeger_url",
            "alertmanager_url",
        ]
        for attr in endpoint_attrs:
            assert hasattr(config, attr)

    def test_credential_configuration(self) -> None:
        """Test credential configuration attributes."""
        config = FlextObservabilityConfig()
        cred_attrs = [
            "prometheus_username",
            "prometheus_password",
            "grafana_username",
            "grafana_password",
        ]
        for attr in cred_attrs:
            assert hasattr(config, attr)
