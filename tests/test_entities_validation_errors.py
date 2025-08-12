"""Test entity validation error paths for complete coverage."""

from flext_observability.observability_models import (
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
        metric = FlextMetric(
            id="test_id",
            name="",  # Empty name should fail validation
            value=42.0,
            unit="count",
        )
        result = metric.validate_business_rules()
        assert result.is_failure
        assert "Invalid metric name" in result.error

    def test_metric_invalid_value_validation(self) -> None:
        """Test FlextMetric with invalid value type."""
        metric = FlextMetric(
            id="test_id",
            name="test_metric",
            value=42.0,
            unit="count",
        )
        # Force invalid value type to test validation
        object.__setattr__(metric, "value", "not_a_number")
        result = metric.validate_business_rules()
        assert result.is_failure
        assert "Invalid metric value" in result.error

    def test_log_entry_invalid_message_validation(self) -> None:
        """Test FlextLogEntry with invalid message (empty string)."""
        log_entry = FlextLogEntry(
            id="test_id",
            message="",  # Empty message should fail validation
            level="info",
        )
        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert "Invalid log message" in result.error

    def test_log_entry_invalid_level_validation(self) -> None:
        """Test FlextLogEntry with invalid level."""
        log_entry = FlextLogEntry(
            id="test_id",
            message="Test message",
            level="invalid_level",  # Invalid level should fail validation
        )
        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert "Invalid log level" in result.error

    def test_trace_invalid_trace_id_validation(self) -> None:
        """Test FlextTrace with invalid trace_id (empty string)."""
        trace = FlextTrace(
            id="test_id",
            trace_id="",  # Empty trace_id should fail validation
            operation="test_operation",
            span_id="span_123",
        )
        result = trace.validate_business_rules()
        assert result.is_failure
        assert "Invalid trace ID" in result.error

    def test_trace_invalid_operation_validation(self) -> None:
        """Test FlextTrace with invalid operation (empty string)."""
        trace = FlextTrace(
            id="test_id",
            trace_id="trace_123",
            operation="",  # Empty operation should fail validation
            span_id="span_123",
        )
        result = trace.validate_business_rules()
        assert result.is_failure
        assert "Invalid operation name" in result.error

    def test_alert_invalid_title_validation(self) -> None:
        """Test FlextAlert with invalid title (empty string)."""
        alert = FlextAlert(
            id="test_id",
            title="",  # Empty title should fail validation
            message="Test message",
        )
        result = alert.validate_business_rules()
        assert result.is_failure
        assert "Invalid alert title" in result.error

    def test_alert_invalid_message_validation(self) -> None:
        """Test FlextAlert with invalid message (empty string)."""
        alert = FlextAlert(
            id="test_id",
            title="Test Alert",
            message="",  # Empty message should fail validation
        )
        result = alert.validate_business_rules()
        assert result.is_failure
        assert "Invalid alert message" in result.error

    def test_alert_invalid_severity_validation(self) -> None:
        """Test FlextAlert with invalid severity."""
        alert = FlextAlert(
            id="test_id",
            title="Test Alert",
            message="Test message",
            severity="invalid_severity",  # Invalid severity should fail validation
        )
        result = alert.validate_business_rules()
        assert result.is_failure
        assert "Invalid alert severity" in result.error

    def test_health_check_invalid_component_validation(self) -> None:
        """Test FlextHealthCheck with invalid component (empty string)."""
        health_check = FlextHealthCheck(
            id="test_id",
            component="",  # Empty component should fail validation
            status="healthy",
        )
        result = health_check.validate_business_rules()
        assert result.is_failure
        assert "Invalid component name" in result.error

    def test_health_check_invalid_status_validation(self) -> None:
        """Test FlextHealthCheck with invalid status."""
        health_check = FlextHealthCheck(
            id="test_id",
            component="test_component",
            status="invalid_status",  # Invalid status should fail validation
        )
        result = health_check.validate_business_rules()
        assert result.is_failure
        assert "Invalid health status" in result.error
