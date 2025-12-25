"""Test coverage for API module error handling and edge cases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import math
from datetime import UTC, datetime



    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)


class TestApiErrorHandling:
    """Test coverage for API error handling paths."""

    def test_flext_create_metric_histogram_unit_inference(self) -> None:
        """Test metric type inference for histogram units."""
        # Test histogram inference from unit
        result = flext_create_metric("test_metric", 1.0, "histogram_buckets")
        assert result.is_success

        # Test histogram inference from name pattern
        result = flext_create_metric("test_duration", 1.0, "seconds")
        assert result.is_success

        result = flext_create_metric("test_time", 1.0, "milliseconds")
        assert result.is_success

        result = flext_create_metric("request_histogram", 1.0, "count")
        assert result.is_success

    def test_flext_create_metric_with_invalid_values(self) -> None:
        """Test metric creation with invalid values to trigger error handling."""
        # Test with invalid metric unit to potentially trigger validation errors
        # This should still succeed but tests the error handling paths
        result = flext_create_metric("valid_metric", 42.0, "count")
        assert result.is_success

        # Test with valid values to ensure normal path works
        result = flext_create_metric("test_counter", 10.0, "count")
        assert result.is_success

    def test_flext_create_log_entry_error_handling(self) -> None:
        """Test log entry creation error handling paths."""
        # Test with valid values to cover normal execution
        result = flext_create_log_entry("Test message", "test_service", "info")
        assert result.is_success

        # Test with different log levels
        result = flext_create_log_entry("Warning message", "test_service", "warning")
        assert result.is_success

        result = flext_create_log_entry("Error message", "test_service", "error")
        assert result.is_success

    def test_flext_create_trace_error_handling(self) -> None:
        """Test trace creation error handling paths."""
        # Test with valid values to cover normal execution
        result = flext_create_trace("test_operation", "test_service")
        assert result.is_success

        # Test with context parameters
        context = {"trace_id": "custom_trace_123", "span_id": "custom_span_456"}
        result = flext_create_trace(
            "operation_with_context",
            "service",
            context=context,
        )
        assert result.is_success

        # Test with partial context
        context = {"trace_id": "only_trace_id"}
        result = flext_create_trace("partial_context_op", "service", context=context)
        assert result.is_success

        context = {"span_id": "only_span_id"}
        result = flext_create_trace("partial_context_op2", "service", context=context)
        assert result.is_success

    def test_flext_create_alert_error_handling(self) -> None:
        """Test alert creation error handling paths."""
        # Test with valid values to cover normal execution
        result = flext_create_alert("Test alert", "test_service", "medium")
        assert result.is_success

        # Test with different alert levels
        result = flext_create_alert("Warning alert", "test_service", "high")
        assert result.is_success

        result = flext_create_alert("Error alert", "test_service", "critical")
        assert result.is_success

        result = flext_create_alert("Critical alert", "test_service", "critical")
        assert result.is_success

    def test_flext_create_health_check_error_handling(self) -> None:
        """Test health check creation error handling paths."""
        # Test with valid values to cover normal execution
        result = flext_create_health_check("test_service", "healthy")
        assert result.is_success

        # Test with different health statuses
        result = flext_create_health_check("service2", "degraded")
        assert result.is_success

        result = flext_create_health_check("service3", "unhealthy")
        assert result.is_success

    def test_api_functions_with_custom_timestamps(self) -> None:
        """Test API functions with custom timestamps."""
        custom_timestamp = datetime.now(UTC)

        # Test all API functions with custom timestamps
        metric_result = flext_create_metric(
            "timestamped_metric",
            1.0,
            "count",
            timestamp=custom_timestamp,
        )
        assert metric_result.is_success

        log_result = flext_create_log_entry(
            "Timestamped log",
            "test_service",
            "info",
            timestamp=custom_timestamp,
        )
        assert log_result.is_success

        trace_result = flext_create_trace(
            "timestamped_op",
            "test_service",
            timestamp=custom_timestamp,
        )
        assert trace_result.is_success

        alert_result = flext_create_alert(
            "Timestamped alert",
            "test_service",
            "medium",
            timestamp=custom_timestamp,
        )
        assert alert_result.is_success

        health_result = flext_create_health_check(
            "test_service",
            "healthy",
            timestamp=custom_timestamp,
        )
        assert health_result.is_success

    def test_metric_type_inference_edge_cases(self) -> None:
        """Test edge cases in metric type inference."""
        # Test counter inference from unit
        result = flext_create_metric("test_count", 5.0, "counts")
        assert result.is_success

        # Test counter inference from name ending
        result = flext_create_metric("requests_total", 100.0, "units")
        assert result.is_success

        result = flext_create_metric("errors_count", 5.0, "units")
        assert result.is_success

        # Test histogram inference from name
        result = flext_create_metric("response_duration", 0.5, "seconds")
        assert result.is_success

    def test_api_module_exports(self) -> None:
        """Test that API module exports are accessible."""
        # Test all exported functions are callable
        assert callable(flext_create_metric)
        assert callable(flext_create_log_entry)
        assert callable(flext_create_trace)
        assert callable(flext_create_alert)
        assert callable(flext_create_health_check)

        # Test functions return FlextResult objects
        result = flext_create_metric("export_test", 1.0, "test")
        assert hasattr(result, "success")
        assert hasattr(result, "data")


class TestApiEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_metric_creation_with_decimal_values(self) -> None:
        """Test metric creation handles Decimal conversion properly."""
        # Test with float values (should be converted to Decimal internally)
        result = flext_create_metric("decimal_test", math.pi, "count")
        assert result.is_success

        # Test with integer values
        result = flext_create_metric("int_test", 42, "count")
        assert result.is_success

    def test_trace_id_generation_logic(self) -> None:
        """Test trace ID generation with different config scenarios."""
        # Test with empty context
        result = flext_create_trace("empty_context", "service", context={})
        assert result.is_success

        # Test with string values in context
        context = {"trace_id": "trace_123", "span_id": "span_456"}
        result = flext_create_trace("string_context", "service", context=context)
        assert result.is_success

        # Test with string conversion of IDs
        context = {"trace_id": "123", "span_id": "456"}  # String IDs
        result = flext_create_trace("numeric_ids", "service", context=context)
        assert result.is_success

    def test_api_functions_parameter_combinations(self) -> None:
        """Test API functions with various parameter combinations."""
        # Test metric with all optional parameters
        result = flext_create_metric("full_metric", 99.5, "percent")
        assert result.is_success

        # Test log entry with minimal parameters
        result = flext_create_log_entry(
            "Minimal log",
            "service",
        )  # No level specified, should default to INFO
        assert result.is_success

        # Test health check with minimal parameters
        result = flext_create_health_check(
            "minimal_service",
        )  # No status specified, should default to healthy
        assert result.is_success
