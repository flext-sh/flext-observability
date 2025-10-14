"""Unit tests for flext_observability.models module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability import FlextObservabilityModels


class TestFlextObservabilityModels:
    """Test the unified FlextObservabilityModels class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityModels inherits from FlextCore.Models."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityModels, FlextCore.Models)

    def test_metrics_namespace(self) -> None:
        """Test Metrics namespace exists and is properly structured."""
        assert hasattr(FlextObservabilityModels, "Metrics")
        assert hasattr(FlextObservabilityModels.Metrics, "MetricEntry")

    def test_tracing_namespace(self) -> None:
        """Test Tracing namespace exists and is properly structured."""
        assert hasattr(FlextObservabilityModels, "Tracing")
        assert hasattr(FlextObservabilityModels.Tracing, "TraceEntry")

    def test_alerting_namespace(self) -> None:
        """Test Alerting namespace exists and is properly structured."""
        assert hasattr(FlextObservabilityModels, "Alerting")
        assert hasattr(FlextObservabilityModels.Alerting, "AlertEntry")

    def test_health_namespace(self) -> None:
        """Test Health namespace exists and is properly structured."""
        assert hasattr(FlextObservabilityModels, "Health")
        assert hasattr(FlextObservabilityModels.Health, "HealthCheckEntry")

    def test_logging_namespace(self) -> None:
        """Test Logging namespace exists and is properly structured."""
        assert hasattr(FlextObservabilityModels, "Logging")
        assert hasattr(FlextObservabilityModels.Logging, "LogEntry")

    def test_model_classes_exist(self) -> None:
        """Test that all main model classes exist as nested classes."""
        # Test that the main Entry classes exist
        assert hasattr(FlextObservabilityModels.Metrics, "MetricEntry")
        assert hasattr(FlextObservabilityModels.Tracing, "TraceEntry")
        assert hasattr(FlextObservabilityModels.Alerting, "AlertEntry")
        assert hasattr(FlextObservabilityModels.Health, "HealthCheckEntry")
        assert hasattr(FlextObservabilityModels.Logging, "LogEntry")

        # Test that config classes exist
        assert hasattr(FlextObservabilityModels.Metrics, "MetricConfig")
        assert hasattr(FlextObservabilityModels.Tracing, "TraceConfig")
        assert hasattr(FlextObservabilityModels.Alerting, "AlertConfig")
        assert hasattr(FlextObservabilityModels.Health, "HealthConfig")
        assert hasattr(FlextObservabilityModels.Logging, "LogConfig")

    def test_model_inheritance(self) -> None:
        """Test that model classes inherit from correct base classes."""
        from flext_core import FlextCore

        # Test that entry classes inherit from FlextCore.Models.Value
        assert issubclass(
            FlextObservabilityModels.Metrics.MetricEntry, FlextCore.Models.Value
        )
        assert issubclass(
            FlextObservabilityModels.Tracing.TraceEntry, FlextCore.Models.Value
        )
        assert issubclass(
            FlextObservabilityModels.Alerting.AlertEntry, FlextCore.Models.Value
        )
        assert issubclass(
            FlextObservabilityModels.Health.HealthCheckEntry, FlextCore.Models.Value
        )
        assert issubclass(
            FlextObservabilityModels.Logging.LogEntry, FlextCore.Models.Value
        )
