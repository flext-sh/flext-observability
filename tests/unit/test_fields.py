"""Unit tests for flext_observability.fields module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest



    FlextObservabilityFields,
)
from flext_observability.constants import FlextObservabilityConstants


class TestFlextObservabilityFields:
    """Test the unified FlextObservabilityFields class."""

    def test_metric_valid_units_constant(self) -> None:
        """Test METRIC_VALID_UNITS constant contains expected units."""
        expected_units = {
            "count",
            "percent",
            "bytes",
            "seconds",
            "milliseconds",
            "requests",
            "errors",
            "connections",
            "memory",
            "cpu",
        }
        assert expected_units == FlextObservabilityFields.METRIC_VALID_UNITS

    def test_alert_valid_levels_constant(self) -> None:
        """Test ALERT_VALID_LEVELS constant contains expected levels."""
        expected_levels = {
            FlextObservabilityConstants.ALERT_LEVEL_INFO,
            FlextObservabilityConstants.ALERT_LEVEL_WARNING,
            FlextObservabilityConstants.ALERT_LEVEL_ERROR,
            FlextObservabilityConstants.ALERT_LEVEL_CRITICAL,
        }
        assert expected_levels == FlextObservabilityFields.ALERT_VALID_LEVELS

    def test_trace_valid_statuses_constant(self) -> None:
        """Test TRACE_VALID_STATUSES constant contains expected statuses."""
        expected_statuses = {
            FlextObservabilityConstants.TRACE_STATUS_STARTED,
            FlextObservabilityConstants.TRACE_STATUS_RUNNING,
            FlextObservabilityConstants.TRACE_STATUS_COMPLETED,
            FlextObservabilityConstants.TRACE_STATUS_FAILED,
        }
        assert expected_statuses == FlextObservabilityFields.TRACE_VALID_STATUSES

    def test_health_valid_statuses_constant(self) -> None:
        """Test HEALTH_VALID_STATUSES constant contains expected statuses."""
        expected_statuses = {
            FlextObservabilityConstants.HEALTH_STATUS_HEALTHY,
            FlextObservabilityConstants.HEALTH_STATUS_DEGRADED,
            FlextObservabilityConstants.HEALTH_STATUS_UNHEALTHY,
        }
        assert expected_statuses == FlextObservabilityFields.HEALTH_VALID_STATUSES

    def test_create_metric_name_field(self) -> None:
        """Test create_metric_name_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_metric_name_field()
        assert field is not None
        # Field validation would require Pydantic model usage

    def test_create_metric_value_field(self) -> None:
        """Test create_metric_value_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_metric_value_field()
        assert field is not None

    def test_create_metric_unit_field(self) -> None:
        """Test create_metric_unit_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_metric_unit_field()
        assert field is not None

    def test_create_trace_name_field(self) -> None:
        """Test create_trace_name_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_trace_name_field()
        assert field is not None

    def test_create_alert_message_field(self) -> None:
        """Test create_alert_message_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_alert_message_field()
        assert field is not None

    def test_create_timestamp_field(self) -> None:
        """Test create_timestamp_field returns proper Field configuration."""
        field = FlextObservabilityFields.create_timestamp_field()
        assert field is not None


class TestMetricFields:
    """Test MetricFields nested class validation."""

    def test_validate_metric_value_positive(self) -> None:
        """Test metric value validation with positive values."""
        assert FlextObservabilityFields.MetricFields.validate_metric_value(42.0) == 42.0
        assert FlextObservabilityFields.MetricFields.validate_metric_value(0.0) == 0.0
        assert FlextObservabilityFields.MetricFields.validate_metric_value(100) == 100.0

    def test_validate_metric_value_negative_rejected(self) -> None:
        """Test metric value validation rejects negative values."""
        with pytest.raises(ValueError, match="Metric value cannot be negative"):
            FlextObservabilityFields.MetricFields.validate_metric_value(-1.0)
        with pytest.raises(ValueError, match="Metric value cannot be negative"):
            FlextObservabilityFields.MetricFields.validate_metric_value(-0.01)

    def test_validate_metric_unit_valid(self) -> None:
        """Test metric unit validation with valid units."""
        valid_units = ["count", "percent", "bytes", "seconds", "milliseconds"]
        for unit in valid_units:
            assert (
                FlextObservabilityFields.MetricFields.validate_metric_unit(unit) == unit
            )

    def test_validate_metric_unit_invalid_rejected(self) -> None:
        """Test metric unit validation rejects invalid units."""
        with pytest.raises(ValueError, match="Invalid metric unit"):
            FlextObservabilityFields.MetricFields.validate_metric_unit("invalid_unit")


class TestAlertFields:
    """Test AlertFields nested class validation."""

    def test_validate_alert_level_valid(self) -> None:
        """Test alert level validation with valid levels."""
        valid_levels = [
            FlextObservabilityConstants.ALERT_LEVEL_INFO,
            FlextObservabilityConstants.ALERT_LEVEL_WARNING,
            FlextObservabilityConstants.ALERT_LEVEL_ERROR,
            FlextObservabilityConstants.ALERT_LEVEL_CRITICAL,
        ]
        for level in valid_levels:
            assert (
                FlextObservabilityFields.AlertFields.validate_alert_level(level)
                == level
            )

    def test_validate_alert_level_invalid_rejected(self) -> None:
        """Test alert level validation rejects invalid levels."""
        with pytest.raises(ValueError, match="Invalid alert level"):
            FlextObservabilityFields.AlertFields.validate_alert_level("invalid_level")


class TestTraceFields:
    """Test TraceFields nested class validation."""

    def test_validate_trace_status_valid(self) -> None:
        """Test trace status validation with valid statuses."""
        valid_statuses = [
            FlextObservabilityConstants.TRACE_STATUS_STARTED,
            FlextObservabilityConstants.TRACE_STATUS_RUNNING,
            FlextObservabilityConstants.TRACE_STATUS_COMPLETED,
            FlextObservabilityConstants.TRACE_STATUS_FAILED,
        ]
        for status in valid_statuses:
            assert (
                FlextObservabilityFields.TraceFields.validate_trace_status(status)
                == status
            )

    def test_validate_trace_status_invalid_rejected(self) -> None:
        """Test trace status validation rejects invalid statuses."""
        with pytest.raises(ValueError, match="Invalid trace status"):
            FlextObservabilityFields.TraceFields.validate_trace_status("invalid_status")


class TestHealthFields:
    """Test HealthFields nested class validation."""

    def test_validate_health_status_valid(self) -> None:
        """Test health status validation with valid statuses."""
        valid_statuses = [
            FlextObservabilityConstants.HEALTH_STATUS_HEALTHY,
            FlextObservabilityConstants.HEALTH_STATUS_DEGRADED,
            FlextObservabilityConstants.HEALTH_STATUS_UNHEALTHY,
        ]
        for status in valid_statuses:
            assert (
                FlextObservabilityFields.HealthFields.validate_health_status(status)
                == status
            )

    def test_validate_health_status_invalid_rejected(self) -> None:
        """Test health status validation rejects invalid statuses."""
        with pytest.raises(ValueError, match="Invalid health status"):
            FlextObservabilityFields.HealthFields.validate_health_status(
                "invalid_status",
            )


# Removed backward compatibility and field instance tests
# as those symbols have been removed from the public API
