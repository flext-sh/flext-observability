"""Test observability entities via simple API."""

from __future__ import annotations

from flext_observability import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)


class TestEntityValidation:
    """Test entity validation via simple API results."""

    def test_metric_validation(self) -> None:
        """Test metric validation through created entities."""
        # Valid metric
        result = flext_create_metric("valid_metric", 42.0)
        assert result.success
        assert result.data is not None
        validation_result = result.data.validate_business_rules()
        assert validation_result.success

    def test_log_entry_validation(self) -> None:
        """Test log entry validation."""
        result = flext_create_log_entry("Test message", "info")
        assert result.success
        assert result.data is not None
        validation_result = result.data.validate_business_rules()
        assert validation_result.success

    def test_trace_validation(self) -> None:
        """Test trace validation."""
        result = flext_create_trace("trace-123", "test_operation")
        assert result.success
        assert result.data is not None
        validation_result = result.data.validate_business_rules()
        assert validation_result.success

    def test_alert_validation(self) -> None:
        """Test alert validation."""
        result = flext_create_alert("Test Alert", "Test message")
        assert result.success
        assert result.data is not None
        validation_result = result.data.validate_business_rules()
        assert validation_result.success

    def test_health_check_validation(self) -> None:
        """Test health check validation."""
        result = flext_create_health_check("test_component")
        assert result.success
        assert result.data is not None
        validation_result = result.data.validate_business_rules()
        assert validation_result.success
