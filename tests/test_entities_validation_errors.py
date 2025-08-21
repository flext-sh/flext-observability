"""Test entity validation error paths for complete coverage."""

import pytest
from pydantic import ValidationError

from flext_observability import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)


class TestEntityValidationErrors:
    """Test entity validation error paths to improve coverage."""

    def test_metric_invalid_name_validation(self) -> None:
        """Test FlextMetric with invalid name (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextMetric(
                name="",  # Empty name should fail Pydantic validation
                value=42.0,
                unit="count",
            )

    def test_metric_invalid_value_validation(self) -> None:
        """Test FlextMetric with invalid value type."""
        metric = FlextMetric(
            name="test_metric",
            value=42.0,
            unit="count",
        )
        # Test business rule validation for negative values (bypass Pydantic validation)
        object.__setattr__(metric, "value", -10.0)
        result = metric.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Metric value cannot be negative" in result.error

    def test_log_entry_invalid_message_validation(self) -> None:
        """Test FlextLogEntry with invalid message (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextLogEntry(
                message="",  # Empty message should fail Pydantic validation
                service="test_service",
                level="INFO",
            )

    def test_log_entry_invalid_level_validation(self) -> None:
        """Test FlextLogEntry with invalid level."""
        log_entry = FlextLogEntry(
            message="Test message",
            service="test_service",
            level="INVALID_LEVEL",  # Invalid level for business rules
        )
        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid log level" in result.error

    def test_trace_invalid_trace_id_validation(self) -> None:
        """Test FlextTrace service_name validation (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextTrace(
                operation_name="test_operation",
                service_name="",  # Empty service_name should fail Pydantic validation
                trace_id="trace_123",
                span_id="span_123",
            )

    def test_trace_invalid_operation_validation(self) -> None:
        """Test FlextTrace with invalid operation (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextTrace(
                operation_name="",  # Empty operation should fail Pydantic validation
                service_name="test_service",
                trace_id="trace_123",
                span_id="span_123",
            )

    def test_alert_invalid_title_validation(self) -> None:
        """Test FlextAlert with invalid message (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextAlert(
                message="",  # Empty message should fail Pydantic validation
                service="test_service",
                level="info",
            )

    def test_alert_invalid_message_validation(self) -> None:
        """Test FlextAlert business rule validation."""
        alert = FlextAlert(
            message="Valid message",
            service="test_service",
            level="info",
        )
        # Test business rule validation for empty message after creation (bypass Pydantic validation)
        object.__setattr__(alert, "message", "")
        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Alert message cannot be empty" in result.error

    def test_alert_invalid_severity_validation(self) -> None:
        """Test FlextAlert with invalid level."""
        alert = FlextAlert(
            message="Test message",
            service="test_service",
            level="invalid_level",  # Invalid level for business rules
        )
        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert level" in result.error

    def test_health_check_invalid_component_validation(self) -> None:
        """Test FlextHealthCheck with invalid service_name (empty string)."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextHealthCheck(
                service_name="",  # Empty service_name should fail Pydantic validation
                status="healthy",
            )

    def test_health_check_invalid_status_validation(self) -> None:
        """Test FlextHealthCheck with invalid status."""
        health_check = FlextHealthCheck(
            service_name="test_component",
            status="invalid_status",  # Invalid status for business rules
        )
        result = health_check.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid health status" in result.error
