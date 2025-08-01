"""Simple test for flext_observability.exceptions module - achieve 100% coverage.

Tests all exception classes with their actual signatures and messages.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_observability.exceptions import (
    FlextObservabilityConfigurationError,
    FlextObservabilityConnectionError,
    FlextObservabilityError,
    FlextObservabilityHealthError,
    FlextObservabilityLoggingError,
    FlextObservabilityMetricsError,
    FlextObservabilityProcessingError,
    FlextObservabilityTimeoutError,
    FlextObservabilityTracingError,
    FlextObservabilityValidationError,
)


def test_flext_observability_error() -> None:
    """Test FlextObservabilityError class."""
    # Default
    error = FlextObservabilityError()
    assert error.message == "Observability error"

    # Custom message
    error = FlextObservabilityError("Custom error")
    assert error.message == "Custom error"

    # With component
    error = FlextObservabilityError("Error", component="metrics")
    assert error.message == "Error"

    # With kwargs
    error = FlextObservabilityError("Error", component="test", extra="value")
    assert error.message == "Error"


def test_flext_observability_configuration_error() -> None:
    """Test FlextObservabilityConfigurationError class."""
    # Default
    error = FlextObservabilityConfigurationError()
    assert "Observability configuration error" in error.message

    # Custom message
    error = FlextObservabilityConfigurationError("Custom config error")
    assert "Custom config error" in error.message

    # With config_key
    error = FlextObservabilityConfigurationError(
        "Config error", config_key="prometheus.endpoint"
    )
    assert "Config error" in error.message

    # With component and config_key
    error = FlextObservabilityConfigurationError(
        "Config error", config_key="timeout", component="metrics"
    )
    assert "Config error" in error.message


def test_flext_observability_connection_error() -> None:
    """Test FlextObservabilityConnectionError class."""
    # Default
    error = FlextObservabilityConnectionError()
    assert "Observability connection failed" in error.message

    # Custom message
    error = FlextObservabilityConnectionError("Connection failed")
    assert "Connection failed" in error.message

    # With endpoint
    error = FlextObservabilityConnectionError(
        "Failed", endpoint="http://localhost:9090"
    )
    assert "Failed" in error.message

    # With service_name
    error = FlextObservabilityConnectionError("Failed", service_name="prometheus")
    assert "Failed" in error.message


def test_flext_observability_processing_error() -> None:
    """Test FlextObservabilityProcessingError class."""
    # Default
    error = FlextObservabilityProcessingError()
    assert "Observability processing failed" in error.message

    # Custom message
    error = FlextObservabilityProcessingError("Processing failed")
    assert "Processing failed" in error.message

    # With operation
    error = FlextObservabilityProcessingError("Failed", operation="collect_metrics")
    assert "Failed" in error.message

    # With metric_name
    error = FlextObservabilityProcessingError("Failed", metric_name="cpu_usage")
    assert "Failed" in error.message


def test_flext_observability_timeout_error() -> None:
    """Test FlextObservabilityTimeoutError class."""
    # Default
    error = FlextObservabilityTimeoutError()
    assert "Observability operation timed out" in error.message

    # Custom message
    error = FlextObservabilityTimeoutError("Timeout occurred")
    assert "Timeout occurred" in error.message

    # With operation
    error = FlextObservabilityTimeoutError("Timeout", operation="query")
    assert "Timeout" in error.message

    # With timeout_seconds
    error = FlextObservabilityTimeoutError("Timeout", timeout_seconds=30.0)
    assert "Timeout" in error.message


def test_flext_observability_validation_error() -> None:
    """Test FlextObservabilityValidationError class."""
    # Default
    error = FlextObservabilityValidationError()
    assert "Observability validation failed" in error.message

    # Custom message
    error = FlextObservabilityValidationError("Validation failed")
    assert "Validation failed" in error.message

    # With field
    error = FlextObservabilityValidationError("Invalid", field="cpu_usage")
    assert "Invalid" in error.message

    # With value
    error = FlextObservabilityValidationError("Invalid", value=150.5)
    assert "Invalid" in error.message

    # With metric_name
    error = FlextObservabilityValidationError("Invalid", metric_name="memory_percent")
    assert "Invalid" in error.message


def test_flext_observability_metrics_error() -> None:
    """Test FlextObservabilityMetricsError class."""
    # Default
    error = FlextObservabilityMetricsError()
    assert "Observability metrics error" in error.message

    # Custom message
    error = FlextObservabilityMetricsError("Metrics failed")
    assert "Metrics failed" in error.message

    # With metric_type
    error = FlextObservabilityMetricsError("Failed", metric_type="counter")
    assert "Failed" in error.message


def test_flext_observability_tracing_error() -> None:
    """Test FlextObservabilityTracingError class."""
    # Default
    error = FlextObservabilityTracingError()
    assert "Observability tracing error" in error.message

    # Custom message
    error = FlextObservabilityTracingError("Tracing failed")
    assert "Tracing failed" in error.message

    # With trace_id
    error = FlextObservabilityTracingError("Failed", trace_id="abc123")
    assert "Failed" in error.message

    # With span_name
    error = FlextObservabilityTracingError("Failed", span_name="process_data")
    assert "Failed" in error.message


def test_flext_observability_logging_error() -> None:
    """Test FlextObservabilityLoggingError class."""
    # Default
    error = FlextObservabilityLoggingError()
    assert "Observability logging error" in error.message

    # Custom message
    error = FlextObservabilityLoggingError("Logging failed")
    assert "Logging failed" in error.message

    # With logger_name
    error = FlextObservabilityLoggingError("Failed", logger_name="flext.metrics")
    assert "Failed" in error.message

    # With log_level
    error = FlextObservabilityLoggingError("Failed", log_level="DEBUG")
    assert "Failed" in error.message


def test_flext_observability_health_error() -> None:
    """Test FlextObservabilityHealthError class."""
    # Default
    error = FlextObservabilityHealthError()
    assert "Observability health check failed" in error.message

    # Custom message
    error = FlextObservabilityHealthError("Health check failed")
    assert "Health check failed" in error.message

    # With check_name
    error = FlextObservabilityHealthError("Failed", check_name="liveness")
    assert "Failed" in error.message

    # With service_name
    error = FlextObservabilityHealthError("Failed", service_name="prometheus")
    assert "Failed" in error.message


def test_all_exceptions_can_be_raised() -> None:
    """Test all exceptions can be raised and caught."""
    exceptions = [
        FlextObservabilityError,
        FlextObservabilityConfigurationError,
        FlextObservabilityConnectionError,
        FlextObservabilityProcessingError,
        FlextObservabilityTimeoutError,
        FlextObservabilityValidationError,
        FlextObservabilityMetricsError,
        FlextObservabilityTracingError,
        FlextObservabilityLoggingError,
        FlextObservabilityHealthError,
    ]

    for exception_class in exceptions:
        exception_message = "Test exception"
        with pytest.raises(exception_class):
            raise exception_class(exception_message)


def test_inheritance_hierarchy() -> None:
    """Test exception inheritance hierarchy."""
    # Test that all exceptions inherit from Exception
    error = FlextObservabilityError()
    assert isinstance(error, Exception)

    # Test specific inheritance (some inherit from flext-core exceptions)
    config_error = FlextObservabilityConfigurationError()
    assert isinstance(config_error, Exception)

    connection_error = FlextObservabilityConnectionError()
    assert isinstance(connection_error, Exception)

    # Test observability-specific exceptions inherit from FlextObservabilityError
    metrics_error = FlextObservabilityMetricsError()
    assert isinstance(metrics_error, FlextObservabilityError)
    assert isinstance(metrics_error, Exception)

    health_error = FlextObservabilityHealthError()
    assert isinstance(health_error, FlextObservabilityError)
    assert isinstance(health_error, Exception)
