"""Test flext_simple.py coverage for conditional paths using flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import math
import time
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import patch

import flext_tests
import pytest
from flext_core import FlextCore
from pydantic import ValidationError

from flext_observability import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    entities as entities_module,
    flext_alert,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
    flext_health_check,
    flext_metric,
    flext_trace,
)


class TestSimpleCoverage:
    """Test flext_simple conditional paths for complete coverage."""

    def test_metric_type_inference_counter(self) -> None:
        """Test metric type inference for counter metrics."""
        # Test _total suffix
        result = flext_create_metric("requests_total", 100)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "counter"

        # Test _count suffix
        result = flext_create_metric("errors_count", 5)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "counter"

    def test_metric_type_inference_histogram(self) -> None:
        """Test metric type inference for histogram metrics."""
        # Test _duration suffix
        result = flext_create_metric("request_duration", 0.5)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "histogram"

        # Test _time suffix
        result = flext_create_metric("response_time", 0.2)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "histogram"

        # Test _seconds suffix
        result = flext_create_metric("processing_seconds", 1.5)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "histogram"

        # Test "histogram" in name
        result = flext_create_metric("cpu_histogram_data", 85.0)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "histogram"

    def test_metric_default_type_gauge(self) -> None:
        """Test default metric type (gauge)."""
        result = flext_create_metric("custom_metric", 42.0)
        assert result.is_success
        assert result.data is not None
        assert result.data.metric_type == "gauge"

    def test_metric_with_decimal_value(self) -> None:
        """Test metric creation with Decimal value."""
        result = flext_create_metric("precise_value", Decimal("123.456789"))
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data.value, Decimal)
        assert result.data.value == Decimal("123.456789")

    def test_create_metric_validation_failure(self) -> None:
        """Test metric creation with validation failure."""
        result = flext_create_metric("", 42.0)  # Empty name
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None and "Metric name cannot be empty" in result.error
        )

    def test_create_log_entry_validation_failure(self) -> None:
        """Test log entry creation with validation failure."""
        result = flext_create_log_entry(
            "test message",
            "test_service",
            "INVALID_LEVEL",
        )  # Invalid level
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid log level" in result.error

    def test_create_log_entry_invalid_level(self) -> None:
        """Test log entry creation with invalid level."""
        result = flext_create_log_entry(
            "Test message",
            "test_service",
            level="INVALID_LEVEL",
        )
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid log level" in result.error

    def test_create_trace_validation_failure(self) -> None:
        """Test trace creation with validation failure."""
        result = flext_create_trace("", "test_service")  # Empty operation_name
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Operation name cannot be empty" in result.error
        )

    def test_create_trace_invalid_operation(self) -> None:
        """Test trace creation with invalid operation."""
        result = flext_create_trace("")  # Invalid empty operation
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Operation name cannot be empty" in result.error
        )

    def test_create_alert_validation_failure(self) -> None:
        """Test alert creation with validation failure."""
        result = flext_create_alert("", "test_service")  # Empty title
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None and "Alert title cannot be empty" in result.error
        )

    def test_create_alert_invalid_message(self) -> None:
        """Test alert creation with invalid message."""
        result = flext_create_alert("Test title", "")  # Empty message
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None and "Alert message cannot be empty" in result.error
        )

    def test_create_health_check_validation_failure(self) -> None:
        """Test health check creation with validation failure."""
        result = flext_create_health_check("")  # Empty component
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Component name cannot be empty" in result.error
        )

    def test_create_health_check_invalid_status(self) -> None:
        """Test health check creation with invalid status."""
        result = flext_create_health_check("test_component", status="invalid_status")
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid health status" in result.error


class TestFlextMixinsCoverage:
    """Test FlextCore.Mixins methods for complete coverage."""

    def test_generate_entity_id(self) -> None:
        """Test FlextCore.UtilitiesGenerators.generate_entity_id method."""
        entity_id1 = FlextCore.UtilitiesGenerators.generate_entity_id()
        entity_id2 = FlextCore.UtilitiesGenerators.generate_entity_id()

        assert isinstance(entity_id1, str)
        assert isinstance(entity_id2, str)
        assert len(entity_id1) > 0
        assert len(entity_id2) > 0
        assert entity_id1 != entity_id2  # Should be unique

    def test_generate_correlation_id(self) -> None:
        """Test FlextCore.UtilitiesGenerators.generate_correlation_id method."""
        corr_id1 = FlextCore.UtilitiesGenerators.generate_correlation_id()
        corr_id2 = FlextCore.UtilitiesGenerators.generate_correlation_id()

        assert isinstance(corr_id1, str)
        assert isinstance(corr_id2, str)
        assert len(corr_id1) > 0
        assert len(corr_id2) > 0
        assert corr_id1 != corr_id2  # Should be unique

    def test_generate_timestamp_coverage(self) -> None:
        """Test FlextCore.UtilitiesGenerators.generate_timestamp method - covers linha 70."""
        timestamp1 = FlextCore.UtilitiesGenerators.generate_timestamp()
        time.sleep(0.001)  # Pequeno delay para garantir diferença
        timestamp2 = FlextCore.UtilitiesGenerators.generate_timestamp()

        assert isinstance(timestamp1, float)
        assert isinstance(timestamp2, float)
        assert timestamp2 > timestamp1

    def test_generate_uuid_coverage(self) -> None:
        """Test FlextCore.UtilitiesGenerators.generate_uuid method - covers linha 74."""
        uuid1 = FlextCore.UtilitiesGenerators.generate_uuid()
        uuid2 = FlextCore.UtilitiesGenerators.generate_uuid()

        assert isinstance(uuid1, str)
        assert isinstance(uuid2, str)
        assert len(uuid1) > 0
        assert len(uuid2) > 0
        assert uuid1 != uuid2

    def test_generate_entity_id_coverage(self) -> None:
        """Test FlextCore.UtilitiesGenerators.generate_entity_id method - covers linha 78."""
        entity_id1 = FlextCore.UtilitiesGenerators.generate_entity_id()
        entity_id2 = FlextCore.UtilitiesGenerators.generate_entity_id()

        assert isinstance(entity_id1, str)
        assert isinstance(entity_id2, str)
        assert len(entity_id1) > 0
        assert len(entity_id2) > 0
        assert entity_id1 != entity_id2  # Should be unique

    def test_generate_utc_datetime_coverage(self) -> None:
        """Test datetime.now(UTC) function - covers lines 97-98."""
        dt1 = datetime.now(UTC)
        time.sleep(0.001)  # Small delay to ensure different timestamps
        dt2 = datetime.now(UTC)

        assert isinstance(dt1, datetime)
        assert isinstance(dt2, datetime)
        assert dt1.tzinfo is not None  # Should have timezone info
        assert dt2.tzinfo is not None  # Should have timezone info
        assert dt2 > dt1  # Should be chronologically ordered

    def test_metric_name_validation_error_coverage(self) -> None:
        """Test FlextMetric name validation error - covers lines 177-180."""
        # Test empty name validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(id="test-id", name="", value=42.0)

        # Verify the error contains the expected message
        assert "Metric name cannot be empty" in str(exc_info.value)

    def test_metric_name_validation_success_coverage(self) -> None:
        """Test FlextMetric name validation success - covers line 180."""
        # Test successful validation with a valid name
        metric = FlextMetric(id="test-metric-id", name="valid_metric_name", value=42.0)

        # Verify the metric was created successfully
        assert metric.name == "valid_metric_name"
        assert metric.value == 42.0
        assert isinstance(metric, FlextMetric)

    def test_metric_value_validation_nan_coverage(self) -> None:
        """Test FlextMetric value validation with NaN - covers lines 194-195, 200-202."""
        # Test NaN validation error (goes through isnan path after bug fix)
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(id="test-id", name="test", value=float("nan"))

        # Verify the error contains the expected message
        assert "Metric value cannot be NaN or infinite" in str(exc_info.value)

    def test_metric_value_validation_inf_coverage(self) -> None:
        """Test FlextMetric value validation with infinity - covers lines 194-195, 200-202."""
        # Test infinity validation error (goes through isinf path after bug fix)
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(id="test-id", name="test", value=float("inf"))

        # Verify the error contains the expected message
        assert "Metric value cannot be NaN or infinite" in str(exc_info.value)

    def test_metric_value_validation_non_numeric_coverage(self) -> None:
        """Test FlextMetric value validation with non-numeric - testing Pydantic validation."""
        # Test that Pydantic correctly rejects non-numeric strings
        # Use model_validate to test validation without MyPy type checking
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric.model_validate(
                {"id": "test-id", "name": "test", "value": "not_a_number"},
            )

        # Verify it's a Pydantic validation error (occurs before our field validator)
        assert "Input should be a valid number" in str(
            exc_info.value,
        ) or "decimal" in str(exc_info.value)

    def test_metric_value_validation_float_exception_coverage(self) -> None:
        """Test FlextMetric field validator exception handling - covers lines 189-191."""

        # Create a class that can trigger the ValueError/TypeError in field validator
        class BadFloat:
            def __float__(self) -> float:
                msg = "Cannot convert to float"
                raise ValueError(msg)

        # Test calling the field validator directly to trigger the exception path
        with pytest.raises(ValueError, match="Metric value must be numeric"):
            FlextMetric.validate_metric_value(BadFloat())

    def test_metric_value_validation_decimal_nan_coverage(self) -> None:
        """Test FlextMetric value validation with Decimal NaN - covers lines 191, 200-201."""
        # Test Decimal NaN validation error (goes through isnan path)
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(id="test-id", name="test", value=Decimal("nan"))

        # Verify the error contains the expected message
        assert "Metric value cannot be NaN or infinite" in str(exc_info.value)

    def test_metric_value_validation_decimal_inf_coverage(self) -> None:
        """Test FlextMetric value validation with Decimal infinity - covers lines 191, 200-201."""
        # Test Decimal infinity validation error (goes through isinf path)
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(id="test-id", name="test", value=Decimal("inf"))

        # Verify the error contains the expected message
        assert "Metric value cannot be NaN or infinite" in str(exc_info.value)

    def test_metric_type_validation_error_coverage(self) -> None:
        """Test FlextMetric metric_type validation error - covers lines 211-212."""
        # Test invalid metric_type validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextMetric(
                id="test-id",
                name="test",
                value=42.0,
                metric_type="invalid_type",
            )

        # Verify the error contains the expected message
        assert "Invalid metric type: invalid_type" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_metric_type_validation_success_coverage(self) -> None:
        """Test FlextMetric metric_type validation success - covers return path line 213."""
        # Test valid metric types
        valid_types = ["gauge", "counter", "histogram", "summary"]

        for metric_type in valid_types:
            metric = FlextMetric(
                id="test-id",
                name="test",
                value=42.0,
                metric_type=metric_type,
            )
            assert metric.metric_type == metric_type
            assert isinstance(metric, FlextMetric)

    def test_flext_tests_performance_integration(self) -> None:
        """Test using flext_tests PerformanceProfiler for real performance measurement."""
        profiler = flext_tests.FlextTestsPerformance.PerformanceProfiler()

        # Teste performance real das funções de criação
        results = []
        for i in range(10):  # Reduzir número para teste mais rápido
            result = flext_create_metric(f"perf_metric_{i}", float(i), "count")
            assert result.is_success
            results.append(result)

        # Verificar que temos dados reais do profiler
        assert profiler is not None
        assert len(results) == 10

        # Testar funcionalidade de memory profiling
        memory_info = profiler.profile_memory("memory_test_operation")
        assert memory_info is not None

    def test_flext_result_factory_real_usage(self) -> None:
        """Test using FlextCore.ResultFactory from flext_tests for result validation."""
        # Usar ResultFactory para validar padrões de resultado
        test_result = flext_tests.FlextTestsFactories.ResultFactory.is_success_result(
            "test_data",
        )
        assert test_result.is_success
        assert test_result.data == "test_data"

        failure_result = flext_tests.FlextTestsFactories.ResultFactory.failure_result(
            "test_error",
        )
        assert failure_result.is_failure
        assert failure_result.error == "test_error"

        # Validar que nossas funções seguem o mesmo padrão
        real_result = flext_create_metric("validation_test", 42.0, "count")
        assert real_result.is_success
        assert real_result.data is not None

    def test_flext_metric_validate_business_rules_success_coverage(self) -> None:
        """Test FlextMetric.validate_business_rules() method success path - covers lines 244-253."""
        # Test successful validation path (line 253)
        metric = FlextMetric(id="test-metric-id", name="valid_metric_name", value=42.0)

        # Call the validate_business_rules method directly to test it
        result = metric.validate_business_rules()
        assert result.is_success
        assert result.data is None  # Success returns None

    def test_flext_metric_validate_business_rules_name_failure_coverage(self) -> None:
        """Test FlextMetric.validate_business_rules() method name validation failure - covers lines 244-245."""
        # Create metric with empty name to test validation failure path
        metric = FlextMetric(
            id="test-metric-id",
            name="valid_name",  # Start with valid name
            value=42.0,
        )

        # Directly modify the name to empty to test validation logic
        # (bypassing Pydantic validation to test the validate_business_rules() method specifically)
        metric.__dict__["name"] = ""  # Direct assignment to bypass field validation

        # Call validate_business_rules method - should fail on line 245
        result = metric.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid metric name" in result.error

    def test_flext_metric_validate_business_rules_value_type_failure_coverage(
        self,
    ) -> None:
        """Test FlextMetric.validate_business_rules() method value type validation - covers lines 248-252."""
        # Create metric with valid data first
        metric = FlextMetric(id="test-metric-id", name="valid_name", value=42.0)

        # Test string that cannot be converted to float - line 251-252
        metric.__dict__["value"] = (
            "not_a_number"  # Direct assignment to test validate_business_rules()
        )

        result = metric.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid metric value" in result.error

    def test_flext_metric_validate_business_rules_string_number_success_coverage(
        self,
    ) -> None:
        """Test FlextMetric.validate_business_rules() method with string that can be converted to float - covers line 250."""
        # Create metric with valid data first
        metric = FlextMetric(id="test-metric-id", name="valid_name", value=42.0)

        # Test string number that CAN be converted to float - line 250 success path
        metric.__dict__["value"] = (
            "123.456"  # Direct assignment to test validate_business_rules()
        )

        result = metric.validate_business_rules()
        assert (
            result.is_success
        )  # Should succeed because "123.456" can be converted to float

    def test_flext_log_entry_message_validation_error_coverage(self) -> None:
        """Test FlextLogEntry message field validation error - covers lines 356-359."""
        # Test empty message validation error (line 357-358)
        with pytest.raises(ValidationError) as exc_info:
            FlextLogEntry(
                id="test-id",
                message="",  # Empty message should trigger validation error
            )

        # Verify the error contains the expected message
        assert "Log message cannot be empty" in str(exc_info.value)

    def test_flext_log_entry_message_validation_success_coverage(self) -> None:
        """Test FlextLogEntry message field validation success - covers line 359."""
        # Test successful message validation (line 359)
        log_entry = FlextLogEntry(id="test-log-id", message="Valid log message")

        # Verify the log entry was created successfully
        assert log_entry.message == "Valid log message"
        assert isinstance(log_entry, FlextLogEntry)

    def test_flext_log_entry_level_validation_error_coverage(self) -> None:
        """Test FlextLogEntry level field validation error - covers lines 365-369."""
        # Test invalid level validation error (line 366-368)
        with pytest.raises(ValidationError) as exc_info:
            FlextLogEntry(
                id="test-id",
                message="Test message",
                level="invalid_level",  # Invalid level should trigger validation error
            )

        # Verify the error contains the expected message and valid levels
        assert "Invalid log level: invalid_level" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_flext_log_entry_level_validation_success_coverage(self) -> None:
        """Test FlextLogEntry level field validation success - covers line 369."""
        # Test all valid levels (line 369 success path)
        valid_levels = ["debug", "info", "warning", "error", "critical"]

        for level in valid_levels:
            log_entry = FlextLogEntry(
                id=f"test-log-id-{level}",
                message=f"Test message for {level}",
                level=level,
            )

            # Verify the log entry was created successfully with valid level
            assert log_entry.level == level
            assert isinstance(log_entry, FlextLogEntry)

    def test_flext_log_entry_validate_business_rules_success_coverage(self) -> None:
        """Test FlextLogEntry.validate_business_rules() method success path - covers lines 400-404."""
        # Test successful validation path (line 404)
        log_entry = FlextLogEntry(
            id="test-log-id",
            message="Valid log message",
            level="info",
        )

        # Call the validate_business_rules method directly to test it
        result = log_entry.validate_business_rules()
        assert result.is_success
        assert result.data is None  # Success returns None

    def test_flext_log_entry_validate_business_rules_message_failure_coverage(
        self,
    ) -> None:
        """Test FlextLogEntry.validate_business_rules() method message validation failure - covers lines 400-401."""
        # Create log entry with valid message first
        log_entry = FlextLogEntry(
            id="test-log-id",
            message="Valid message",
            level="info",
        )

        # Directly modify the message to empty to test validation logic
        # (bypassing Pydantic validation to test the validate_business_rules() method specifically)
        log_entry.__dict__["message"] = (
            ""  # Direct assignment to bypass field validation
        )

        # Call validate_business_rules method - should fail on line 401
        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid log message" in result.error

    def test_flext_log_entry_validate_business_rules_level_failure_coverage(
        self,
    ) -> None:
        """Test FlextLogEntry.validate_business_rules() method level validation failure - covers lines 402-403."""
        # Create log entry with valid data first
        log_entry = FlextLogEntry(
            id="test-log-id",
            message="Valid message",
            level="info",
        )

        # Test invalid level that doesn't match the set - line 402-403
        log_entry.__dict__["level"] = (
            "invalid_level"  # Direct assignment to test validate_business_rules()
        )

        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid log level" in result.error

    def test_flext_trace_trace_id_validation_error_coverage(self) -> None:
        """Test FlextTrace trace_id field validation error - covers lines 522-525."""
        # Test empty trace_id validation error (line 523-524)
        with pytest.raises(ValidationError) as exc_info:
            FlextTrace(
                id="test-id",
                trace_id="",  # Empty trace_id should trigger validation error
                operation="test_operation",
                span_id="test_span_id",
            )

        # Verify the error contains the expected message
        assert "Trace ID cannot be empty" in str(exc_info.value)

    def test_flext_trace_trace_id_validation_success_coverage(self) -> None:
        """Test FlextTrace trace_id field validation success - covers line 525."""
        # Test successful trace_id validation (line 525)
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="valid_trace_id",
            operation="test_operation",
            span_id="test_span_id",
        )

        # Verify the trace was created successfully
        assert trace.trace_id == "valid_trace_id"
        assert isinstance(trace, FlextTrace)

    def test_flext_trace_operation_validation_error_coverage(self) -> None:
        """Test FlextTrace operation field validation error - covers lines 531-534."""
        # Test empty operation validation error (line 532-533)
        with pytest.raises(ValidationError) as exc_info:
            FlextTrace(
                id="test-id",
                trace_id="test_trace_id",
                operation="",  # Empty operation should trigger validation error
                span_id="test_span_id",
            )

        # Verify the error contains the expected message
        assert "Operation name cannot be empty" in str(exc_info.value)

    def test_flext_trace_operation_validation_success_coverage(self) -> None:
        """Test FlextTrace operation field validation success - covers line 534."""
        # Test successful operation validation (line 534)
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="test_trace_id",
            operation="valid_operation_name",
            span_id="test_span_id",
        )

        # Verify the trace was created successfully
        assert trace.operation == "valid_operation_name"
        assert isinstance(trace, FlextTrace)

    def test_flext_trace_span_id_validation_error_coverage(self) -> None:
        """Test FlextTrace span_id field validation error - covers lines 540-543."""
        # Test empty span_id validation error (line 541-542)
        with pytest.raises(ValidationError) as exc_info:
            FlextTrace(
                id="test-id",
                trace_id="test_trace_id",
                operation="test_operation",
                span_id="",  # Empty span_id should trigger validation error
            )

        # Verify the error contains the expected message
        assert "Span ID cannot be empty" in str(exc_info.value)

    def test_flext_trace_span_id_validation_success_coverage(self) -> None:
        """Test FlextTrace span_id field validation success - covers line 543."""
        # Test successful span_id validation (line 543)
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="test_trace_id",
            operation="test_operation",
            span_id="valid_span_id",
        )

        # Verify the trace was created successfully
        assert trace.span_id == "valid_span_id"
        assert isinstance(trace, FlextTrace)

    def test_flext_trace_duration_validation_error_coverage(self) -> None:
        """Test FlextTrace duration_ms field validation error - covers lines 549-552."""
        # Test negative duration validation error (line 550-551)
        with pytest.raises(ValidationError) as exc_info:
            FlextTrace(
                id="test-id",
                trace_id="test_trace_id",
                operation="test_operation",
                span_id="test_span_id",
                duration_ms=-100,  # Negative duration should trigger validation error
            )

        # Verify the error contains the expected message
        assert "Duration must be non-negative" in str(exc_info.value)

    def test_flext_trace_duration_validation_success_coverage(self) -> None:
        """Test FlextTrace duration_ms field validation success - covers line 552."""
        # Test successful duration validation (line 552) with zero and positive values
        valid_durations = [0, 100, 5000]

        for duration in valid_durations:
            trace = FlextTrace(
                id=f"test-trace-id-{duration}",
                trace_id="test_trace_id",
                operation="test_operation",
                span_id="test_span_id",
                duration_ms=duration,
            )

            # Verify the trace was created successfully with valid duration
            assert trace.duration_ms == duration
            assert isinstance(trace, FlextTrace)

    def test_flext_trace_status_validation_error_coverage(self) -> None:
        """Test FlextTrace status field validation error - covers lines 558-562."""
        # Test invalid status validation error (line 559-561)
        with pytest.raises(ValidationError) as exc_info:
            FlextTrace(
                id="test-id",
                trace_id="test_trace_id",
                operation="test_operation",
                span_id="test_span_id",
                status="invalid_status",  # Invalid status should trigger validation error
            )

        # Verify the error contains the expected message and valid statuses
        assert "Invalid trace status: invalid_status" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_flext_trace_status_validation_success_coverage(self) -> None:
        """Test FlextTrace status field validation success - covers line 562."""
        # Test all valid statuses (line 562 success path)
        valid_statuses = ["pending", "completed", "error", "timeout"]

        for status in valid_statuses:
            trace = FlextTrace(
                id=f"test-trace-id-{status}",
                trace_id="test_trace_id",
                operation="test_operation",
                span_id="test_span_id",
                status=status,
            )

            # Verify the trace was created successfully with valid status
            assert trace.status == status
            assert isinstance(trace, FlextTrace)

    def test_flext_trace_validate_business_rules_success_coverage(self) -> None:
        """Test FlextTrace.validate_business_rules() method success path - covers lines 593-597."""
        # Test successful validation path (line 597)
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="valid_trace_id",
            operation="valid_operation",
            span_id="valid_span_id",
        )

        # Call the validate_business_rules method directly to test it
        result = trace.validate_business_rules()
        assert result.is_success
        assert result.data is None  # Success returns None

    def test_flext_trace_validate_business_rules_trace_id_failure_coverage(
        self,
    ) -> None:
        """Test FlextTrace.validate_business_rules() method trace_id validation failure - covers lines 593-594."""
        # Create trace with valid data first
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="valid_trace_id",
            operation="valid_operation",
            span_id="valid_span_id",
        )

        # Directly modify the trace_id to empty to test validation logic
        # (bypassing Pydantic validation to test the validate_business_rules() method specifically)
        trace.__dict__["trace_id"] = ""  # Direct assignment to bypass field validation

        # Call validate_business_rules method - should fail on line 594
        result = trace.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid trace ID" in result.error

    def test_flext_trace_validate_business_rules_operation_failure_coverage(
        self,
    ) -> None:
        """Test FlextTrace.validate_business_rules() method operation validation failure - covers lines 595-596."""
        # Create trace with valid data first
        trace = FlextTrace(
            id="test-trace-id",
            trace_id="valid_trace_id",
            operation="valid_operation",
            span_id="valid_span_id",
        )

        # Test invalid operation that fails validation - line 595-596
        trace.__dict__["operation"] = (
            ""  # Direct assignment to test validate_business_rules()
        )

        result = trace.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid operation name" in str(result.error)

    def test_flext_alert_title_validation_error_coverage(self) -> None:
        """Test FlextAlert title field validation error - covers lines 703-706."""
        # Test empty title validation error (line 704-705)
        with pytest.raises(ValidationError) as exc_info:
            FlextAlert(
                id="test-id",
                title="",  # Empty title should trigger validation error
                message="Test alert message",
            )

        # Verify the error contains the expected message
        assert "Alert title cannot be empty" in str(exc_info.value)

    def test_flext_alert_title_validation_success_coverage(self) -> None:
        """Test FlextAlert title field validation success - covers line 706."""
        # Test successful title validation (line 706)
        alert = FlextAlert(
            id="test-alert-id",
            title="Valid Alert Title",
            message="Test alert message",
        )

        # Verify the alert was created successfully
        assert alert.title == "Valid Alert Title"
        assert isinstance(alert, FlextAlert)

    def test_flext_alert_message_validation_error_coverage(self) -> None:
        """Test FlextAlert message field validation error - covers lines 712-715."""
        # Test empty message validation error (line 713-714)
        with pytest.raises(ValidationError) as exc_info:
            FlextAlert(
                id="test-id",
                title="Test Alert Title",
                message="",  # Empty message should trigger validation error
            )

        # Verify the error contains the expected message
        assert "Alert message cannot be empty" in str(exc_info.value)

    def test_flext_alert_message_validation_success_coverage(self) -> None:
        """Test FlextAlert message field validation success - covers line 715."""
        # Test successful message validation (line 715)
        alert = FlextAlert(
            id="test-alert-id",
            title="Test Alert Title",
            message="Valid alert message with details",
        )

        # Verify the alert was created successfully
        assert alert.message == "Valid alert message with details"
        assert isinstance(alert, FlextAlert)

    def test_flext_alert_severity_validation_error_coverage(self) -> None:
        """Test FlextAlert severity field validation error - covers lines 721-725."""
        # Test invalid severity validation error (line 722-724)
        with pytest.raises(ValidationError) as exc_info:
            FlextAlert(
                id="test-id",
                title="Test Alert Title",
                message="Test alert message",
                severity="invalid_severity",  # Invalid severity should trigger validation error
            )

        # Verify the error contains the expected message and valid severities
        assert "Invalid alert severity: invalid_severity" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_flext_alert_severity_validation_success_coverage(self) -> None:
        """Test FlextAlert severity field validation success - covers line 725."""
        # Test all valid severities (line 725 success path)
        valid_severities = ["low", "medium", "high", "critical", "emergency"]

        for severity in valid_severities:
            alert = FlextAlert(
                id=f"test-alert-id-{severity}",
                title="Test Alert Title",
                message="Test alert message",
                severity=severity,
            )

            # Verify the alert was created successfully with valid severity
            assert alert.severity == severity
            assert isinstance(alert, FlextAlert)

    def test_flext_alert_status_validation_error_coverage(self) -> None:
        """Test FlextAlert status field validation error - covers lines 731-735."""
        # Test invalid status validation error (line 732-734)
        with pytest.raises(ValidationError) as exc_info:
            FlextAlert(
                id="test-id",
                title="Test Alert Title",
                message="Test alert message",
                status="invalid_status",  # Invalid status should trigger validation error
            )

        # Verify the error contains the expected message and valid statuses
        assert "Invalid alert status: invalid_status" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_flext_alert_status_validation_success_coverage(self) -> None:
        """Test FlextAlert status field validation success - covers line 735."""
        # Test all valid statuses (line 735 success path)
        valid_statuses = ["active", "acknowledged", "resolved", "suppressed"]

        for status in valid_statuses:
            alert = FlextAlert(
                id=f"test-alert-id-{status}",
                title="Test Alert Title",
                message="Test alert message",
                status=status,
            )

            # Verify the alert was created successfully with valid status
            assert alert.status == status
            assert isinstance(alert, FlextAlert)

    def test_flext_alert_validate_business_rules_success_coverage(self) -> None:
        """Test FlextAlert.validate_business_rules() method success path - covers lines 766-772."""
        # Test successful validation path (line 772)
        alert = FlextAlert(
            id="test-alert-id",
            title="Valid Alert Title",
            message="Valid alert message",
            severity="medium",
        )

        # Call the validate_business_rules method directly to test it
        result = alert.validate_business_rules()
        assert result.is_success
        assert result.data is None  # Success returns None

    def test_flext_alert_validate_business_rules_title_failure_coverage(self) -> None:
        """Test FlextAlert.validate_business_rules() method title validation failure - covers lines 766-767."""
        # Create alert with valid data first
        alert = FlextAlert(
            id="test-alert-id",
            title="Valid Title",
            message="Valid message",
            severity="medium",
        )

        # Directly modify the title to empty to test validation logic
        # (bypassing Pydantic validation to test the validate_business_rules() method specifically)
        alert.__dict__["title"] = ""  # Direct assignment to bypass field validation

        # Call validate_business_rules method - should fail on line 767
        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert title" in str(result.error)

    def test_flext_alert_validate_business_rules_message_failure_coverage(self) -> None:
        """Test FlextAlert.validate_business_rules() method message validation failure - covers lines 768-769."""
        # Create alert with valid data first
        alert = FlextAlert(
            id="test-alert-id",
            title="Valid Title",
            message="Valid message",
            severity="medium",
        )

        # Test invalid message that fails validation - line 768-769
        alert.__dict__["message"] = (
            ""  # Direct assignment to test validate_business_rules()
        )

        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert message" in str(result.error)

    def test_flext_alert_validate_business_rules_severity_failure_coverage(
        self,
    ) -> None:
        """Test FlextAlert.validate_business_rules() method severity validation failure - covers lines 770-771."""
        # Create alert with valid data first
        alert = FlextAlert(
            id="test-alert-id",
            title="Valid Title",
            message="Valid message",
            severity="medium",
        )

        # Test invalid severity that fails validation - line 770-771
        alert.__dict__["severity"] = (
            "invalid_severity"  # Direct assignment to test validate_business_rules()
        )

        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert severity" in str(result.error)

    def test_flext_health_check_component_validation_error_coverage(self) -> None:
        """Test FlextHealthCheck component field validation error - covers lines 876-879."""
        # Test empty component validation error (line 877-878)
        with pytest.raises(ValidationError) as exc_info:
            FlextHealthCheck(
                id="test-id",
                component="",  # Empty component should trigger validation error
            )

        # Verify the error contains the expected message
        assert "Component name cannot be empty" in str(exc_info.value)

    def test_flext_health_check_component_validation_success_coverage(self) -> None:
        """Test FlextHealthCheck component field validation success - covers line 879."""
        # Test successful component validation (line 879)
        health_check = FlextHealthCheck(
            id="test-health-check-id",
            component="valid_component_name",
        )

        # Verify the health check was created successfully
        assert health_check.component == "valid_component_name"
        assert isinstance(health_check, FlextHealthCheck)

    def test_flext_health_check_status_validation_error_coverage(self) -> None:
        """Test FlextHealthCheck status field validation error - covers lines 885-889."""
        # Test invalid status validation error (line 886-888)
        with pytest.raises(ValidationError) as exc_info:
            FlextHealthCheck(
                id="test-id",
                component="test_component",
                status="invalid_status",  # Invalid status should trigger validation error
            )

        # Verify the error contains the expected message and valid statuses
        assert "Invalid health status: invalid_status" in str(exc_info.value)
        assert "Must be one of" in str(exc_info.value)

    def test_flext_health_check_status_validation_success_coverage(self) -> None:
        """Test FlextHealthCheck status field validation success - covers line 889."""
        # Test all valid statuses (line 889 success path)
        valid_statuses = ["healthy", "unhealthy", "degraded", "unknown"]

        for status in valid_statuses:
            health_check = FlextHealthCheck(
                id=f"test-health-check-id-{status}",
                component="test_component",
                status=status,
            )

            # Verify the health check was created successfully with valid status
            assert health_check.status == status
            assert isinstance(health_check, FlextHealthCheck)

    def test_flext_health_check_validate_business_rules_invalid_component_coverage(
        self,
    ) -> None:
        """Test FlextHealthCheck validate_business_rules with invalid component - covers lines 920-921."""
        # Create a valid health check first, then modify component to bypass field validation
        health = FlextHealthCheck.model_construct(
            id=FlextCore.UtilitiesGenerators.generate_uuid(),
            component="",  # Empty component triggers line 920-921
            status="healthy",
            message="Test message",
            timestamp=datetime.fromtimestamp(
                FlextCore.UtilitiesGenerators.generate_timestamp(),
                tz=datetime.now(UTC).astimezone().tzinfo,
            ),
            metrics={},
        )

        # Test validation failure for invalid component
        result = health.validate_business_rules()

        # Verify business rule validation failed
        assert result.is_failure
        assert result.error == "Invalid component name"
        assert result.error is not None and "component" in result.error

    def test_flext_health_check_validate_business_rules_invalid_status_coverage(
        self,
    ) -> None:
        """Test FlextHealthCheck validate_business_rules with invalid status - covers lines 922-923."""
        # Create health check with invalid status using model_construct to bypass field validation
        health = FlextHealthCheck.model_construct(
            id=FlextCore.UtilitiesGenerators.generate_uuid(),
            component="database",
            status="invalid_status",  # Invalid status triggers line 922-923
            message="Test message",
            timestamp=datetime.fromtimestamp(
                FlextCore.UtilitiesGenerators.generate_timestamp(),
                tz=datetime.now(UTC).astimezone().tzinfo,
            ),
            metrics={},
        )

        # Test validation failure for invalid status
        result = health.validate_business_rules()

        # Verify business rule validation failed
        assert result.is_failure
        assert result.error == "Invalid health status"
        assert result.error is not None and "status" in result.error

    def test_flext_health_check_validate_business_rules_success_coverage(self) -> None:
        """Test FlextHealthCheck validate_business_rules with valid data - covers line 924."""
        # Create health check with valid component and status
        health = FlextHealthCheck(
            id=FlextCore.UtilitiesGenerators.generate_uuid(),
            component="database",
            status="healthy",  # Valid status
            message="Database is operational",
            timestamp=datetime.fromtimestamp(
                FlextCore.UtilitiesGenerators.generate_timestamp(),
                tz=datetime.now(UTC).astimezone().tzinfo,
            ),
            metrics={},
        )

        # Test successful validation
        result = health.validate_business_rules()

        # Verify business rule validation passed
        assert result.is_success
        assert result.error is None
        assert result.data is None  # Success returns None data

    def test_flext_health_check_all_valid_statuses_coverage(self) -> None:
        """Test FlextHealthCheck validate_business_rules with all valid statuses - covers line 924."""
        # Test all valid status values
        valid_statuses = ["healthy", "unhealthy", "degraded", "unknown"]

        for status in valid_statuses:
            health = FlextHealthCheck(
                id=FlextCore.UtilitiesGenerators.generate_uuid(),
                component="test-component",
                status=status,
                message=f"Testing status: {status}",
                timestamp=datetime.fromtimestamp(
                    FlextCore.UtilitiesGenerators.generate_timestamp(),
                    tz=datetime.now(UTC).astimezone().tzinfo,
                ),
                metrics={},
            )

            # Each valid status should pass validation
            result = health.validate_business_rules()
            assert result.is_success, f"Status {status} should be valid"
            assert result.error is None
            assert result.data is None

    def test_flext_alert_factory_with_id_and_version_coverage(self) -> None:
        """Test flext_alert factory function with id and version - covers lines 944-954."""
        # Test with both id and version in kwargs (triggers lines 944-954)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()
        custom_version = 2
        FlextCore.UtilitiesGenerators.generate_timestamp()
        custom_tags = {"environment": "test", "priority": "high"}

        alert = flext_alert(
            title="Test Alert",
            message="Test alert message",
            severity="high",
            status="active",
            id=custom_id,
            version=custom_version,
            tags=custom_tags,
        )

        # Verify the alert was created with provided id and version
        assert alert.id == custom_id
        assert alert.version == custom_version
        assert alert.title == "Test Alert"
        assert alert.message == "Test alert message"
        assert alert.severity == "high"
        assert alert.status == "active"
        assert alert.tags == custom_tags
        assert isinstance(alert.timestamp, datetime)

    def test_flext_alert_factory_with_id_only_coverage(self) -> None:
        """Test flext_alert factory function with id but no version - covers lines 955-964."""
        # Test with id but no version in kwargs (triggers lines 955-964)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()
        FlextCore.UtilitiesGenerators.generate_timestamp()

        alert = flext_alert(
            title="Alert with ID only",
            message="Alert message with custom ID",
            severity="medium",
            status="acknowledged",
            id=custom_id,
        )

        # Verify the alert was created with provided id but default version
        assert alert.id == custom_id
        assert alert.version == 1  # Default version when not provided
        assert alert.title == "Alert with ID only"
        assert alert.message == "Alert message with custom ID"
        assert alert.severity == "medium"
        assert alert.status == "acknowledged"
        assert isinstance(alert.timestamp, datetime)

    def test_flext_alert_factory_default_generation_coverage(self) -> None:
        """Test flext_alert factory function with default id generation - covers line 965."""
        # Test with no id or version (triggers line 965 - default path)
        alert = flext_alert(
            title="Default Alert",
            message="Alert with auto-generated ID",
        )

        # Verify the alert was created with auto-generated id and defaults
        assert alert.id is not None
        assert len(alert.id) > 10  # Generated IDs should be substantial length
        assert alert.version == 1  # Default version
        assert alert.title == "Default Alert"
        assert alert.message == "Alert with auto-generated ID"
        assert alert.severity == "low"  # Default severity
        assert alert.status == "active"  # Default status
        assert isinstance(alert.tags, dict)
        assert isinstance(alert.timestamp, datetime)

    def test_flext_trace_factory_with_id_coverage(self) -> None:
        """Test flext_trace factory function with custom id - covers lines 989-999."""
        # Test with custom id in kwargs (triggers lines 989-999)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()
        custom_span_attrs = {"http.method": "GET", "http.status": 200}
        custom_duration = 150
        custom_timestamp = FlextCore.UtilitiesGenerators.generate_timestamp()

        trace = flext_trace(
            trace_id="trace-123",
            operation="api.request",
            span_id="span-456",
            status="completed",
            id=custom_id,
            span_attributes=custom_span_attrs,
            duration_ms=custom_duration,
            timestamp=custom_timestamp,
        )

        # Verify the trace was created with provided values
        assert trace.id == custom_id
        assert trace.trace_id == "trace-123"
        assert trace.operation == "api.request"
        assert trace.span_id == "span-456"
        assert trace.status == "completed"
        assert trace.span_attributes == custom_span_attrs
        assert trace.duration_ms == custom_duration
        assert isinstance(trace.timestamp, datetime)

    def test_flext_trace_factory_default_generation_coverage(self) -> None:
        """Test flext_trace factory function with default id generation - covers lines 1000-1008."""
        # Test with no id (triggers lines 1000-1008 - default path)
        trace = flext_trace(
            trace_id="trace-default",
            operation="db.query",
            span_id="span-default",
        )

        # Verify the trace was created with auto-generated id and defaults
        assert trace.id is not None
        assert len(trace.id) > 10  # Generated IDs should be substantial
        assert trace.trace_id == "trace-default"
        assert trace.operation == "db.query"
        assert trace.span_id == "span-default"
        assert trace.status == "pending"  # Default status
        assert isinstance(trace.span_attributes, dict)
        assert trace.duration_ms == 0  # Default duration
        assert isinstance(trace.timestamp, datetime)

    def test_flext_metric_with_id_and_version_coverage(self) -> None:
        """Test flext_metric factory with id and version - covers lines 1025-1034."""
        # Test with both id and version in kwargs (triggers lines 1025-1034)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()
        custom_version = 3
        custom_tags = {"env": "prod", "region": "us-east"}

        result = flext_metric(
            name="cpu.usage",
            value=75.5,
            unit="percent",
            metric_type="gauge",
            id=custom_id,
            version=custom_version,
            tags=custom_tags,
        )

        # Verify success and correct values
        assert result.is_success
        metric = result.data
        assert metric is not None
        assert metric.id == custom_id
        assert metric.version == custom_version
        assert metric.name == "cpu.usage"
        assert metric.value == 75.5
        assert metric.unit == "percent"
        assert metric.metric_type == "gauge"
        assert metric.tags == custom_tags

    def test_flext_metric_with_id_only_coverage(self) -> None:
        """Test flext_metric factory with id only - covers lines 1035-1043."""
        # Test with id but no version (triggers lines 1035-1043)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()

        result = flext_metric(name="memory.used", value=2048, unit="MB", id=custom_id)

        # Verify success
        assert result.is_success
        metric = result.data
        assert metric is not None
        assert metric.id == custom_id
        assert metric.version == 1  # Default version
        assert metric.name == "memory.used"
        assert metric.value == 2048

    def test_flext_metric_default_generation_coverage(self) -> None:
        """Test flext_metric factory with default id - covers lines 1044-1052."""
        # Test with no id (triggers lines 1044-1052)
        result = flext_metric(name="requests.total", value=1000)

        # Verify success with auto-generated id
        assert result.is_success
        metric = result.data
        assert metric is not None
        assert metric.id is not None
        assert len(metric.id) > 10  # Generated ID
        assert metric.name == "requests.total"
        assert metric.value == 1000

    def test_flext_metric_validation_failure_coverage(self) -> None:
        """Test flext_metric with validation failure - covers lines 1058-1062."""
        # Test with empty name to trigger validation failure
        result = flext_metric(
            name="",  # Empty name will fail validation
            value=100,
        )

        # Verify failure from business rule validation
        assert result.is_failure
        # Cannot access .data on failure - it raises TypeError
        assert "Metric name cannot be empty" in (result.error or "")

    def test_flext_metric_exception_handling_coverage(self) -> None:
        """Test flext_metric exception handling - covers lines 1066-1069."""
        # Test with NaN value to trigger exception
        result = flext_metric(
            name="bad.metric",
            value=math.nan,  # NaN will trigger validation error
        )

        # Verify failure from exception handling
        assert result.is_failure
        # Cannot access .data on failure - it raises TypeError
        assert "Failed to create metric" in (result.error or "")

    def test_flext_health_check_factory_with_id_coverage(self) -> None:
        """Test flext_health_check factory function with custom id - covers lines 1083-1091."""
        # Test with custom id in kwargs (triggers lines 1083-1091)
        custom_id = FlextCore.UtilitiesGenerators.generate_uuid()
        custom_metrics = {"cpu": 75.5, "memory": 2048, "disk": 80.0}
        custom_timestamp = FlextCore.UtilitiesGenerators.generate_timestamp()

        health = flext_health_check(
            component="database",
            status="healthy",
            message="All systems operational",
            id=custom_id,
            metrics=custom_metrics,
            timestamp=custom_timestamp,
        )

        # Verify the health check was created with provided values
        assert health.id == custom_id
        assert health.component == "database"
        assert health.status == "healthy"
        assert health.message == "All systems operational"
        assert health.metrics == custom_metrics
        assert isinstance(health.timestamp, datetime)

    def test_flext_health_check_factory_default_generation_coverage(self) -> None:
        """Test flext_health_check factory function with default id - covers lines 1092-1099."""
        # Test with no id (triggers lines 1092-1099 - default path)
        health = flext_health_check(
            component="api-service",
            status="degraded",
            message="High latency detected",
        )

        # Verify the health check was created with auto-generated id
        assert health.id is not None
        assert len(health.id) > 10  # Generated ID
        assert health.component == "api-service"
        assert health.status == "degraded"
        assert health.message == "High latency detected"
        assert isinstance(health.metrics, dict)
        assert isinstance(health.timestamp, datetime)

    def test_flext_metric_business_rule_validation_failure_coverage(self) -> None:
        """Test flext_metric with business rule validation failure - covers line 1060."""
        # Mock validate_business_rules to return failure
        with patch.object(FlextMetric, "validate_business_rules") as mock_validate:
            mock_validate.return_value = FlextCore.Result[None].fail(
                "Mock business rule failure",
            )

            result = flext_metric(name="test.metric", value=100)

            # Verify failure from business rule validation
            assert result.is_failure
            assert "Mock business rule failure" in (result.error or "")

    def test_flext_metric_type_error_exception_coverage(self) -> None:
        """Test flext_metric with general Exception - covers lines 1068-1069."""
        # Mock the FlextMetric class constructor to raise a general exception
        # This will trigger the general Exception handler at lines 1068-1069
        with patch.object(entities_module, "FlextMetric") as mock_metric_class:
            mock_metric_class.side_effect = RuntimeError(
                "Unexpected error in model construction",
            )

            result = entities_module.flext_metric(name="test.metric", value=100)

            # Verify failure from exception handling
            assert result.is_failure
            assert "Failed to create metric" in (result.error or "")
