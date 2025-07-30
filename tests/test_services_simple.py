"""Test observability services - simplified for coverage."""

from __future__ import annotations

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


class TestServicesBasic:
    """Basic tests for all services to ensure coverage."""

    def test_metrics_service(self) -> None:
        """Test metrics service basic functionality."""
        service = FlextMetricsService()
        assert service is not None

        # Test with valid metric
        metric_result = flext_create_metric("test", 1.0)
        if metric_result.is_success and metric_result.data is not None:
            record_result = service.record_metric(metric_result.data)
            assert record_result.is_success

    def test_logging_service(self) -> None:
        """Test logging service basic functionality."""
        service = FlextLoggingService()
        assert service is not None

        # Test with valid log entry
        log_result = flext_create_log_entry("test message")
        if log_result.is_success and log_result.data is not None:
            service_result = service.log_entry(log_result.data)
            assert service_result.is_success

    def test_tracing_service(self) -> None:
        """Test tracing service basic functionality."""
        service = FlextTracingService()
        assert service is not None

        # Test with valid trace
        trace_result = flext_create_trace("trace-123", "test_op")
        if trace_result.is_success and trace_result.data is not None:
            service_result = service.start_trace(trace_result.data)
            assert service_result.is_success

    def test_alert_service(self) -> None:
        """Test alert service basic functionality."""
        service = FlextAlertService()
        assert service is not None

        # Test with valid alert
        alert_result = flext_create_alert("Test", "Message")
        if alert_result.is_success and alert_result.data is not None:
            service_result = service.create_alert(alert_result.data)
            assert service_result.is_success

    def test_health_service(self) -> None:
        """Test health service basic functionality."""
        service = FlextHealthService()
        assert service is not None

        # Test overall health
        health_result = service.get_overall_health()
        assert health_result.is_success

        # Test with valid health check
        check_result = flext_create_health_check("test_component")
        if check_result.is_success and check_result.data is not None:
            service_result = service.check_health(check_result.data)
            assert service_result.is_success

    def test_services_with_container(self) -> None:
        """Test services initialization with container."""
        container = FlextContainer()

        services: list[
            FlextMetricsService
            | FlextLoggingService
            | FlextTracingService
            | FlextAlertService
            | FlextHealthService
        ] = [
            FlextMetricsService(container),
            FlextLoggingService(container),
            FlextTracingService(container),
            FlextAlertService(container),
            FlextHealthService(container),
        ]

        for service in services:
            assert service is not None
            if service.container != container:
                msg = f"Expected {container}, got {service.container}"
                raise AssertionError(msg)
