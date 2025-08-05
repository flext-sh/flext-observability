"""Test flext_simple.py coverage for conditional paths."""

from decimal import Decimal

from flext_observability.flext_simple import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)


class TestSimpleCoverage:
    """Test flext_simple conditional paths for complete coverage."""

    def test_metric_type_inference_counter(self) -> None:
        """Test metric type inference for counter metrics."""
        # Test _total suffix
        result = flext_create_metric("requests_total", 100)
        assert result.success
        assert result.data.metric_type == "counter"

        # Test _count suffix
        result = flext_create_metric("errors_count", 5)
        assert result.success
        assert result.data.metric_type == "counter"

    def test_metric_type_inference_histogram(self) -> None:
        """Test metric type inference for histogram metrics."""
        # Test _duration suffix
        result = flext_create_metric("request_duration", 0.5)
        assert result.success
        assert result.data.metric_type == "histogram"

        # Test _time suffix
        result = flext_create_metric("response_time", 0.2)
        assert result.success
        assert result.data.metric_type == "histogram"

        # Test _seconds suffix
        result = flext_create_metric("processing_seconds", 1.5)
        assert result.success
        assert result.data.metric_type == "histogram"

        # Test "histogram" in name
        result = flext_create_metric("cpu_histogram_data", 85.0)
        assert result.success
        assert result.data.metric_type == "histogram"

    def test_metric_default_type_gauge(self) -> None:
        """Test default metric type (gauge)."""
        result = flext_create_metric("custom_metric", 42.0)
        assert result.success
        assert result.data.metric_type == "gauge"

    def test_metric_with_decimal_value(self) -> None:
        """Test metric creation with Decimal value."""
        result = flext_create_metric("precise_value", 123.456789)
        assert result.success
        assert isinstance(result.data.value, Decimal)
        assert result.data.value == Decimal("123.456789")

    def test_create_metric_validation_failure(self) -> None:
        """Test metric creation with validation failure."""
        result = flext_create_metric("", 42.0)  # Empty name
        assert result.is_failure
        assert "Invalid metric name" in result.error

    def test_create_log_entry_validation_failure(self) -> None:
        """Test log entry creation with validation failure."""
        result = flext_create_log_entry("", "info")  # Empty message
        assert result.is_failure
        assert "Invalid log message" in result.error

    def test_create_log_entry_invalid_level(self) -> None:
        """Test log entry creation with invalid level."""
        result = flext_create_log_entry("Test message", "invalid_level")
        assert result.is_failure
        assert "Invalid log level" in result.error

    def test_create_trace_validation_failure(self) -> None:
        """Test trace creation with validation failure."""
        result = flext_create_trace("", "test_operation")  # Empty trace_id
        assert result.is_failure
        assert "Invalid trace ID" in result.error

    def test_create_trace_invalid_operation(self) -> None:
        """Test trace creation with invalid operation."""
        result = flext_create_trace("trace_123", "")  # Empty operation
        assert result.is_failure
        assert "Invalid operation name" in result.error

    def test_create_alert_validation_failure(self) -> None:
        """Test alert creation with validation failure."""
        result = flext_create_alert("", "Test message")  # Empty title
        assert result.is_failure
        assert "Invalid alert title" in result.error

    def test_create_alert_invalid_message(self) -> None:
        """Test alert creation with invalid message."""
        result = flext_create_alert("Test Title", "")  # Empty message
        assert result.is_failure
        assert "Invalid alert message" in result.error

    def test_create_health_check_validation_failure(self) -> None:
        """Test health check creation with validation failure."""
        result = flext_create_health_check("")  # Empty component
        assert result.is_failure
        assert "Invalid component name" in result.error

    def test_create_health_check_invalid_status(self) -> None:
        """Test health check creation with invalid status."""
        result = flext_create_health_check("test_component", status="invalid_status")
        assert result.is_failure
        assert "Invalid health status" in result.error
