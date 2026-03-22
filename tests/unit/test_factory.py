"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextContainer

from flext_observability import (
    get_global_factory,
    reset_global_factory,
)
from flext_observability._core import FlextObservabilityMasterFactory
from tests.utilities import u


class TestFlextObservabilityMasterFactoryReal:
    """Real functionality tests for master factory without excessive mocking."""

    def test_factory_initialization_and_container_real(self) -> None:
        """Test factory initialization with real container integration."""
        container = FlextContainer()
        factory = FlextObservabilityMasterFactory(container)
        u.Tests.Matchers.that(factory.container is container, eq=True)
        factory_default = FlextObservabilityMasterFactory()
        u.Tests.Matchers.that(hasattr(factory_default, "container"), eq=True)

    def test_metric_creation_real_functionality(self) -> None:
        """Test metric creation with actual factory functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.create_metric("test_metric", 42.5, "gauge")
        u.Tests.Matchers.that(metric_result.is_success, eq=True)
        u.Tests.Matchers.that(metric_result.value.name == "test_metric", eq=True)
        u.Tests.Matchers.that(abs(metric_result.value.value - 42.5) < 1e-9, eq=True)
        u.Tests.Matchers.that(metric_result.value.unit == "gauge", eq=True)

    def test_metric_creation_with_validation_real(self) -> None:
        """Test metric creation with real validation logic."""
        factory = FlextObservabilityMasterFactory()
        invalid_result = factory.create_metric("", 10.0)
        u.Tests.Matchers.that(invalid_result.is_failure, eq=True)
        u.Tests.Matchers.that(invalid_result.error is not None, eq=True)
        assert invalid_result.error is not None
        u.Tests.Matchers.that(
            "must be non-empty string" in invalid_result.error, eq=True
        )

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        log_result = factory.create_log_entry("Test log message", "info")
        u.Tests.Matchers.that(log_result.is_success, eq=True)
        u.Tests.Matchers.that(log_result.value.message == "Test log message", eq=True)
        u.Tests.Matchers.that(log_result.value.level == "info", eq=True)

    def test_log_creation_validation_real(self) -> None:
        """Test log creation with real validation."""
        factory = FlextObservabilityMasterFactory()
        custom_level_result = factory.create_log_entry("Test", "INVALID_LEVEL")
        if custom_level_result.is_failure:
            u.Tests.Matchers.that(custom_level_result.error is not None, eq=True)
        else:
            u.Tests.Matchers.that(
                custom_level_result.value.level in {"INVALID_LEVEL", "info"}, eq=True
            )

    def test_alert_creation_real_functionality(self) -> None:
        """Test alert creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        alert_result = factory.create_alert(
            "Critical error detected", "monitoring", "critical"
        )
        u.Tests.Matchers.that(alert_result.is_success, eq=True)
        u.Tests.Matchers.that(
            alert_result.value.message == "Critical error detected", eq=True
        )
        u.Tests.Matchers.that(alert_result.value.title == "Alert: monitoring", eq=True)
        u.Tests.Matchers.that(alert_result.value.severity == "critical", eq=True)

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        trace_result = factory.create_trace("user_authentication", "auth_service")
        u.Tests.Matchers.that(trace_result.is_success, eq=True)
        u.Tests.Matchers.that(trace_result.value.name == "user_authentication", eq=True)
        u.Tests.Matchers.that(trace_result.value.trace_id != "", eq=True)

    def test_health_check_creation_real_functionality(self) -> None:
        """Test health check creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        health_result = factory.create_health_check("database", "healthy")
        u.Tests.Matchers.that(health_result.is_success, eq=True)
        u.Tests.Matchers.that(health_result.value.component == "database", eq=True)
        u.Tests.Matchers.that(health_result.value.status == "healthy", eq=True)

    def test_factory_shorthand_methods_real(self) -> None:
        """Test factory shorthand methods with real functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.metric("cpu_usage", 85.2)
        u.Tests.Matchers.that(metric_result.is_success, eq=True)
        metric = metric_result.value
        u.Tests.Matchers.that(hasattr(metric, "name"), eq=True)
        u.Tests.Matchers.that(metric.name == "cpu_usage", eq=True)
        u.Tests.Matchers.that(hasattr(metric, "value"), eq=True)
        u.Tests.Matchers.that(abs(metric.value - 85.2) < 1e-9, eq=True)
        log_result = factory.log("System started")
        u.Tests.Matchers.that(log_result.is_success, eq=True)
        log_entry = log_result.value
        u.Tests.Matchers.that(hasattr(log_entry, "message"), eq=True)
        u.Tests.Matchers.that(log_entry.message == "System started", eq=True)
        alert_result = factory.alert("High memory usage", "monitoring")
        u.Tests.Matchers.that(alert_result.is_success, eq=True)
        alert = alert_result.value
        u.Tests.Matchers.that(hasattr(alert, "title"), eq=True)
        u.Tests.Matchers.that(alert.title == "High memory usage", eq=True)
        u.Tests.Matchers.that(alert.message == "monitoring", eq=True)
        trace_result = factory.trace("trace-123", "api_request")
        u.Tests.Matchers.that(trace_result.is_success, eq=True)
        trace = trace_result.value
        u.Tests.Matchers.that(hasattr(trace, "name"), eq=True)
        u.Tests.Matchers.that(trace.name == "api_request", eq=True)
        u.Tests.Matchers.that(trace.trace_id == "trace-123", eq=True)

    def test_global_factory_real_functionality(self) -> None:
        """Test global factory with real functionality."""
        reset_global_factory()
        factory1 = get_global_factory()
        u.Tests.Matchers.that(hasattr(factory1, "get_status"), eq=True)
        factory2 = get_global_factory()
        u.Tests.Matchers.that(hasattr(factory2, "get_status"), eq=True)
        reset_global_factory()
        factory3 = get_global_factory()
        u.Tests.Matchers.that(hasattr(factory3, "get_status"), eq=True)

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
            u.Tests.Matchers.that(result.is_failure, eq=True)
            u.Tests.Matchers.that(result.error is not None, eq=True)
            u.Tests.Matchers.that(expected_error in result.error, eq=True)

    def test_factory_integration_with_services_real(self) -> None:
        """Test factory integration with real service workflows."""
        factory = FlextObservabilityMasterFactory()
        metric = factory.create_metric("request_count", 100, "counter")
        log = factory.create_log_entry("Request processed", "info")
        alert = factory.create_alert("High request count", "monitoring", "medium")
        trace = factory.create_trace("process_request", "api_service")
        health = factory.create_health_check("api_service", "healthy")
        results = [metric, log, alert, trace, health]
        for result in results:
            u.Tests.Matchers.that(hasattr(result, "is_success"), eq=True)
            u.Tests.Matchers.that(result.is_success, eq=True)
        timestamp_fields = ("timestamp", "created_at", "start_time")
        for result in results:
            entity = result.value if hasattr(result, "unwrap") else result
            has_timestamp = any(hasattr(entity, f) for f in timestamp_fields)
            u.Tests.Matchers.that(has_timestamp, eq=True)
            timestamp_attr = None
            for field in timestamp_fields:
                timestamp_attr = getattr(entity, field, None)
                if timestamp_attr is not None:
                    break
            if timestamp_attr:
                if hasattr(timestamp_attr, "root"):
                    u.Tests.Matchers.that(
                        isinstance(timestamp_attr.root, datetime), eq=True
                    )
                else:
                    u.Tests.Matchers.that(isinstance(timestamp_attr, datetime), eq=True)
