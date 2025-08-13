"""Test flext_monitor.py missing coverage lines to reach 95% target."""

from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_observability.observability_monitor import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)


class TestMonitorMissingCoverage:
    """Test specific missing lines in flext_monitor.py for complete coverage."""

    def test_get_health_status_failure_path(self) -> None:
        """Test flext_get_health_status when health service returns failure - covers line 274."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True
        monitor._health_service = Mock()

        # Mock health service to return failure
        monitor._health_service.get_overall_health.return_value = FlextResult.fail(
            "Health check failed",
        )

        result = monitor.flext_get_health_status()
        assert result.is_failure
        assert "Health check failed" in result.error

    def test_record_metric_no_metrics_service(self) -> None:
        """Test flext_record_metric when metrics service is not available - covers line 306."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = None

        result = monitor.flext_record_metric("test_metric", 42.0)
        assert result.is_failure
        assert "Metrics service not available" in result.error

    def test_record_metric_creation_failure(self) -> None:
        """Test flext_record_metric when metric creation fails - covers lines 313-315."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = Mock()

        # Mock flext_metric to return failure
        with patch("flext_observability.entities.flext_metric") as mock_metric:
            mock_metric.return_value = FlextResult.fail("Metric creation failed")

            result = monitor.flext_record_metric("test_metric", 42.0)
            assert result.is_failure
            assert "Metric creation failed" in result.error

    def test_record_metric_creation_returns_none(self) -> None:
        """Test flext_record_metric when metric creation returns None - covers line 318."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = Mock()

        # Mock flext_metric to return success but with None data
        with patch("flext_observability.entities.flext_metric") as mock_metric:
            mock_metric.return_value = FlextResult.ok(None)

            result = monitor.flext_record_metric("test_metric", 42.0)
            assert result.is_failure
            assert "Metric creation returned None" in result.error

    def test_record_metric_exception_handling(self) -> None:
        """Test flext_record_metric exception handling - covers lines 322-323."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = Mock()

        # Mock flext_metric to raise exception
        with patch("flext_observability.entities.flext_metric") as mock_metric:
            mock_metric.side_effect = ValueError("Test exception")

            result = monitor.flext_record_metric("test_metric", 42.0)
            assert result.is_failure
            assert "Failed to record metric: Test exception" in result.error

    def test_get_metrics_summary_no_service(self) -> None:
        """Test flext_get_metrics_summary when metrics service not available - covers lines 327-328."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = None

        result = monitor.flext_get_metrics_summary()
        assert result.is_failure
        assert "Metrics service not available" in result.error

    def test_get_metrics_summary_with_service(self) -> None:
        """Test flext_get_metrics_summary when service is available - covers line 330."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = Mock()

        # Mock service to return success
        expected_summary = {"total_metrics": 5, "last_update": "2025-01-01"}
        monitor._metrics_service.get_metrics_summary.return_value = FlextResult.ok(
            expected_summary,
        )

        result = monitor.flext_get_metrics_summary()
        assert result.success
        assert result.data == expected_summary

    def test_monitored_function_alert_creation_exception(self) -> None:
        """Test monitored function alert creation exception handling - covers lines 434-435."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True
        monitor._running = True
        monitor._alert_service = Mock()
        monitor._functions_monitored = 0

        # Create a function that will raise an exception
        @flext_monitor_function(monitor=monitor)
        def failing_function():
            msg = "Test exception"
            raise ValueError(msg)

        # Mock flext_alert to raise an exception during alert creation
        with patch("flext_observability.entities.flext_alert") as mock_alert:
            mock_alert.side_effect = AttributeError("Alert creation failed")

            # Function should still raise the original exception even if alert creation fails
            with pytest.raises(ValueError, match="Test exception"):
                failing_function()

            # Verify alert creation was attempted
            mock_alert.assert_called_once()

    def test_monitored_function_with_alert_service_exception_handling(self) -> None:
        """Test comprehensive exception handling in monitored function alert creation."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True
        monitor._running = True
        monitor._alert_service = Mock()
        monitor._functions_monitored = 0

        @flext_monitor_function(monitor=monitor)
        def failing_function():
            msg = "Original error"
            raise RuntimeError(msg)

        # Test ValueError in alert creation
        with patch("flext_observability.entities.flext_alert") as mock_alert:
            mock_alert.side_effect = ValueError("Alert value error")

            with pytest.raises(RuntimeError, match="Original error"):
                failing_function()

        # Test TypeError in alert creation
        with patch("flext_observability.entities.flext_alert") as mock_alert:
            mock_alert.side_effect = TypeError("Alert type error")

            with pytest.raises(RuntimeError, match="Original error"):
                failing_function()

        # Test AttributeError in alert creation
        with patch("flext_observability.entities.flext_alert") as mock_alert:
            mock_alert.side_effect = AttributeError("Alert attribute error")

            with pytest.raises(RuntimeError, match="Original error"):
                failing_function()

    def test_all_record_metric_exception_types(self) -> None:
        """Test all exception types in record_metric method."""
        monitor = FlextObservabilityMonitor()
        monitor._metrics_service = Mock()

        exception_types = [
            ValueError("Value error"),
            TypeError("Type error"),
            AttributeError("Attribute error"),
        ]

        for exception in exception_types:
            with patch("flext_observability.entities.flext_metric") as mock_metric:
                mock_metric.side_effect = exception

                result = monitor.flext_record_metric("test", 1.0)
                assert result.is_failure
                assert str(exception) in result.error
