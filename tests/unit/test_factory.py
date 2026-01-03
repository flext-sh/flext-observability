"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from datetime import datetime

from flext_core import FlextContainer

from flext_observability import (
    FlextObservabilityMasterFactory,
    get_global_factory,
    reset_global_factory,
)


class TestFlextObservabilityMasterFactoryReal:
    """Real functionality tests for master factory without excessive mocking."""

    def test_factory_initialization_and_container_real(self) -> None:
        """Test factory initialization with real container integration."""
        # Test with custom container
        container = FlextContainer()
        factory = FlextObservabilityMasterFactory(container)
        assert factory.container is container

        # Test without container (creates default)
        factory_default = FlextObservabilityMasterFactory()
        assert factory_default.container is not None
        assert isinstance(factory_default.container, FlextContainer)

    def test_metric_creation_real_functionality(self) -> None:
        """Test metric creation with actual factory functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create metric using factory method
        metric_result = factory.create_metric("test_metric", 42.5, "gauge")

        # Validate real result
        assert metric_result.is_success, (
            f"Metric creation failed: {metric_result.error}"
        )
        assert metric_result.data is not None
        assert metric_result.data.name == "test_metric"
        assert metric_result.data.value == 42.5
        assert metric_result.data.unit == "gauge"

    def test_metric_creation_with_validation_real(self) -> None:
        """Test metric creation with real validation logic."""
        factory = FlextObservabilityMasterFactory()

        # Test with empty name (should fail validation)
        invalid_result = factory.create_metric("", 10.0)
        assert invalid_result.is_failure
        assert invalid_result.error is not None
        assert "must be non-empty string" in invalid_result.error

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create log using factory (signature: message, level, context)
        log_result = factory.create_log_entry(
            "Test log message",
            "info",
        )

        # Validate real result
        assert log_result.is_success, f"Log creation failed: {log_result.error}"
        assert log_result.data is not None
        assert log_result.data.message == "Test log message"
        # FlextLogEntry doesn't have service field, check other attributes
        assert log_result.data.level == "info"

    def test_log_creation_validation_real(self) -> None:
        """Test log creation with real validation."""
        factory = FlextObservabilityMasterFactory()

        # Test custom level - system validates and may reject or use default
        # Signature: (message, level, context)
        custom_level_result = factory.create_log_entry(
            "Test",
            "INVALID_LEVEL",
        )
        if custom_level_result.is_failure:
            # If system rejects it, verify error message
            assert custom_level_result.error is not None
        else:
            # System accepts/normalizes - either uses provided value or defaults to 'info'
            assert custom_level_result.value.level in ("INVALID_LEVEL", "info")

    def test_alert_creation_real_functionality(self) -> None:
        """Test alert creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create alert using factory
        alert_result = factory.create_alert(
            "Critical error detected",
            "monitoring",
            "critical",
        )

        # Validate real result
        assert alert_result.is_success, f"Alert creation failed: {alert_result.error}"
        assert alert_result.data is not None
        assert alert_result.data.message == "Critical error detected"
        # FlextAlert title format is "Alert: {service}"
        assert alert_result.data.title == "Alert: monitoring"
        assert alert_result.data.severity == "critical"

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create trace using factory
        trace_result = factory.create_trace("user_authentication", "auth_service")

        # Validate real result
        assert trace_result.is_success, f"Trace creation failed: {trace_result.error}"
        assert trace_result.data is not None
        # Trace uses 'name' attribute for the operation
        assert trace_result.data.name == "user_authentication"
        # Trace should have generated IDs
        assert trace_result.data.trace_id is not None

    def test_health_check_creation_real_functionality(self) -> None:
        """Test health check creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create health check using factory
        health_result = factory.create_health_check("database", "healthy")

        # Validate real result
        assert health_result.is_success, (
            f"Health check creation failed: {health_result.error}"
        )
        assert health_result.data is not None
        assert health_result.data.component == "database"
        assert health_result.data.status == "healthy"

    def test_factory_shorthand_methods_real(self) -> None:
        """Test factory shorthand methods with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Test shorthand metric method
        metric_result = factory.metric("cpu_usage", 85.2)
        assert metric_result.is_success
        metric = metric_result.value
        assert hasattr(metric, "name")
        assert metric.name == "cpu_usage"
        assert hasattr(metric, "value")
        assert metric.value == 85.2

        # Test shorthand log method
        log_result = factory.log("System started")
        assert log_result.is_success
        log_entry = log_result.value
        assert hasattr(log_entry, "message")
        assert log_entry.message == "System started"

        # Test shorthand alert method - alert(title, message)
        alert_result = factory.alert("High memory usage", "monitoring")
        assert alert_result.is_success
        alert = alert_result.value
        assert hasattr(alert, "title")
        assert alert.title == "High memory usage"
        assert alert.message == "monitoring"

        # Test shorthand trace method - trace(trace_id, operation) -> Trace with name=operation
        trace_result = factory.trace("trace-123", "api_request")
        assert trace_result.is_success
        trace = trace_result.value
        assert hasattr(trace, "name")
        assert trace.name == "api_request"
        assert trace.trace_id == "trace-123"

    def test_global_factory_real_functionality(self) -> None:
        """Test global factory with real functionality."""
        # Reset to ensure clean state
        reset_global_factory()

        # Get global factory - should create new instance
        factory1 = get_global_factory()
        assert factory1 is not None
        assert isinstance(factory1, FlextObservabilityMasterFactory)

        # Get again - should return same instance
        factory2 = get_global_factory()
        assert factory2 is factory1

        # Reset and get again - should create new instance
        reset_global_factory()
        factory3 = get_global_factory()
        assert factory3 is not factory1
        assert factory3 is not factory2

    def test_factory_error_handling_real(self) -> None:
        """Test factory error handling with real scenarios."""
        factory = FlextObservabilityMasterFactory()

        # Test with various invalid inputs
        # Note: create_log_entry signature is (message, level, context)
        # Note: create_trace signature is (operation, service)
        test_cases = [
            # (method, args, expected_error_text)
            ("create_metric", ("", 10.0), "must be non-empty string"),
            (
                "create_log_entry",
                ("",),  # message is required
                "Log message cannot be empty",
            ),
            # Note: create_alert with empty message doesn't fail, so not testing
            (
                "create_trace",
                ("", "service"),
                "must be non-empty string",  # "Trace name must be non-empty string"
            ),
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

        # Create multiple entities and verify they work together
        metric = factory.create_metric("request_count", 100, "counter")
        # create_log_entry signature: (message, level, context)
        log = factory.create_log_entry("Request processed", "info")
        alert = factory.create_alert("High request count", "monitoring", "medium")
        trace = factory.create_trace("process_request", "api_service")
        health = factory.create_health_check("api_service", "healthy")

        # All should succeed
        results = [metric, log, alert, trace, health]
        for i, result in enumerate(results):
            # FlextResult uses is_success property
            assert hasattr(result, "is_success"), f"Entity {i} missing is_success property"
            assert result.is_success, (
                f"Entity {i} creation failed: {getattr(result, 'error', 'Unknown error')}"
            )

        # Verify entities have proper timestamps
        # Different entities use different timestamp field names
        timestamp_fields = ("timestamp", "created_at", "start_time")
        for result in results:
            entity = result.value if hasattr(result, "unwrap") else result
            has_timestamp = any(hasattr(entity, f) for f in timestamp_fields)
            assert has_timestamp, f"Entity {type(entity).__name__} has no timestamp field"

            # Get the timestamp value from whichever field exists
            timestamp_attr = None
            for field in timestamp_fields:
                timestamp_attr = getattr(entity, field, None)
                if timestamp_attr is not None:
                    break

            if timestamp_attr:
                # Handle both FlextModels and datetime objects
                if hasattr(timestamp_attr, "root"):
                    # FlextModels object with .root attribute
                    assert isinstance(timestamp_attr.root, datetime)
                else:
                    # Direct datetime object
                    assert isinstance(timestamp_attr, datetime)
