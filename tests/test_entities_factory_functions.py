"""Test entity factory functions for complete coverage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from decimal import Decimal

import pytest

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
            "Test Title",  # message parameter
            "Test Message",  # service parameter
            level="error",  # level parameter (changed from severity)
            tags={"test": "value"},
        )
        assert str(alert.id) != ""  # ID is auto-generated
        assert alert.message == "Test Title"
        assert alert.service == "Test Message"
        assert alert.level == "error"

    def test_flext_alert_with_id_only(self) -> None:
        """Test flext_alert with only id provided."""
        alert = flext_alert(
            "Test Title",  # message parameter
            "Test Message",  # service parameter
            tags={"test": "value"},
        )
        assert str(alert.id) != ""  # ID is auto-generated
        assert alert.message == "Test Title"
        assert alert.service == "Test Message"

    def test_flext_alert_without_id(self) -> None:
        """Test flext_alert without id (auto-generated)."""
        alert = flext_alert(
            "Test Title",  # message parameter
            "Test Message",  # service parameter
            tags={"test": "value"},
        )
        assert alert.id is not None
        assert str(alert.id) != ""
        assert alert.message == "Test Title"
        assert alert.service == "Test Message"

    def test_flext_trace_with_id(self) -> None:
        """Test flext_trace with id provided."""
        trace = flext_trace(
            operation_name="test_operation",  # operation_name parameter
            service_name="trace_123",  # service_name parameter
            span_id="span_456",
            trace_id="trace_123",
            tags={"test": "value"},
        )
        assert str(trace.id) != ""  # ID is auto-generated
        assert trace.operation_name == "test_operation"
        assert trace.service_name == "trace_123"
        assert trace.span_id == "span_456"
        assert trace.trace_id == "trace_123"

    def test_flext_trace_without_id(self) -> None:
        """Test flext_trace without id (auto-generated)."""
        trace = flext_trace(
            operation_name="another_operation",  # operation_name parameter
            service_name="trace_789",  # service_name parameter
            span_id="span_012",
            tags={"test": "value"},
        )
        assert trace.id is not None
        assert str(trace.id) != ""
        assert trace.operation_name == "another_operation"
        assert trace.service_name == "trace_789"

    def test_flext_metric_with_id_and_version(self) -> None:
        """Test flext_metric with both id and version provided."""
        metric = flext_metric(
            "test_metric",
            42.5,
            unit="seconds",
            tags={"env": "test"},
        )
        # Factory function returns entity directly with auto-generated ID
        assert str(metric.id) != ""
        assert metric.version == 1  # Default version
        assert metric.name == "test_metric"
        assert metric.value == 42.5

    def test_flext_metric_with_id_only(self) -> None:
        """Test flext_metric with only id provided."""
        metric = flext_metric(
            "test_metric",
            100.0,
            tags={"test": "value"},
        )
        # Factory function returns entity directly with auto-generated ID
        assert str(metric.id) != ""
        assert metric.version == 1

    def test_flext_metric_without_id(self) -> None:
        """Test flext_metric without id (auto-generated)."""
        metric = flext_metric(
            "auto_metric",
            75.0,
            unit="percent",
            tags={"auto": "generated"},
        )
        assert metric.id is not None
        assert str(metric.id) != ""

    def test_flext_metric_with_decimal_value(self) -> None:
        """Test flext_metric with Decimal value."""
        metric = flext_metric(
            "decimal_metric",
            Decimal("123.456"),
            unit="currency",
        )
        # Factory function returns entity directly
        assert isinstance(metric.value, Decimal)
        assert metric.value == Decimal("123.456")

    def test_flext_metric_creation_error(self) -> None:
        """Test flext_metric error handling."""
        # Test that Pydantic validation catches empty name
        with pytest.raises(Exception, match="String should have at least 1 character"):
            flext_metric(
                "",  # Empty name should cause validation error
                42.0,
            )

    def test_flext_health_check_with_id(self) -> None:
        """Test flext_health_check with id provided."""
        health = flext_health_check(
            service_name="test_component",  # service_name parameter
            status="healthy",
            details={"cpu": 50.0},  # details instead of metrics
        )
        assert str(health.id) != ""  # ID is auto-generated
        assert health.service_name == "test_component"
        assert health.status == "healthy"

    def test_flext_health_check_without_id(self) -> None:
        """Test flext_health_check without id (auto-generated)."""
        health = flext_health_check(
            service_name="auto_component",  # service_name parameter
            details={"memory": 75.0},  # details instead of metrics
        )
        assert health.id is not None
        assert str(health.id) != ""
        assert health.service_name == "auto_component"

    def test_flext_metric_validation_edge_cases(self) -> None:
        """Test flext_metric validation with edge cases - real validation testing."""
        # Test with extreme values - real boundary testing
        large_metric = flext_metric("large_value_metric", float("1e10"))
        assert large_metric.value == 1e10
        assert large_metric.name == "large_value_metric"

        # Test with very small positive values
        small_metric = flext_metric("small_value_metric", float("1e-10"))
        assert small_metric.value == 1e-10
        assert small_metric.name == "small_value_metric"

        # Test with zero value - boundary condition
        zero_metric = flext_metric("zero_metric", 0.0)
        assert zero_metric.value == 0.0
        assert zero_metric.name == "zero_metric"

        # Test that negative values are rejected - real business rule validation
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            flext_metric("negative_metric", -42.5)
