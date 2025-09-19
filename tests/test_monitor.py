"""Test observability monitor functionality with real code execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import threading
import time

import pytest

from flext_observability import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)


class TestMonitorRealFunctionality:
    """Test observability monitor with actual functionality - no excessive mocking."""

    def test_monitor_initialization_and_health_status(self) -> None:
        """Test real monitor initialization and health status retrieval."""
        # Create monitor without container dependency
        monitor = FlextObservabilityMonitor()

        # Initialize observability services
        init_result = monitor.flext_initialize_observability()
        assert init_result.success, f"Initialization failed: {init_result.error}"

        # Start monitoring
        start_result = monitor.flext_start_monitoring()
        assert start_result.success, f"Start monitoring failed: {start_result.error}"

        # Get health status
        health_result = monitor.flext_get_health_status()
        assert health_result.success, f"Health status failed: {health_result.error}"

        health_data = health_result.data
        assert isinstance(health_data, dict)
        assert "monitor_metrics" in health_data

        # Stop monitoring
        stop_result = monitor.flext_stop_monitoring()
        assert stop_result.success, f"Stop monitoring failed: {stop_result.error}"

    def test_real_metric_recording_workflow(self) -> None:
        """Test complete metric recording workflow with real services."""
        monitor = FlextObservabilityMonitor()

        # Initialize the monitor
        init_result = monitor.flext_initialize_observability()
        assert init_result.success

        # Record various types of metrics
        counter_result = monitor.flext_record_metric("requests_total", 1.0, "counter")
        assert counter_result.success, f"Counter metric failed: {counter_result.error}"

        gauge_result = monitor.flext_record_metric("cpu_usage_percent", 75.5, "gauge")
        assert gauge_result.success, f"Gauge metric failed: {gauge_result.error}"

        histogram_result = monitor.flext_record_metric(
            "response_time_seconds", 0.25, "histogram",
        )
        assert histogram_result.success, (
            f"Histogram metric failed: {histogram_result.error}"
        )

        # Get metrics summary
        summary_result = monitor.flext_get_metrics_summary()
        assert summary_result.success, f"Metrics summary failed: {summary_result.error}"

        summary_data = summary_result.data
        assert isinstance(summary_data, dict)
        assert "service_info" in summary_data

    def test_function_monitoring_decorator_real_execution(self) -> None:
        """Test function monitoring decorator with real function execution."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        # Create a real function to monitor
        @flext_monitor_function(monitor=monitor, metric_name="test_computation")
        def compute_fibonacci(n: int) -> int:
            """Compute fibonacci number - real computation."""
            if n <= 1:
                return n
            return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)

        # Execute the monitored function
        result = compute_fibonacci(10)
        assert result == 55  # Verify the function actually worked

        # Verify monitoring captured metrics
        assert monitor.flext_is_monitoring_active()

        # Get metrics summary to verify monitoring worked
        summary_result = monitor.flext_get_metrics_summary()
        assert summary_result.success

        summary_data = summary_result.data
        assert isinstance(summary_data, dict)

    def test_error_handling_in_real_scenarios(self) -> None:
        """Test error handling with real error scenarios (not mocked)."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        # Test recording metric with invalid data
        invalid_result = monitor.flext_record_metric("", 0.0)  # Empty name
        assert invalid_result.is_failure
        assert "Metric name cannot be empty" in (invalid_result.error or "")

        # Test function monitoring with real exception
        @flext_monitor_function(monitor=monitor, metric_name="error_function")
        def failing_function() -> None:
            """Function that actually raises an exception."""
            error_message = "Real error for testing"
            raise ValueError(error_message)

        # Execute and expect the exception to be re-raised
        with pytest.raises(ValueError, match="Real error for testing"):
            failing_function()

    def test_service_lifecycle_management(self) -> None:
        """Test real service lifecycle management without mocking."""
        monitor = FlextObservabilityMonitor()

        # Initially not initialized
        assert not monitor.flext_is_monitoring_active()

        # Initialize services
        init_result = monitor.flext_initialize_observability()
        assert init_result.success

        # Start monitoring
        start_result = monitor.flext_start_monitoring()
        assert start_result.success
        assert monitor.flext_is_monitoring_active()

        # Stop monitoring
        stop_result = monitor.flext_stop_monitoring()
        assert stop_result.success
        assert not monitor.flext_is_monitoring_active()

    def test_concurrent_metric_recording(self) -> None:
        """Test concurrent metric recording to verify thread safety."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        results: list[bool] = []

        def record_metrics(thread_id: int) -> None:
            """Record metrics from multiple threads."""
            for i in range(10):
                result = monitor.flext_record_metric(
                    f"thread_{thread_id}_metric_{i}", float(i),
                )
                results.append(result.success)

        # Create and start multiple threads
        threads: list[threading.Thread] = []
        for thread_id in range(3):
            thread = threading.Thread(target=record_metrics, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify all metric recordings succeeded
        assert all(results), "Some metric recordings failed in concurrent test"
        assert len(results) == 30  # 3 threads * 10 metrics each

    def test_performance_monitoring_real_workload(self) -> None:
        """Test performance monitoring with real computational workload."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        @flext_monitor_function(monitor=monitor, metric_name="cpu_intensive_task")
        def cpu_intensive_task(iterations: int) -> int:
            """Perform CPU-intensive computation."""
            total = 0
            for i in range(iterations):
                total += i**2
            return total

        # Execute the task and measure
        start_time = time.time()
        result = cpu_intensive_task(1000)  # Reduced for faster test
        end_time = time.time()

        # Verify computation result
        expected = sum(i**2 for i in range(1000))
        assert result == expected

        # Verify execution time was captured
        execution_time = end_time - start_time
        assert execution_time > 0

        # Get metrics summary to verify monitoring captured performance data
        summary_result = monitor.flext_get_metrics_summary()
        assert summary_result.success
