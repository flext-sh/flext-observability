"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

import pytest
from flext_core import FlextContainer, p

from flext_observability import (
    get_global_factory,
    reset_global_factory,
)
from flext_observability._core import FlextObservabilityMasterFactory


class TestFlextObservabilityMasterFactoryReal:
    """Real functionality tests for master factory without excessive mocking."""

    def test_factory_initialization_and_container_real(self) -> None:
        """Test factory initialization with real container integration."""
        container = FlextContainer()
        factory = FlextObservabilityMasterFactory(container)
        assert factory.container is container
        factory_default = FlextObservabilityMasterFactory()
        assert factory_default.container is not None
        assert isinstance(factory_default.container, p.Container)

    def test_metric_creation_real_functionality(self) -> None:
        """Test metric creation with actual factory functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.create_metric("test_metric", 42.5, "gauge")
        assert metric_result.is_success, (
            f"Metric creation failed: {metric_result.error}"
        )
        assert metric_result.value is not None
        assert metric_result.value.name == "test_metric"
        assert metric_result.value.value == pytest.approx(42.5)
        assert metric_result.value.unit == "gauge"

    def test_metric_creation_with_validation_real(self) -> None:
        """Test metric creation with real validation logic."""
        factory = FlextObservabilityMasterFactory()
        invalid_result = factory.create_metric("", 10.0)
        assert invalid_result.is_failure
        assert invalid_result.error is not None
        assert "must be non-empty string" in invalid_result.error

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        log_result = factory.create_log_entry("Test log message", "info")
        assert log_result.is_success, f"Log creation failed: {log_result.error}"
        assert log_result.value is not None
        assert log_result.value.message == "Test log message"
        assert log_result.value.level == "info"

    def test_log_creation_validation_real(self) -> None:
        """Test log creation with real validation."""
        factory = FlextObservabilityMasterFactory()
        custom_level_result = factory.create_log_entry("Test", "INVALID_LEVEL")
        if custom_level_result.is_failure:
            assert custom_level_result.error is not None
        else:
            assert custom_level_result.value.level in {"INVALID_LEVEL", "info"}

    def test_alert_creation_real_functionality(self) -> None:
        """Test alert creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        alert_result = factory.create_alert(
            "Critical error detected", "monitoring", "critical"
        )
        assert alert_result.is_success, f"Alert creation failed: {alert_result.error}"
        assert alert_result.value is not None
        assert alert_result.value.message == "Critical error detected"
        assert alert_result.value.title == "Alert: monitoring"
        assert alert_result.value.severity == "critical"

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        trace_result = factory.create_trace("user_authentication", "auth_service")
        assert trace_result.is_success, f"Trace creation failed: {trace_result.error}"
        assert trace_result.value is not None
        assert trace_result.value.name == "user_authentication"
        assert trace_result.value.trace_id is not None

    def test_health_check_creation_real_functionality(self) -> None:
        """Test health check creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        health_result = factory.create_health_check("database", "healthy")
        assert health_result.is_success, (
            f"Health check creation failed: {health_result.error}"
        )
        assert health_result.value is not None
        assert health_result.value.component == "database"
        assert health_result.value.status == "healthy"

    def test_factory_shorthand_methods_real(self) -> None:
        """Test factory shorthand methods with real functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.metric("cpu_usage", 85.2)
        assert metric_result.is_success
        metric = metric_result.value
        assert hasattr(metric, "name")
        assert metric.name == "cpu_usage"
        assert hasattr(metric, "value")
        assert metric.value == pytest.approx(85.2)
        log_result = factory.log("System started")
        assert log_result.is_success
        log_entry = log_result.value
        assert hasattr(log_entry, "message")
        assert log_entry.message == "System started"
        alert_result = factory.alert("High memory usage", "monitoring")
        assert alert_result.is_success
        alert = alert_result.value
        assert hasattr(alert, "title")
        assert alert.title == "High memory usage"
        assert alert.message == "monitoring"
        trace_result = factory.trace("trace-123", "api_request")
        assert trace_result.is_success
        trace = trace_result.value
        assert hasattr(trace, "name")
        assert trace.name == "api_request"
        assert trace.trace_id == "trace-123"

    def test_global_factory_real_functionality(self) -> None:
        """Test global factory with real functionality."""
        reset_global_factory()
        factory1 = get_global_factory()
        assert factory1 is not None
        factory2 = get_global_factory()
        assert factory2 is not None
        reset_global_factory()
        factory3 = get_global_factory()
        assert factory3 is not None

    def test_factory_error_handling_real(self) -> None:
        """Test factory error handling with real scenarios."""
        factory = FlextObservabilityMasterFactory()
        test_cases = [
            ("create_metric", ("", 10.0), "must be non-empty string"),
            ("create_log_entry", ("",), "Log message cannot be empty"),
            ("create_trace", ("", "service"), "must be non-empty string"),
            ("create_health_check", ("",), "Component name cannot be empty"),
        ]
        for method_name, args, expected_error in test_cases:
            method = getattr(factory, method_name)
            result = method(*args)
            assert result.is_failure, (
                f"Method {method_name} should have failed with args {args}"
            )
            assert result.error is not None
            assert expected_error in result.error

    def test_factory_integration_with_services_real(self) -> None:
        """Test factory integration with real service workflows."""
        factory = FlextObservabilityMasterFactory()
        metric = factory.create_metric("request_count", 100, "counter")
        log = factory.create_log_entry("Request processed", "info")
        alert = factory.create_alert("High request count", "monitoring", "medium")
        trace = factory.create_trace("process_request", "api_service")
        health = factory.create_health_check("api_service", "healthy")
        results = [metric, log, alert, trace, health]
        for i, result in enumerate(results):
            assert hasattr(result, "is_success"), (
                f"Entity {i} missing is_success property"
            )
            assert result.is_success, (
                f"Entity {i} creation failed: {getattr(result, 'error', 'Unknown error')}"
            )
        timestamp_fields = ("timestamp", "created_at", "start_time")
        for result in results:
            entity = result.value if hasattr(result, "unwrap") else result
            has_timestamp = any(hasattr(entity, f) for f in timestamp_fields)
            assert has_timestamp, (
                f"Entity {type(entity).__name__} has no timestamp field"
            )
            timestamp_attr = None
            for field in timestamp_fields:
                timestamp_attr = getattr(entity, field, None)
                if timestamp_attr is not None:
                    break
            if timestamp_attr:
                if hasattr(timestamp_attr, "root"):
                    assert isinstance(timestamp_attr.root, datetime)
                else:
                    assert isinstance(timestamp_attr, datetime)
