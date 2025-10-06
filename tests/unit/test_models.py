"""Unit tests for flext_observability.models module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityModels


class TestFlextObservabilityModels:
    """Test the unified FlextObservabilityModels class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityModels inherits from FlextModels."""
        from flext_core import FlextModels

        assert issubclass(FlextObservabilityModels, FlextModels)

    def test_metrics_namespace(self) -> None:
        """Test Metrics namespace is properly assigned."""
        from flext_observability.metrics import FlextObservabilityMetrics

        assert FlextObservabilityModels.Metrics == FlextObservabilityMetrics

    def test_tracing_namespace(self) -> None:
        """Test Tracing namespace is properly assigned."""
        from flext_observability.tracing import FlextObservabilityTracing

        assert FlextObservabilityModels.Tracing == FlextObservabilityTracing

    def test_alerting_namespace(self) -> None:
        """Test Alerting namespace is properly assigned."""
        from flext_observability.alerting import FlextObservabilityAlerting

        assert FlextObservabilityModels.Alerting == FlextObservabilityAlerting

    def test_health_namespace(self) -> None:
        """Test Health namespace is properly assigned."""
        from flext_observability.health import FlextObservabilityHealth

        assert FlextObservabilityModels.Health == FlextObservabilityHealth

    def test_logging_namespace(self) -> None:
        """Test Logging namespace is properly assigned."""
        from flext_observability.logging import FlextObservabilityLogging

        assert FlextObservabilityModels.Logging == FlextObservabilityLogging

    def test_backward_compatibility_aliases(self) -> None:
        """Test backward compatibility aliases are properly assigned."""
        assert (
            FlextObservabilityModels.FlextMetric
            == FlextObservabilityModels.Metrics.FlextMetric
        )
        assert (
            FlextObservabilityModels.FlextTrace
            == FlextObservabilityModels.Tracing.FlextTrace
        )
        assert (
            FlextObservabilityModels.FlextAlert
            == FlextObservabilityModels.Alerting.FlextAlert
        )
        assert (
            FlextObservabilityModels.FlextHealthCheck
            == FlextObservabilityModels.Health.FlextHealthCheck
        )
        assert (
            FlextObservabilityModels.FlextLogEntry
            == FlextObservabilityModels.Logging.FlextLogEntry
        )

    def test_factory_methods_exist(self) -> None:
        """Test factory methods are available."""
        assert hasattr(FlextObservabilityModels, "flext_metric")
        assert callable(FlextObservabilityModels.flext_metric)
