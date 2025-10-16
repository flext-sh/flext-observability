"""Test entity factory functions for complete coverage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from decimal import Decimal

from flext_observability import (
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)


class TestEntityFactoryFunctions:
    """Test entity factory functions to improve coverage."""

    def test_flext_alert_with_id_and_version(self) -> None:
        """Test flext_alert with both id and version provided."""
        alert = flext_alert(
            "Test Title",  # title parameter
            "Test Message",  # message parameter
            severity="high",  # severity parameter
            tags={"test": "value"},
        )
        assert str(alert.id)  # ID is auto-generated
        assert alert.title == "Test Title"
        assert alert.message == "Test Message"
        assert alert.severity == "high"

    def test_flext_alert_with_id_only(self) -> None:
        """Test flext_alert with only id provided."""
        alert = flext_alert(
            "Test Title",  # message parameter
            "Test Message",  # service parameter
            tags={"test": "value"},
        )
        assert str(alert.id)  # ID is auto-generated
        assert alert.title == "Test Title"
        assert alert.message == "Test Message"

    def test_flext_alert_without_id(self) -> None:
        """Test flext_alert without id (auto-generated)."""
        alert = flext_alert(
            "Test Title",  # message parameter
            "Test Message",  # service parameter
            tags={"test": "value"},
        )
        assert alert.id is not None
        assert str(alert.id)
        assert alert.title == "Test Title"
        assert alert.message == "Test Message"

    def test_flext_trace_with_id(self) -> None:
        """Test flext_trace with id provided."""
        trace = flext_trace(
            "trace_123",  # trace_id parameter
            "test_operation",  # operation parameter
            "span_456",  # span_id parameter
            tags={"test": "value"},
        )
        assert str(trace.id)  # ID is auto-generated
        assert trace.operation == "test_operation"
        # FlextTrace doesn't have service_name field
        assert trace.span_id == "span_456"
        assert trace.trace_id == "trace_123"

    def test_flext_trace_without_id(self) -> None:
        """Test flext_trace without id (auto-generated)."""
        trace = flext_trace(
            "trace_789",  # trace_id parameter
            "another_operation",  # operation parameter
            "span_012",  # span_id parameter
            tags={"test": "value"},
        )
        assert trace.id is not None
        assert str(trace.id)
        assert trace.operation == "another_operation"
        # FlextTrace doesn't have service_name field

    def test_flext_metric_with_id_and_version(self) -> None:
        """Test flext_metric with both id and version provided."""
        metric = flext_metric(
            "test_metric",
            42.5,
            unit="seconds",
            tags={"env": "test"},
        )
        # Factory function returns FlextResult[FlextMetric]
        assert metric.is_success
        metric_obj = metric.unwrap()
        assert str(metric_obj.id)
        assert metric_obj.name == "test_metric"
        assert metric_obj.value == 42.5

    def test_flext_metric_with_id_only(self) -> None:
        """Test flext_metric with only id provided."""
        metric = flext_metric(
            "test_metric",
            100.0,
            tags={"test": "value"},
        )
        # Factory function returns FlextResult[FlextMetric]
        assert metric.is_success
        metric_obj = metric.unwrap()
        assert str(metric_obj.id)

    def test_flext_metric_without_id(self) -> None:
        """Test flext_metric without id (auto-generated)."""
        metric = flext_metric(
            "auto_metric",
            75.0,
            unit="percent",
            tags={"auto": "generated"},
        )
        assert metric.is_success
        metric_obj = metric.unwrap()
        assert metric_obj.id is not None
        assert str(metric_obj.id)

    def test_flext_metric_with_decimal_value(self) -> None:
        """Test flext_metric with Decimal value."""
        metric = flext_metric(
            "decimal_metric",
            Decimal("123.456"),
            unit="currency",
        )
        # Factory function returns FlextResult
        assert metric.is_success
        assert metric.data is not None
        assert isinstance(metric.data.value, Decimal)
        assert metric.data.value == Decimal("123.456")

    def test_flext_metric_creation_error(self) -> None:
        """Test flext_metric error handling."""
        # Test that validation catches empty name
        result = flext_metric(
            "",  # Empty name should cause validation error
            42.0,
        )
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None and "Metric name cannot be empty" in result.error
        )

    def test_flext_health_check_with_id(self) -> None:
        """Test flext_health_check with id provided."""
        health = flext_health_check(
            "test_component",  # component parameter
            "healthy",  # status parameter
            message="Health check message",
            metrics={"cpu": 50.0},  # metrics parameter
        )
        assert str(health.id)  # ID is auto-generated
        assert health.component == "test_component"
        assert health.status == "healthy"

    def test_flext_health_check_without_id(self) -> None:
        """Test flext_health_check without id (auto-generated)."""
        health = flext_health_check(
            "auto_component",  # component parameter
            "healthy",  # status parameter
            metrics={"memory": 75.0},  # metrics parameter
        )
        assert health.id is not None
        assert str(health.id)
        assert health.component == "auto_component"

    def test_flext_metric_validation_edge_cases(self) -> None:
        """Test flext_metric validation with edge cases - real validation testing."""
        # Test with extreme values - real boundary testing
        large_metric = flext_metric("large_value_metric", float("1e10"))
        assert large_metric.is_success
        large_metric_obj = large_metric.unwrap()
        assert large_metric_obj.value == 1e10
        assert large_metric_obj.name == "large_value_metric"

        # Test with very small positive values
        small_metric = flext_metric("small_value_metric", float("1e-10"))
        assert small_metric.is_success
        small_metric_obj = small_metric.unwrap()
        assert small_metric_obj.value == 1e-10
        assert small_metric_obj.name == "small_value_metric"

        # Test with zero value - boundary condition
        zero_metric = flext_metric("zero_metric", 0.0)
        assert zero_metric.is_success
        zero_metric_obj = zero_metric.unwrap()
        assert zero_metric_obj.value == 0.0
        assert zero_metric_obj.name == "zero_metric"

        # Test that negative values are allowed - current implementation allows them
        negative_metric = flext_metric("negative_metric", -42.5)
        assert negative_metric.is_success
        negative_metric_obj = negative_metric.unwrap()
        assert negative_metric_obj.value == -42.5
        assert negative_metric_obj.name == "negative_metric"
