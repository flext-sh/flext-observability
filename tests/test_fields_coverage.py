"""Test coverage for fields module validation logic."""

import pytest

import flext_observability.fields as fields_module
from flext_observability.fields import (
    AlertLevelField,
    HealthStatusField,
    MetricUnitField,
    MetricValueField,
    TraceStatusField,
    alert_message_field,
    metric_name_field,
    metric_unit_field,
    metric_value_field,
    timestamp_field,
    trace_name_field,
)


class TestFieldValidators:
    """Test coverage for Pydantic field validators."""

    def test_metric_value_field_positive_values(self) -> None:
        """Test MetricValueField validation with positive values."""
        # Test valid positive values
        assert MetricValueField.validate_metric_value(42.0) == 42.0
        assert MetricValueField.validate_metric_value(0.0) == 0.0
        assert (
            MetricValueField.validate_metric_value(100) == 100.0
        )  # int to float conversion

    def test_metric_value_field_negative_validation(self) -> None:
        """Test MetricValueField validation rejects negative values."""
        with pytest.raises(ValueError, match="Metric value cannot be negative"):
            MetricValueField.validate_metric_value(-1.0)

        with pytest.raises(ValueError, match="Metric value cannot be negative"):
            MetricValueField.validate_metric_value(-0.01)

    def test_metric_unit_field_valid_units(self) -> None:
        """Test MetricUnitField validation with valid units."""
        valid_units = [
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
        ]

        for unit in valid_units:
            assert MetricUnitField.validate_metric_unit(unit) == unit

    def test_metric_unit_field_invalid_units(self) -> None:
        """Test MetricUnitField validation rejects invalid units."""
        invalid_units = ["invalid_unit", "pixels", "kilograms", ""]

        for unit in invalid_units:
            with pytest.raises(ValueError, match="Invalid metric unit"):
                MetricUnitField.validate_metric_unit(unit)

    def test_alert_level_field_valid_levels(self) -> None:
        """Test AlertLevelField validation with valid levels."""
        valid_levels = ["info", "warning", "error", "critical"]

        for level in valid_levels:
            assert AlertLevelField.validate_alert_level(level) == level

    def test_alert_level_field_invalid_levels(self) -> None:
        """Test AlertLevelField validation rejects invalid levels."""
        invalid_levels = ["debug", "fatal", "notice", ""]

        for level in invalid_levels:
            with pytest.raises(ValueError, match="Invalid alert level"):
                AlertLevelField.validate_alert_level(level)

    def test_trace_status_field_valid_statuses(self) -> None:
        """Test TraceStatusField validation with valid statuses."""
        valid_statuses = ["started", "running", "completed", "failed"]

        for status in valid_statuses:
            assert TraceStatusField.validate_trace_status(status) == status

    def test_trace_status_field_invalid_statuses(self) -> None:
        """Test TraceStatusField validation rejects invalid statuses."""
        invalid_statuses = ["pending", "cancelled", "unknown", ""]

        for status in invalid_statuses:
            with pytest.raises(ValueError, match="Invalid trace status"):
                TraceStatusField.validate_trace_status(status)

    def test_health_status_field_valid_statuses(self) -> None:
        """Test HealthStatusField validation with valid statuses."""
        valid_statuses = ["healthy", "degraded", "unhealthy"]

        for status in valid_statuses:
            assert HealthStatusField.validate_health_status(status) == status

    def test_health_status_field_invalid_statuses(self) -> None:
        """Test HealthStatusField validation rejects invalid statuses."""
        invalid_statuses = ["ok", "down", "maintenance", ""]

        for status in invalid_statuses:
            with pytest.raises(ValueError, match="Invalid health status"):
                HealthStatusField.validate_health_status(status)


class TestConvenienceFields:
    """Test coverage for convenience field definitions."""

    def test_metric_name_field_definition(self) -> None:
        """Test metric_name_field has correct configuration."""
        field = metric_name_field
        assert hasattr(field, "description")
        assert field.description == "Metric name"
        # Check field has metadata constraints
        assert hasattr(field, "metadata")
        assert len(field.metadata) > 0

    def test_metric_value_field_definition(self) -> None:
        """Test metric_value_field has correct configuration."""
        field = metric_value_field
        assert hasattr(field, "description")
        assert field.description == "Metric value (non-negative)"
        # Check field has metadata constraints
        assert hasattr(field, "metadata")
        assert len(field.metadata) > 0

    def test_metric_unit_field_definition(self) -> None:
        """Test metric_unit_field has correct configuration."""
        field = metric_unit_field
        assert hasattr(field, "description")
        assert field.description == "Metric unit"

    def test_trace_name_field_definition(self) -> None:
        """Test trace_name_field has correct configuration."""
        field = trace_name_field
        assert hasattr(field, "description")
        assert field.description == "Trace operation name"
        # Check field has metadata constraints
        assert hasattr(field, "metadata")
        assert len(field.metadata) > 0

    def test_alert_message_field_definition(self) -> None:
        """Test alert_message_field has correct configuration."""
        field = alert_message_field
        assert hasattr(field, "description")
        assert field.description == "Alert message"
        # Check field has metadata constraints
        assert hasattr(field, "metadata")
        assert len(field.metadata) > 0

    def test_timestamp_field_definition(self) -> None:
        """Test timestamp_field has correct configuration."""
        field = timestamp_field
        assert hasattr(field, "description")
        assert field.description == "Timestamp"
        assert hasattr(field, "default_factory")

    def test_all_convenience_fields_available(self) -> None:
        """Test all convenience fields are properly defined."""
        # Test that all exports from __all__ exist and are not None
        for export_name in fields_module.__all__:
            assert hasattr(fields_module, export_name), f"Missing export: {export_name}"
            exported_item = getattr(fields_module, export_name)
            assert exported_item is not None, f"Null export: {export_name}"


class TestFieldValidatorClassProperties:
    """Test coverage for field validator class properties."""

    def test_metric_unit_field_valid_units_property(self) -> None:
        """Test MetricUnitField.valid_units contains expected units."""
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

        assert MetricUnitField.valid_units == expected_units
        assert len(MetricUnitField.valid_units) == 10

    def test_all_field_classes_have_validators(self) -> None:
        """Test all field classes have the expected validator methods."""
        # Test MetricValueField
        assert hasattr(MetricValueField, "validate_metric_value")
        assert callable(MetricValueField.validate_metric_value)

        # Test MetricUnitField
        assert hasattr(MetricUnitField, "validate_metric_unit")
        assert callable(MetricUnitField.validate_metric_unit)

        # Test AlertLevelField
        assert hasattr(AlertLevelField, "validate_alert_level")
        assert callable(AlertLevelField.validate_alert_level)

        # Test TraceStatusField
        assert hasattr(TraceStatusField, "validate_trace_status")
        assert callable(TraceStatusField.validate_trace_status)

        # Test HealthStatusField
        assert hasattr(HealthStatusField, "validate_health_status")
        assert callable(HealthStatusField.validate_health_status)
