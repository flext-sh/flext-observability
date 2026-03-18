"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

import pytest
from flext_core import FlextContainer
from flext_tests import tm

from flext_observability import (
    get_global_factory,
    reset_global_factory,
)
from flext_observability._core import FlextObservabilityMasterFactory
from tests import p


class TestFlextObservabilityMasterFactoryReal:
    """Real functionality tests for master factory without excessive mocking."""

    def test_factory_initialization_and_container_real(self) -> None:
        """Test factory initialization with real container integration."""
        container = FlextContainer()
        factory = FlextObservabilityMasterFactory(container)
        tm.that(factory.container is container, eq=True)
        factory_default = FlextObservabilityMasterFactory()
        tm.that(factory_default.container is not None, eq=True)
        tm.that(isinstance(factory_default.container, p.Container), eq=True)

    def test_metric_creation_real_functionality(self) -> None:
        """Test metric creation with actual factory functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.create_metric("test_metric", 42.5, "gauge")
        (
            tm.that(metric_result.is_success, eq=True),
            (f"Metric creation failed: {metric_result.error}"),
        )
        tm.that(metric_result.value is not None, eq=True)
        tm.that(metric_result.value.name == "test_metric", eq=True)
        tm.that(metric_result.value.value == pytest.approx(42.5), eq=True)
        tm.that(metric_result.value.unit == "gauge", eq=True)

    def test_metric_creation_with_validation_real(self) -> None:
        """Test metric creation with real validation logic."""
        factory = FlextObservabilityMasterFactory()
        invalid_result = factory.create_metric("", 10.0)
        tm.that(invalid_result.is_failure, eq=True)
        tm.that(invalid_result.error is not None, eq=True)
        tm.that("must be non-empty string" in invalid_result.error, eq=True)

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        log_result = factory.create_log_entry("Test log message", "info")
        (
            tm.that(log_result.is_success, eq=True),
            f"Log creation failed: {log_result.error}",
        )
        tm.that(log_result.value is not None, eq=True)
        tm.that(log_result.value.message == "Test log message", eq=True)
        tm.that(log_result.value.level == "info", eq=True)

    def test_log_creation_validation_real(self) -> None:
        """Test log creation with real validation."""
        factory = FlextObservabilityMasterFactory()
        custom_level_result = factory.create_log_entry("Test", "INVALID_LEVEL")
        if custom_level_result.is_failure:
            tm.that(custom_level_result.error is not None, eq=True)
        else:
            tm.that(
                custom_level_result.value.level in {"INVALID_LEVEL", "info"}, eq=True
            )

    def test_alert_creation_real_functionality(self) -> None:
        """Test alert creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        alert_result = factory.create_alert(
            "Critical error detected", "monitoring", "critical"
        )
        (
            tm.that(alert_result.is_success, eq=True),
            f"Alert creation failed: {alert_result.error}",
        )
        tm.that(alert_result.value is not None, eq=True)
        tm.that(alert_result.value.message == "Critical error detected", eq=True)
        tm.that(alert_result.value.title == "Alert: monitoring", eq=True)
        tm.that(alert_result.value.severity == "critical", eq=True)

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        trace_result = factory.create_trace("user_authentication", "auth_service")
        (
            tm.that(trace_result.is_success, eq=True),
            f"Trace creation failed: {trace_result.error}",
        )
        tm.that(trace_result.value is not None, eq=True)
        tm.that(trace_result.value.name == "user_authentication", eq=True)
        tm.that(trace_result.value.trace_id is not None, eq=True)

    def test_health_check_creation_real_functionality(self) -> None:
        """Test health check creation with real functionality."""
        factory = FlextObservabilityMasterFactory()
        health_result = factory.create_health_check("database", "healthy")
        (
            tm.that(health_result.is_success, eq=True),
            (f"Health check creation failed: {health_result.error}"),
        )
        tm.that(health_result.value is not None, eq=True)
        tm.that(health_result.value.component == "database", eq=True)
        tm.that(health_result.value.status == "healthy", eq=True)

    def test_factory_shorthand_methods_real(self) -> None:
        """Test factory shorthand methods with real functionality."""
        factory = FlextObservabilityMasterFactory()
        metric_result = factory.metric("cpu_usage", 85.2)
        tm.that(metric_result.is_success, eq=True)
        metric = metric_result.value
        tm.that(hasattr(metric, "name"), eq=True)
        tm.that(metric.name == "cpu_usage", eq=True)
        tm.that(hasattr(metric, "value"), eq=True)
        tm.that(metric.value == pytest.approx(85.2), eq=True)
        log_result = factory.log("System started")
        tm.that(log_result.is_success, eq=True)
        log_entry = log_result.value
        tm.that(hasattr(log_entry, "message"), eq=True)
        tm.that(log_entry.message == "System started", eq=True)
        alert_result = factory.alert("High memory usage", "monitoring")
        tm.that(alert_result.is_success, eq=True)
        alert = alert_result.value
        tm.that(hasattr(alert, "title"), eq=True)
        tm.that(alert.title == "High memory usage", eq=True)
        tm.that(alert.message == "monitoring", eq=True)
        trace_result = factory.trace("trace-123", "api_request")
        tm.that(trace_result.is_success, eq=True)
        trace = trace_result.value
        tm.that(hasattr(trace, "name"), eq=True)
        tm.that(trace.name == "api_request", eq=True)
        tm.that(trace.trace_id == "trace-123", eq=True)

    def test_global_factory_real_functionality(self) -> None:
        """Test global factory with real functionality."""
        reset_global_factory()
        factory1 = get_global_factory()
        tm.that(factory1 is not None, eq=True)
        factory2 = get_global_factory()
        tm.that(factory2 is not None, eq=True)
        reset_global_factory()
        factory3 = get_global_factory()
        tm.that(factory3 is not None, eq=True)

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
            (
                tm.that(result.is_failure, eq=True),
                (f"Method {method_name} should have failed with args {args}"),
            )
            tm.that(result.error is not None, eq=True)
            tm.that(expected_error in result.error, eq=True)

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
            (
                tm.that(hasattr(result, "is_success"), eq=True),
                (f"Entity {i} missing is_success property"),
            )
            (
                tm.that(result.is_success, eq=True),
                (
                    f"Entity {i} creation failed: {getattr(result, 'error', 'Unknown error')}"
                ),
            )
        timestamp_fields = ("timestamp", "created_at", "start_time")
        for result in results:
            entity = result.value if hasattr(result, "unwrap") else result
            has_timestamp = any(hasattr(entity, f) for f in timestamp_fields)
            (
                tm.that(has_timestamp, eq=True),
                (f"Entity {type(entity).__name__} has no timestamp field"),
            )
            timestamp_attr = None
            for field in timestamp_fields:
                timestamp_attr = getattr(entity, field, None)
                if timestamp_attr is not None:
                    break
            if timestamp_attr:
                if hasattr(timestamp_attr, "root"):
                    tm.that(isinstance(timestamp_attr.root, datetime), eq=True)
                else:
                    tm.that(isinstance(timestamp_attr, datetime), eq=True)
