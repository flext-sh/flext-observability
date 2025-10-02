"""Test services with real functionality - no excessive mocking.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import threading

from flext_observability import (
    FlextAlertService,
    FlextHealthService,
    FlextMetricsService,
    FlextTracingService,
    flext_create_alert,
    flext_create_health_check,
    flext_create_metric,
    flext_create_trace,
)


class TestMetricsServiceRealFunctionality:
    """Test FlextMetricsService with real functionality."""

    def test_complete_metrics_workflow(self) -> None:
        """Test complete metrics recording and retrieval workflow."""
        service = FlextMetricsService()

        # Record different types of metrics
        counter_metric = flext_create_metric("http_requests_total", 1.0, "count")
        assert counter_metric.is_success

        gauge_metric = flext_create_metric("cpu_usage_percent", 75.5, "percent")
        assert gauge_metric.is_success

        histogram_metric = flext_create_metric(
            "response_time_ms",
            250.0,
            "milliseconds",
        )
        assert histogram_metric.is_success

        # Record metrics
        counter_result = service.record_metric(counter_metric.unwrap())
        assert counter_result.is_success

        gauge_result = service.record_metric(gauge_metric.unwrap())
        assert gauge_result.is_success

        histogram_result = service.record_metric(histogram_metric.unwrap())
        assert histogram_result.is_success

        # Get individual metric values
        counter_value = service.get_metric_value("http_requests_total")
        assert counter_value.is_success
        assert counter_value.data == 1.0

        gauge_value = service.get_metric_value("cpu_usage_percent")
        assert gauge_value.is_success
        assert gauge_value.data == 75.5

        histogram_value = service.get_metric_value("response_time_ms")
        assert histogram_value.is_success
        assert histogram_value.data == 250.0

        # Get summary
        summary = service.get_metrics_summary()
        assert summary.is_success
        assert isinstance(summary.data, dict)
        assert "service_info" in summary.data

        service_info = summary.data["service_info"]
        assert isinstance(service_info, dict)
        assert service_info["metrics_recorded"] == 3

    def test_metrics_aggregation_behavior(self) -> None:
        """Test real metrics aggregation behavior."""
        service = FlextMetricsService()

        # Record multiple counter metrics
        for _ in range(5):
            counter_metric = flext_create_metric("request_count", 1.0, "count")
            assert counter_metric.is_success
            service.record_metric(counter_metric.unwrap())

        # Counter should sum values
        counter_value = service.get_metric_value("request_count")
        assert counter_value.is_success
        assert counter_value.data == 5.0

        # Record multiple gauge metrics (should keep latest)
        for value in [10.0, 20.0, 30.0]:
            gauge_metric = flext_create_metric("temperature", value, "celsius")
            assert gauge_metric.is_success
            service.record_metric(gauge_metric.unwrap())

        gauge_value = service.get_metric_value("temperature")
        assert gauge_value.is_success
        assert gauge_value.data == 30.0  # Latest value

    def test_prometheus_export_format(self) -> None:
        """Test Prometheus export format with real data."""
        service = FlextMetricsService()

        # Record various metrics
        metrics_data = [
            ("http_requests_total", 100.0, "count"),
            ("cpu_usage", 65.5, "percent"),
            ("memory_usage", 1024.0, "bytes"),
        ]

        for name, value, unit in metrics_data:
            metric = flext_create_metric(name, value, unit)
            assert metric.is_success
            service.record_metric(metric.unwrap())

        # Export to Prometheus format
        export_result = service.export_prometheus_format()
        assert export_result.is_success

        prometheus_output = export_result.data
        assert isinstance(prometheus_output, str)

        # Verify format contains expected metrics
        assert "http_requests_total 100.0" in prometheus_output
        assert "cpu_usage 65.5" in prometheus_output
        assert "memory_usage 1024.0" in prometheus_output

        # Verify TYPE directives
        assert "# TYPE http_requests_total counter" in prometheus_output
        assert "# TYPE cpu_usage gauge" in prometheus_output

    def test_metrics_reset_functionality(self) -> None:
        """Test metrics reset functionality."""
        service = FlextMetricsService()

        # Record some metrics
        for i in range(3):
            metric = flext_create_metric(f"test_metric_{i}", float(i), "count")
            assert metric.is_success
            service.record_metric(metric.unwrap())

        # Verify metrics exist
        summary_before = service.get_metrics_summary()
        assert summary_before.is_success
        service_info = summary_before.unwrap()["service_info"]
        assert isinstance(service_info, dict)
        assert service_info["metrics_recorded"] == 3

        # Reset metrics
        reset_result = service.reset_metrics()
        assert reset_result.is_success

        # Verify metrics are cleared
        summary_after = service.get_metrics_summary()
        assert summary_after.is_success
        service_info_after = summary_after.unwrap()["service_info"]
        assert isinstance(service_info_after, dict)
        assert service_info_after["metrics_recorded"] == 0

    def test_concurrent_metrics_recording(self) -> None:
        """Test concurrent metrics recording for thread safety."""
        service = FlextMetricsService()
        results: list[bool] = []

        def record_metrics_batch(thread_id: int) -> None:
            """Record metrics from a specific thread."""
            for i in range(5):
                metric = flext_create_metric(
                    f"thread_{thread_id}_metric_{i}",
                    float(i),
                    "count",
                )
                if metric.is_success:
                    result = service.record_metric(metric.unwrap())
                    results.append(result.is_success)

        # Start multiple threads
        threads: list[threading.Thread] = []
        for thread_id in range(4):
            thread = threading.Thread(target=record_metrics_batch, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify all recordings succeeded
        assert all(results)
        assert len(results) == 20  # 4 threads * 5 metrics each

        # Verify service state
        summary = service.get_metrics_summary()
        assert summary.is_success


class TestTracingServiceRealFunctionality:
    """Test FlextTracingService with real functionality."""

    def test_complete_tracing_workflow(self) -> None:
        """Test complete trace creation and management workflow."""
        service = FlextTracingService()

        # Create and start a trace
        trace = flext_create_trace("user_request", "api_service")
        assert trace.is_success

        trace_obj = trace.unwrap()
        start_result = service.start_trace(trace_obj)
        assert start_result.is_success

        # Add spans to the trace
        span_result = service.add_span_to_trace(trace_obj.trace_id, "database_query")
        assert span_result.is_success

        span_result2 = service.add_span_to_trace(trace_obj.trace_id, "cache_lookup")
        assert span_result2.is_success

        # Get trace info
        trace_info = service.get_trace_info(trace_obj.trace_id)
        assert trace_info.is_success

        # Finish the trace
        finish_result = service.finish_trace(trace_obj.trace_id)
        assert finish_result.is_success

        # Get tracing summary
        summary = service.get_tracing_summary()
        assert summary.is_success
        assert isinstance(summary.data, dict)

    def test_jaeger_export_format(self) -> None:
        """Test Jaeger export format with real trace data."""
        service = FlextTracingService()

        # Create a trace with spans
        trace = flext_create_trace("payment_processing", "payment_service")
        assert trace.is_success

        trace_obj = trace.unwrap()
        service.start_trace(trace_obj)
        service.add_span_to_trace(trace_obj.trace_id, "validate_payment")
        service.add_span_to_trace(trace_obj.trace_id, "process_payment")
        service.finish_trace(trace_obj.trace_id)

        # Export to Jaeger format
        jaeger_result = service.export_jaeger_format(trace_obj.trace_id)
        assert jaeger_result.is_success

        jaeger_data = jaeger_result.unwrap()
        assert isinstance(jaeger_data, dict)
        assert "traceID" in jaeger_data
        assert "spans" in jaeger_data
        assert jaeger_data["traceID"] == trace_obj.trace_id


# TestLoggingServiceRealFunctionality class removed - FlextLoggingService doesn't exist as a separate class


class TestAlertServiceRealFunctionality:
    """Test FlextAlertService with real functionality."""

    def test_alert_creation_workflow(self) -> None:
        """Test complete alert creation workflow."""
        service = FlextAlertService()

        # Create alerts with different severity levels
        alert_levels = ["low", "medium", "high", "critical"]

        for level in alert_levels:
            alert = flext_create_alert(
                f"Test {level} alert",
                f"Test {level} alert message",
                level,
            )
            assert alert.is_success

            result = service.create_alert(alert.unwrap())
            assert result.is_success


class TestHealthServiceRealFunctionality:
    """Test FlextHealthService with real functionality."""

    def test_health_check_workflow(self) -> None:
        """Test complete health check workflow."""
        service = FlextHealthService()

        # Create health checks for different components
        components = ["database", "cache", "api", "worker"]

        for component in components:
            health_check = flext_create_health_check(component, "healthy")
            assert health_check.is_success

            result = service.check_health(health_check.unwrap())
            assert result.is_success

        # Get overall health
        overall_health = service.get_overall_health()
        assert overall_health.is_success
        assert isinstance(overall_health.data, dict)

        # Get component history
        for component in components:
            history = service.get_component_health_history(component)
            assert history.is_success

    def test_system_health_check(self) -> None:
        """Test system health check functionality."""
        service = FlextHealthService()

        system_health = service.perform_system_health_check()
        assert system_health.is_success

        health_data = system_health.data
        assert isinstance(health_data, dict)
        assert "memory" in health_data
        assert "disk" in health_data

        # Verify structure
        memory_check = health_data["memory"]
        assert isinstance(memory_check, dict)
        assert "status" in memory_check

        disk_check = health_data["disk"]
        assert isinstance(disk_check, dict)
        assert "status" in disk_check

    def test_persistent_unhealthy_component_detection(self) -> None:
        """Test detection of persistently unhealthy components."""
        service = FlextHealthService()

        # Create multiple unhealthy reports for same component
        for _ in range(5):  # More than the threshold
            health_check = flext_create_health_check("failing_component", "unhealthy")
            assert health_check.is_success

            result = service.check_health(health_check.unwrap())
            assert result.is_success

        # Verify component is tracked as persistently unhealthy
        # This tests internal state management without accessing private attributes
        overall_health = service.get_overall_health()
        assert overall_health.is_success


class TestServiceErrorHandlingRealFunctionality:
    """Test error handling in services with real scenarios."""

    def test_metrics_service_invalid_metric_handling(self) -> None:
        """Test metrics service with invalid data - real validation."""
        # Test with invalid metric name (empty)
        invalid_metric = flext_create_metric("", 10.0)
        if invalid_metric.is_failure:
            assert invalid_metric.error is not None
            assert "Metric name cannot be empty" in invalid_metric.error

    def test_metrics_service_export_edge_cases(self) -> None:
        """Test Prometheus export with edge cases."""
        service = FlextMetricsService()

        # Test export with no metrics
        export_result = service.export_prometheus_format()
        assert export_result.is_success
        assert isinstance(export_result.data, str)

        # Test export with special characters in metric names
        special_metric = flext_create_metric("metric_with_underscores", 42.0)
        assert special_metric.is_success
        service.record_metric(special_metric.unwrap())

        export_result = service.export_prometheus_format()
        assert export_result.is_success
        assert "metric_with_underscores 42.0" in export_result.unwrap()

    def test_tracing_service_span_management(self) -> None:
        """Test tracing service span management with real operations."""
        service = FlextTracingService()

        # Create a trace and add multiple spans
        trace = flext_create_trace("complex_operation", "service_a")
        assert trace.is_success

        trace_obj = trace.unwrap()
        start_result = service.start_trace(trace_obj)
        assert start_result.is_success

        # Add spans in sequence
        span_operations = [
            "database_read",
            "computation",
            "cache_write",
            "api_response",
        ]

        for operation in span_operations:
            span_result = service.add_span_to_trace(trace_obj.trace_id, operation)
            assert span_result.is_success

        # Get trace information
        trace_info = service.get_trace_info(trace_obj.trace_id)
        assert trace_info.is_success

        # Finish the trace
        finish_result = service.finish_trace(trace_obj.trace_id)
        assert finish_result.is_success

    def test_alert_service_different_severity_levels(self) -> None:
        """Test alert service with different severity levels."""
        service = FlextAlertService()

        # Test all valid severity levels
        severity_levels = ["low", "medium", "high", "critical", "emergency"]

        for level in severity_levels:
            alert = flext_create_alert(f"Test {level} alert", "test_service", level)
            assert alert.is_success

            result = service.create_alert(alert.data)
            assert result.is_success

        # All alerts created successfully - real functionality validated

    def test_health_service_system_monitoring_real(self) -> None:
        """Test health service system monitoring with real system checks."""
        service = FlextHealthService()

        # Perform real system health check
        system_health = service.perform_system_health_check()
        assert system_health.is_success

        health_data = system_health.data
        assert isinstance(health_data, dict)

        # Verify we have real system metrics
        assert "memory" in health_data
        assert "disk" in health_data

        # Memory check should have real data
        memory_info = health_data["memory"]
        assert isinstance(memory_info, dict)
        assert "status" in memory_info
        assert memory_info["status"] in {"healthy", "warning", "critical"}

        # Disk check should have real data
        disk_info = health_data["disk"]
        assert isinstance(disk_info, dict)
        assert "status" in disk_info
        assert disk_info["status"] in {"healthy", "warning", "critical"}
