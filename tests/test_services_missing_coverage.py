"""Test services.py missing coverage paths to improve overall coverage."""

from unittest.mock import patch

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextTrace,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


class TestServicesMissingCoverage:
    """Test missing coverage paths in services.py."""

    def test_metrics_service_exception_paths(self) -> None:
        """Test exception handling paths in metrics service."""
        service = FlextMetricsService()

        # Test export_prometheus_format exception path
        with patch.object(service, "_metrics_lock") as mock_lock:
            mock_lock.__enter__.side_effect = ValueError("Lock error")
            result = service.export_prometheus_format()
            assert result.is_failure
            assert "Failed to export Prometheus format" in result.error

        # Test reset_metrics exception path
        with patch.object(service, "_metrics_lock") as mock_lock:
            mock_lock.__enter__.side_effect = AttributeError("Lock error")
            result = service.reset_metrics()
            assert result.is_failure
            assert "Failed to reset metrics" in result.error

    def test_tracing_service_hierarchy_with_parent(self) -> None:
        """Test tracing service with parent trace hierarchy."""
        service = FlextTracingService()

        # Start parent trace first
        parent_trace = FlextTrace(
            id="parent_id",
            trace_id="parent_trace_123",
            operation="parent_operation",
            span_id="parent_span",
        )
        parent_result = service.start_trace(parent_trace)
        assert parent_result.success

        # Create child trace with span_attributes containing parent info
        child_trace = FlextTrace(
            id="child_id",
            trace_id="child_trace_456",
            operation="child_operation",
            span_id="child_span",
            span_attributes={"parent_trace_id": "parent_trace_123"},  # Use span_attributes instead
        )

        child_result = service.start_trace(child_trace)
        assert child_result.success

        # Test that trace was created successfully (hierarchy logic would need to be in start_trace)
        trace_info = service.get_trace_info("child_trace_456")
        assert trace_info.success

    def test_tracing_service_add_span_exception_path(self) -> None:
        """Test add_span_to_trace exception handling."""
        service = FlextTracingService()

        # Test with invalid span_attributes causing exception
        with patch.object(service, "_traces_lock") as mock_lock:
            mock_lock.__enter__.side_effect = KeyError("Lock error")
            result = service.add_span_to_trace("nonexistent", "test_span")
            assert result.is_failure
            assert "Failed to add span to trace" in result.error

    def test_tracing_service_finish_trace_exception_path(self) -> None:
        """Test finish_trace exception handling."""
        service = FlextTracingService()

        with patch.object(service, "_traces_lock") as mock_lock:
            mock_lock.__enter__.side_effect = ArithmeticError("Calculation error")
            result = service.finish_trace("test_trace")
            assert result.is_failure
            assert "Failed to finish trace" in result.error

    def test_tracing_service_get_trace_info_exception_path(self) -> None:
        """Test get_trace_info exception handling."""
        service = FlextTracingService()

        with patch.object(service, "_traces_lock") as mock_lock:
            mock_lock.__enter__.side_effect = TypeError("Type error")
            result = service.get_trace_info("test_trace")
            assert result.is_failure
            assert "Failed to get trace info" in result.error

    def test_tracing_service_export_jaeger_exception_path(self) -> None:
        """Test export_jaeger_format exception handling."""
        service = FlextTracingService()

        with patch.object(service, "get_trace_info") as mock_get_trace:
            mock_get_trace.side_effect = ValueError("Trace error")
            result = service.export_jaeger_format("test_trace")
            assert result.is_failure
            assert "Failed to export Jaeger format" in result.error

    def test_tracing_service_summary_exception_path(self) -> None:
        """Test get_tracing_summary exception handling."""
        service = FlextTracingService()

        with patch.object(service, "_traces_lock") as mock_lock:
            mock_lock.__enter__.side_effect = ArithmeticError("Math error")
            result = service.get_tracing_summary()
            assert result.is_failure
            assert "Failed to generate tracing summary" in result.error

    def test_health_service_extract_health_failure_path(self) -> None:
        """Test _extract_actual_health with failure result."""
        service = FlextHealthService()

        # Test with FlextResult failure
        from flext_core import FlextResult
        failure_result = FlextResult.fail("Health check creation failed")

        result = service._extract_actual_health(failure_result)
        assert result.is_failure
        assert "Health check creation failed" in result.error

    def test_health_service_extract_health_none_data(self) -> None:
        """Test _extract_actual_health with None data."""
        service = FlextHealthService()

        from flext_core import FlextResult
        none_result = FlextResult.ok(None)

        result = service._extract_actual_health(none_result)
        assert result.is_failure
        assert "Health check data is None" in result.error

    def test_health_service_persistent_unhealthy_warning(self) -> None:
        """Test persistent unhealthy component warning."""
        service = FlextHealthService()

        # Create unhealthy health check
        unhealthy_check = FlextHealthCheck(
            id="test_id",
            component="failing_component",
            status="unhealthy",
            message="Component failing",
        )

        # Record multiple unhealthy checks to trigger warning
        for _ in range(4):  # More than _unhealthy_threshold (3)
            result = service.check_health(unhealthy_check)
            assert result.success

        # Verify component is in unhealthy set
        assert "failing_component" in service._unhealthy_components

    def test_health_service_check_health_exception_path(self) -> None:
        """Test check_health exception handling."""
        service = FlextHealthService()

        with patch.object(service, "_extract_actual_health") as mock_extract:
            mock_extract.side_effect = AttributeError("Extract error")

            health_check = FlextHealthCheck(
                id="test_id",
                component="test_component",
                status="healthy",
            )
            result = service.check_health(health_check)
            assert result.is_failure
            assert "Failed to check health" in result.error

    def test_health_service_check_health_with_flext_result_success(self) -> None:
        """Test check_health with successful FlextResult input."""
        service = FlextHealthService()

        health_check = FlextHealthCheck(
            id="test_id",
            component="test_component",
            status="healthy",
        )

        from flext_core import FlextResult
        health_result = FlextResult.ok(health_check)

        result = service.check_health(health_result)
        assert result.success
        assert result.data.component == "test_component"

    def test_health_service_check_health_with_flext_result_failure(self) -> None:
        """Test check_health with failed FlextResult input."""
        service = FlextHealthService()

        from flext_core import FlextResult
        health_result = FlextResult.fail("Health check failed")

        result = service.check_health(health_result)
        assert result.is_failure
        assert "Health check failed" in result.error

    def test_health_service_check_health_error_handling_attribute_error(self) -> None:
        """Test check_health error handling with safe attribute access."""
        service = FlextHealthService()

        # Create a mock object that will cause AttributeError during processing
        with patch.object(service, "_extract_actual_health") as mock_extract:
            mock_extract.side_effect = AttributeError("Attribute error")

            # Use a regular health check that would normally work
            health_check = FlextHealthCheck(
                id="test_id",
                component="test_component",
                status="healthy",
            )

            result = service.check_health(health_check)
            assert result.is_failure
            assert "Failed to check health" in result.error

    def test_health_service_overall_health_exception_path(self) -> None:
        """Test get_overall_health exception handling."""
        service = FlextHealthService()

        with patch.object(service, "_health_lock") as mock_lock:
            mock_lock.__enter__.side_effect = ArithmeticError("Math error")
            result = service.get_overall_health()
            assert result.is_failure
            assert "Failed to get overall health" in result.error

    def test_health_service_component_history_exception_path(self) -> None:
        """Test get_component_health_history exception handling."""
        service = FlextHealthService()

        with patch.object(service, "_health_lock") as mock_lock:
            mock_lock.__enter__.side_effect = KeyError("Key error")
            result = service.get_component_health_history("test_component")
            assert result.is_failure
            assert "Failed to get health history" in result.error

    def test_health_service_system_health_check_disk_failure(self) -> None:
        """Test perform_system_health_check with disk check failure."""
        service = FlextHealthService()

        with patch("shutil.disk_usage") as mock_disk_usage:
            mock_disk_usage.side_effect = OSError("Disk error")
            result = service.perform_system_health_check()
            assert result.success

            # Should handle disk error gracefully
            system_checks = result.data
            assert system_checks["disk"]["status"] == "unknown"
            assert "disk check failed" in system_checks["disk"]["error"]

    def test_health_service_system_health_check_exception_path(self) -> None:
        """Test perform_system_health_check exception handling."""
        service = FlextHealthService()

        with patch("psutil.virtual_memory") as mock_memory:
            mock_memory.side_effect = AttributeError("Memory error")
            result = service.perform_system_health_check()
            assert result.is_failure
            assert "System health check failed" in result.error

    def test_alert_service_create_alert_exception_path(self) -> None:
        """Test create_alert exception handling."""
        service = FlextAlertService()

        alert = FlextAlert(
            id="test_id",
            title="Test Alert",
            message="Test message",
        )

        with patch.object(service, "logger") as mock_logger:
            mock_logger.warning.side_effect = ArithmeticError("Log error")
            result = service.create_alert(alert)
            assert result.is_failure
            assert "Failed to create alert" in result.error

    def test_logging_service_exception_path(self) -> None:
        """Test log_entry exception handling."""
        service = FlextLoggingService()

        log_entry = FlextLogEntry(
            id="test_id",
            message="Test message",
            level="info",
        )

        with patch.object(service, "logger") as mock_logger:
            mock_logger.info.side_effect = AttributeError("Logger error")
            result = service.log_entry(log_entry)
            assert result.is_failure
            assert "Failed to log entry" in result.error
