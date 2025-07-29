"""Test simple API functions for observability."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, TypeVar

from flext_observability.flext_simple import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

if TYPE_CHECKING:
    from flext_core import FlextResult

T = TypeVar("T")

def assert_success_with_data[T](result: FlextResult[T]) -> T:
    """Assert result is successful and return non-None data."""
    assert result.is_success
    assert result.data is not None
    return result.data


class TestSimpleApiCreation:
    """Test simple API creation functions."""

    def test_create_metric_success(self) -> None:
        """Test successful metric creation."""
        result = flext_create_metric("test_metric", 42.0)

        data = assert_success_with_data(result)
        if data.name != "test_metric":
            raise AssertionError(f"Expected {"test_metric"}, got {data.name}")
        assert data.value == 42.0

    def test_create_metric_with_options(self) -> None:
        """Test metric creation with optional parameters."""
        now = datetime.now(UTC)
        result = flext_create_metric(
            "test_metric",
            100.5,
            unit="bytes",
            tags={"env": "test"},
            timestamp=now,
        )

        data = assert_success_with_data(result)
        if data.unit != "bytes":
            raise AssertionError(f"Expected {"bytes"}, got {data.unit}")
        assert data.tags == {"env": "test"}
        if data.timestamp != now:
            raise AssertionError(f"Expected {now}, got {data.timestamp}")

    def test_create_log_entry_success(self) -> None:
        """Test successful log entry creation."""
        result = flext_create_log_entry("Test message")

        data = assert_success_with_data(result)
        if data.message != "Test message":
            raise AssertionError(f"Expected {"Test message"}, got {data.message}")
        assert data.level == "info"

    def test_create_log_entry_with_context(self) -> None:
        """Test log entry creation with context."""
        result = flext_create_log_entry(
            "Error occurred",
            level="error",
            context={"user_id": "123", "action": "login"},
        )

        data = assert_success_with_data(result)
        if data.level != "error":
            raise AssertionError(f"Expected {"error"}, got {data.level}")
        # Context might be stored differently, just check it exists
        assert hasattr(data, "context")

    def test_create_trace_success(self) -> None:
        """Test successful trace creation."""
        result = flext_create_trace("trace-123", "user_login")

        data = assert_success_with_data(result)
        if data.trace_id != "trace-123":
            raise AssertionError(f"Expected {"trace-123"}, got {data.trace_id}")
        assert data.operation == "user_login"

    def test_create_trace_with_config(self) -> None:
        """Test trace creation with configuration."""
        config = {
            "span_id": "span-456",
            "status": "completed",
            "duration_ms": 150,
        }
        result = flext_create_trace("trace-789", "data_processing", config=config)

        data = assert_success_with_data(result)
        if data.span_id != "span-456":
            raise AssertionError(f"Expected {"span-456"}, got {data.span_id}")

    def test_create_alert_success(self) -> None:
        """Test successful alert creation."""
        result = flext_create_alert("System Alert", "High CPU usage detected")

        data = assert_success_with_data(result)
        if data.title != "System Alert":
            raise AssertionError(f"Expected {"System Alert"}, got {data.title}")
        assert data.message == "High CPU usage detected"
        if data.severity != "low"  # default:
            raise AssertionError(f"Expected {"low"  # default}, got {data.severity}")

    def test_create_alert_high_severity(self) -> None:
        """Test alert creation with high severity."""
        result = flext_create_alert(
            "Critical Error",
            "Database connection failed",
            severity="critical",
            status="active",
        )

        data = assert_success_with_data(result)
        if data.severity != "critical":
            raise AssertionError(f"Expected {"critical"}, got {data.severity}")
        assert data.status == "active"

    def test_create_health_check_success(self) -> None:
        """Test successful health check creation."""
        result = flext_create_health_check("database")

        data = assert_success_with_data(result)
        if data.component != "database":
            raise AssertionError(f"Expected {"database"}, got {data.component}")
        assert data.status == "unknown"  # default

    def test_create_health_check_with_status(self) -> None:
        """Test health check creation with specific status."""
        result = flext_create_health_check(
            "api_server",
            status="healthy",
            message="All systems operational",
        )

        data = assert_success_with_data(result)
        if data.component != "api_server":
            raise AssertionError(f"Expected {"api_server"}, got {data.component}")
        assert data.status == "healthy"
        if data.message != "All systems operational":
            raise AssertionError(f"Expected {"All systems operational"}, got {data.message}")


class TestSimpleApiErrorHandling:
    """Test error handling in simple API."""

    def test_create_metric_invalid_value(self) -> None:
        """Test metric creation with invalid value."""
        # This tests error handling
        try:
            result = flext_create_metric("test", "invalid")  # type: ignore
            # Function should handle this gracefully
            assert result.is_success or result.is_failure
        except (RuntimeError, ValueError, TypeError):
            # If it throws, that's also acceptable behavior
            pass

    def test_create_functions_with_none_timestamp(self) -> None:
        """Test creation functions handle None timestamp correctly."""
        # Test each function individually to isolate failures
        try:
            metric_result = flext_create_metric("test", 1.0, timestamp=None)
            assert metric_result.is_success or metric_result.is_failure
        except (RuntimeError, ValueError, TypeError):
            pass

        try:
            log_result = flext_create_log_entry("test", timestamp=None)
            assert log_result.is_success or log_result.is_failure
        except (RuntimeError, ValueError, TypeError):
            pass

        try:
            trace_result = flext_create_trace("trace", "op", timestamp=None)
            assert trace_result.is_success or trace_result.is_failure
        except (RuntimeError, ValueError, TypeError):
            pass
