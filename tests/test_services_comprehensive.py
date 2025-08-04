"""Comprehensive tests for services.py - target 161 missing lines coverage.

Tests ALL uncovered methods and error paths to achieve 90%+ coverage.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import Mock, PropertyMock, patch

from flext_core import FlextContainer

from flext_observability.flext_simple import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


class TestFlextMetricsServiceComprehensive:
    """Test ALL methods in FlextMetricsService - target lines 81, 84, 114, 142-162, 166-191, 195-224."""

    def test_record_metric_invalid_metric_none(self) -> None:
        """Test record_metric with None metric (line 81)."""
        service = FlextMetricsService()

        result = service.record_metric(None)  # type: ignore[arg-type]

        assert result.is_failure
        assert "Invalid metric: missing name or value" in result.error

    def test_record_metric_invalid_metric_no_name(self) -> None:
        """Test record_metric with metric without name (line 84)."""
        service = FlextMetricsService()

        # Create mock metric without name
        mock_metric = Mock()
        mock_metric.name = ""
        mock_metric.value = 100

        result = service.record_metric(mock_metric)

        assert result.is_failure
        assert "Metric name must be a non-empty string" in result.error

    def test_record_metric_memory_cleanup(self) -> None:
        """Test record_metric memory cleanup (line 114)."""
        service = FlextMetricsService()

        # Create metric with proper attributes
        metric_result = flext_create_metric("test_metric", 1.0, unit="count")
        assert metric_result.success
        metric = metric_result.data

        # Fill store beyond MAX_METRICS_STORE_SIZE (1000) to trigger cleanup
        for i in range(1001):
            metric.value = float(i)
            service.record_metric(metric)

        # Verify cleanup happened (should keep only last 500)
        assert len(service._metrics_store["test_metric"]) == 500

    def test_get_metric_value_gauge(self) -> None:
        """Test get_metric_value for gauge metric (lines 142-146)."""
        service = FlextMetricsService()

        # Record gauge metric (no metric_type parameter - it's determined by usage)
        metric_result = flext_create_metric("gauge_metric", 50.0, "units")
        assert metric_result.success
        service.record_metric(metric_result.data)

        # Get value
        result = service.get_metric_value("gauge_metric")

        assert result.success
        assert result.data == 50.0

    def test_get_metric_value_counter(self) -> None:
        """Test get_metric_value for counter metric (lines 148-150)."""
        service = FlextMetricsService()

        # Record counter metrics
        metric_result = flext_create_metric("counter_metric", 10.0, "count")
        assert metric_result.success
        metric = metric_result.data

        service.record_metric(metric)
        metric.value = 20.0
        service.record_metric(metric)

        # Get value (should be sum)
        result = service.get_metric_value("counter_metric")

        assert result.success
        assert result.data == 30.0

    def test_get_metric_value_histogram(self) -> None:
        """Test get_metric_value for histogram metric (lines 152-157)."""
        service = FlextMetricsService()

        # Record histogram metrics
        metric_result = flext_create_metric("histogram_metric", 10.0, "histogram_unit")
        assert metric_result.success
        metric = metric_result.data

        service.record_metric(metric)
        metric.value = 20.0
        service.record_metric(metric)

        # Get value (should be mean)
        result = service.get_metric_value("histogram_metric")

        assert result.success
        assert result.data == 15.0  # (10 + 20) / 2

    def test_get_metric_value_not_found(self) -> None:
        """Test get_metric_value for non-existent metric (line 159)."""
        service = FlextMetricsService()

        result = service.get_metric_value("nonexistent_metric")

        assert result.is_failure
        assert "Metric 'nonexistent_metric' not found" in result.error

    def test_get_metric_value_exception(self) -> None:
        """Test get_metric_value exception handling (line 162)."""
        service = FlextMetricsService()

        # Force exception by corrupting internal state
        service._metric_gauges["bad_metric"] = "not_a_number"  # type: ignore[assignment]

        result = service.get_metric_value("bad_metric")

        assert result.is_failure
        assert "Failed to retrieve metric 'bad_metric'" in result.error

    def test_get_metrics_summary_success(self) -> None:
        """Test get_metrics_summary success path (lines 166-188)."""
        service = FlextMetricsService()

        # Record different metric types
        counter_result = flext_create_metric("counter", 10.0, "count")
        gauge_result = flext_create_metric("gauge", 50.0, "gauge_unit")
        histogram_result = flext_create_metric("histogram", 30.0, "histogram_unit")

        assert counter_result.success
        assert gauge_result.success
        assert histogram_result.success

        service.record_metric(counter_result.data)
        service.record_metric(gauge_result.data)
        service.record_metric(histogram_result.data)

        result = service.get_metrics_summary()

        assert result.success
        summary = result.data
        assert "service_info" in summary
        assert "counters" in summary
        assert "gauges" in summary
        assert "histograms" in summary
        assert summary["service_info"]["metrics_recorded"] == 3

    def test_get_metrics_summary_exception(self) -> None:
        """Test get_metrics_summary exception handling (line 191)."""
        service = FlextMetricsService()

        # Force exception by corrupting internal state
        service._metric_histograms["bad"] = ["not", "numbers"]  # type: ignore[assignment]

        result = service.get_metrics_summary()

        assert result.is_failure
        assert "Failed to generate metrics summary" in result.error

    def test_export_prometheus_format_success(self) -> None:
        """Test export_prometheus_format success path (lines 195-224)."""
        service = FlextMetricsService()

        # Record different types of metrics
        counter_result = flext_create_metric("requests_total", 100.0, "count")
        gauge_result = flext_create_metric("cpu_usage", 75.5, "gauge_unit")
        histogram_result = flext_create_metric("response_time", 0.5, "histogram_unit")

        assert counter_result.success
        assert gauge_result.success
        assert histogram_result.success

        service.record_metric(counter_result.data)
        service.record_metric(gauge_result.data)
        service.record_metric(histogram_result.data)

        result = service.export_prometheus_format()

        assert result.success
        prometheus_output = result.data
        assert "# TYPE requests_total counter" in prometheus_output
        assert "requests_total 100.0" in prometheus_output
        assert "# TYPE cpu_usage gauge" in prometheus_output
        assert "cpu_usage 75.5" in prometheus_output


class TestFlextTracingServiceComprehensive:
    """Test ALL methods in FlextTracingService - target lines 307, 310, 337, 371-402, 410-453, etc."""

    def test_start_trace_success(self) -> None:
        """Test start_trace success path."""
        service = FlextTracingService()

        trace_result = flext_create_trace("test_trace_id", "test_operation")
        assert trace_result.success

        result = service.start_trace(trace_result.data)

        assert result.success

    def test_start_trace_invalid_trace(self) -> None:
        """Test start_trace with invalid trace (line 307)."""
        service = FlextTracingService()

        result = service.start_trace(None)  # type: ignore[arg-type]

        assert result.is_failure
        assert "Invalid trace: missing trace_id or operation" in result.error

    def test_start_trace_invalid_trace_id(self) -> None:
        """Test start_trace with invalid trace ID (line 310)."""
        service = FlextTracingService()

        # Create mock trace with empty trace_id
        mock_trace = Mock()
        mock_trace.trace_id = ""
        mock_trace.operation = "test_op"

        result = service.start_trace(mock_trace)

        assert result.is_failure
        assert "Trace ID must be a non-empty string" in result.error

    def test_finish_trace_success(self) -> None:
        """Test finish_trace success path."""
        service = FlextTracingService()

        trace_result = flext_create_trace("test_trace_id", "test_operation")
        assert trace_result.success
        trace = trace_result.data

        # Start then finish trace
        service.start_trace(trace)
        result = service.finish_trace(trace.trace_id)

        assert result.success

    def test_finish_trace_not_found(self) -> None:
        """Test finish_trace with non-existent trace ID."""
        service = FlextTracingService()

        result = service.finish_trace("nonexistent_id")

        assert result.is_failure

    def test_get_trace_info_success(self) -> None:
        """Test get_trace_info success path (lines 455+)."""
        service = FlextTracingService()

        trace_result = flext_create_trace("test_trace_id", "test_operation")
        assert trace_result.success
        trace = trace_result.data

        service.start_trace(trace)
        result = service.get_trace_info(trace.trace_id)

        assert result.success

    def test_get_trace_info_not_found(self) -> None:
        """Test get_trace_info with non-existent trace ID."""
        service = FlextTracingService()

        result = service.get_trace_info("nonexistent_id")

        assert result.is_failure

    def test_export_jaeger_format_success(self) -> None:
        """Test export_jaeger_format success path (lines 478+)."""
        service = FlextTracingService()

        trace_result = flext_create_trace("test_trace_id", "test_operation")
        assert trace_result.success
        trace = trace_result.data

        service.start_trace(trace)
        result = service.export_jaeger_format(trace.trace_id)

        assert result.success

    def test_get_tracing_summary_success(self) -> None:
        """Test get_tracing_summary success path (lines 546+)."""
        service = FlextTracingService()

        result = service.get_tracing_summary()

        assert result.success
        summary = result.data
        assert "service_info" in summary


class TestFlextLoggingServiceComprehensive:
    """Test FlextLoggingService log_entry method - target missing lines."""

    def test_log_entry_success(self) -> None:
        """Test log_entry success path."""
        service = FlextLoggingService()

        log_result = flext_create_log_entry("INFO", "Test message")
        assert log_result.success

        result = service.log_entry(log_result.data)

        assert result.success

    def test_log_entry_with_debug_level(self) -> None:
        """Test log_entry with DEBUG level."""
        service = FlextLoggingService()

        log_result = flext_create_log_entry("DEBUG", "Debug message")
        assert log_result.success

        result = service.log_entry(log_result.data)

        assert result.success

    def test_log_entry_with_error_level(self) -> None:
        """Test log_entry with ERROR level."""
        service = FlextLoggingService()

        log_result = flext_create_log_entry("ERROR", "Error message")
        assert log_result.success

        result = service.log_entry(log_result.data)

        assert result.success

    def test_log_entry_exception_handling(self) -> None:
        """Test log_entry exception handling path."""
        service = FlextLoggingService()

        # Create mock entry that will cause exception
        mock_entry = Mock()
        # Make level property raise exception when accessed
        type(mock_entry).level = PropertyMock(side_effect=AttributeError("Mock error"))
        mock_entry.message = "Test message"
        mock_entry.context = {}

        result = service.log_entry(mock_entry)

        assert result.is_failure


class TestFlextAlertServiceComprehensive:
    """Test FlextAlertService create_alert method - target missing lines."""

    def test_create_alert_success(self) -> None:
        """Test create_alert success path."""
        service = FlextAlertService()

        alert_result = flext_create_alert("Test Alert", "HIGH", "Test message")
        assert alert_result.success

        result = service.create_alert(alert_result.data)

        assert result.success

    def test_create_alert_invalid_alert(self) -> None:
        """Test create_alert with invalid alert."""
        service = FlextAlertService()

        result = service.create_alert(None)  # type: ignore[arg-type]

        assert result.is_failure

    def test_create_alert_exception_handling(self) -> None:
        """Test create_alert exception handling."""
        service = FlextAlertService()

        # Create mock alert that will cause exception when title is accessed
        mock_alert = Mock()
        # Make title property raise exception (this is what create_alert actually accesses)
        type(mock_alert).title = PropertyMock(
            side_effect=ZeroDivisionError("Mock error")
        )
        mock_alert.severity = "HIGH"  # Set severity normally to isolate the title error

        result = service.create_alert(mock_alert)

        assert result.is_failure


class TestFlextHealthServiceComprehensive:
    """Test FlextHealthService methods - target missing lines."""

    def test_check_health_success(self) -> None:
        """Test check_health success path."""
        service = FlextHealthService()

        health_result = flext_create_health_check("test_service", "healthy")
        assert health_result.success

        result = service.check_health(health_result.data)

        assert result.success

    def test_check_health_invalid_check(self) -> None:
        """Test check_health with invalid health check."""
        service = FlextHealthService()

        result = service.check_health(None)  # type: ignore[arg-type]

        assert result.is_failure

    def test_get_overall_health_success(self) -> None:
        """Test get_overall_health success path."""
        service = FlextHealthService()

        result = service.get_overall_health()

        assert result.success
        data = result.data  # Use .data instead of .value
        assert data is not None

    def test_get_component_health_history_success(self) -> None:
        """Test get_component_health_history success path."""
        service = FlextHealthService()

        result = service.get_component_health_history("test_component")

        assert result.success

    def test_perform_system_health_check_success(self) -> None:
        """Test perform_system_health_check success path."""
        service = FlextHealthService()

        result = service.perform_system_health_check()

        assert result.success
        data = result.data
        assert data is not None


class TestServicesExceptionHandling:
    """Test exception handling across all services - target error paths."""

    def test_metrics_service_record_exception(self) -> None:
        """Test metrics service record_metric exception path."""
        service = FlextMetricsService()

        # Create metric that will cause exception when value is accessed
        mock_metric = Mock()
        mock_metric.name = "test"
        # Make value property raise exception that's handled by the service
        type(mock_metric).value = PropertyMock(
            side_effect=ValueError("Mock value error")
        )

        result = service.record_metric(mock_metric)

        assert result.is_failure

    def test_services_time_exception(self) -> None:
        """Test services handling time.time() exceptions."""
        service = FlextMetricsService()
        metric_result = flext_create_metric("test", 1.0)
        assert metric_result.success

        # Apply patch only during record_metric to avoid breaking container initialization
        with patch("flext_observability.services.time.time") as mock_time:
            mock_time.side_effect = ValueError("Time error")
            # Should handle time exception gracefully - expects failure
            result = service.record_metric(metric_result.data)
            # ValueError is captured, so it should fail gracefully
            assert result.is_failure

    def test_services_with_container_injection(self) -> None:
        """Test all services with FlextContainer dependency injection."""
        container = FlextContainer()

        # Test that all services accept container
        metrics_service = FlextMetricsService(container)
        tracing_service = FlextTracingService(container)
        logging_service = FlextLoggingService(container)
        alert_service = FlextAlertService(container)
        health_service = FlextHealthService(container)

        # Verify they all have container
        assert metrics_service.container is container
        assert tracing_service.container is container
        assert logging_service.container is container
        assert alert_service.container is container
        assert health_service.container is container
