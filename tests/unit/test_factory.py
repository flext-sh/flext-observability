"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

from flext_tests import tm

from flext_core import FlextContainer
from flext_observability import FlextObservability

global_factory = FlextObservability.global_factory
clear_global_factory = FlextObservability.clear_global_factory


class TestsFlextObservabilityFactory:
    """Real functionality tests for master factory without excessive mocking."""

    def test_factory_initialization_and_container_real(self) -> None:
        """Test factory initialization with real container integration."""
        container = FlextContainer()
        factory = FlextObservability.FlextObservabilityMasterFactory(container)
        tm.that(factory.container is container, eq=True)
        FlextObservability.FlextObservabilityMasterFactory()

    def test_metric_creation_real_functionality(self) -> None:
        """Test metric creation with actual factory functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        metric_result = factory.create_metric("test_metric", 42.5, "gauge")
        tm.that(metric_result.success, eq=True)
        tm.that(metric_result.value.name, eq="test_metric")
        tm.that(abs(metric_result.value.value - 42.5), lt=1e-9)
        tm.that(metric_result.value.unit, eq="gauge")

    def test_metric_creation_with_validation_real(self) -> None:
        """Test metric creation with real validation logic."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        invalid_result = factory.create_metric("", 10.0)
        tm.that(invalid_result.failure, eq=True)
        tm.that(invalid_result.error, none=False)
        assert invalid_result.error is not None
        tm.that(invalid_result.error, has="must be non-empty string")

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        log_result = factory.create_log_entry("Test log message", "info")
        tm.that(log_result.success, eq=True)
        tm.that(log_result.value.message, eq="Test log message")
        tm.that(log_result.value.level, eq="info")

    def test_log_creation_validation_real(self) -> None:
        """Test log creation with real validation."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        custom_level_result = factory.create_log_entry("Test", "INVALID_LEVEL")
        if custom_level_result.failure:
            tm.that(custom_level_result.error, none=False)
        else:
            tm.that({"INVALID_LEVEL", "info"}, has=custom_level_result.value.level)

    def test_alert_creation_real_functionality(self) -> None:
        """Test alert creation with real functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        alert_result = factory.create_alert(
            "Critical error detected",
            "monitoring",
            "critical",
        )
        tm.that(alert_result.success, eq=True)
        tm.that(alert_result.value.message, eq="Critical error detected")
        tm.that(alert_result.value.title, eq="Alert: monitoring")
        tm.that(alert_result.value.severity, eq="critical")

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        trace_result = factory.create_trace("user_authentication", "auth_service")
        tm.that(trace_result.success, eq=True)
        tm.that(trace_result.value.name, eq="user_authentication")
        tm.that(trace_result.value.trace_id, ne="")

    def test_health_check_creation_real_functionality(self) -> None:
        """Test health check creation with real functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        health_result = factory.create_health_check("database", "healthy")
        tm.that(health_result.success, eq=True)
        tm.that(health_result.value.component, eq="database")
        tm.that(health_result.value.status, eq="healthy")

    def test_factory_shorthand_methods_real(self) -> None:
        """Test factory shorthand methods with real functionality."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        metric_result = factory.metric("cpu_usage", 85.2)
        tm.that(metric_result.success, eq=True)
        metric = metric_result.value
        tm.that(metric.name, eq="cpu_usage")
        tm.that(abs(metric.value - 85.2), lt=1e-9)
        log_result = factory.log("System started")
        tm.that(log_result.success, eq=True)
        log_entry = log_result.value
        tm.that(log_entry.message, eq="System started")
        alert_result = factory.alert("High memory usage", "monitoring")
        tm.that(alert_result.success, eq=True)
        alert = alert_result.value
        tm.that(alert.title, eq="High memory usage")
        tm.that(alert.message, eq="monitoring")
        trace_result = factory.trace("trace-123", "api_request")
        tm.that(trace_result.success, eq=True)
        trace = trace_result.value
        tm.that(trace.name, eq="api_request")
        tm.that(trace.trace_id, eq="trace-123")

    def test_global_factory_real_functionality(self) -> None:
        """Test global factory with real functionality."""
        clear_global_factory()
        global_factory()
        global_factory()
        clear_global_factory()
        global_factory()

    def test_factory_error_handling_real(self) -> None:
        """Test factory error handling with real scenarios."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        test_cases = [
            ("create_metric", ("", 10.0), "must be non-empty string"),
            ("create_log_entry", ("",), "Log message cannot be empty"),
            ("create_trace", ("", "service"), "must be non-empty string"),
            ("create_health_check", ("",), "Component name cannot be empty"),
        ]
        for method_name, args, expected_error in test_cases:
            method = getattr(factory, method_name)
            result = method(*args)
            tm.that(result.failure, eq=True)
            tm.that(result.error, none=False)
            tm.that(result.error, has=expected_error)

    def test_factory_integration_with_services_real(self) -> None:
        """Test factory integration with real service workflows."""
        factory = FlextObservability.FlextObservabilityMasterFactory()
        metric = factory.create_metric("request_count", 100, "counter")
        log = factory.create_log_entry("Request processed", "info")
        alert = factory.create_alert("High request count", "monitoring", "medium")
        trace = factory.create_trace("process_request", "api_service")
        health = factory.create_health_check("api_service", "healthy")
        for result in (metric, log, alert, trace, health):
            tm.that(result.success, eq=True)
        timestamp_fields = ("timestamp", "created_at", "start_time")
        for result in (metric, log, alert, trace, health):
            entity = result.value if hasattr(result, "unwrap") else result
            has_timestamp = any(hasattr(entity, f) for f in timestamp_fields)
            tm.that(has_timestamp, eq=True)
            timestamp_attr = None
            for field in timestamp_fields:
                timestamp_attr = getattr(entity, field, None)
                if timestamp_attr is not None:
                    break
            if timestamp_attr:
                if hasattr(timestamp_attr, "root"):
                    tm.that(timestamp_attr.root, is_=datetime)
                else:
                    tm.that(timestamp_attr, is_=datetime)
