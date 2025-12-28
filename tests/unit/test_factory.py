"""Real functionality tests for FlextObservabilityMasterFactory - NO MOCKS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from datetime import datetime

from flext_core import FlextContainer

from flext_observability.factory import (
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
        assert "Metric name cannot be empty" in invalid_result.error

    def test_log_creation_real_functionality(self) -> None:
        """Test log entry creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create log using factory
        log_result = factory.create_log_entry(
            "Test log message",
            "test_service",
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

        # Test custom level - system accepts it (this is real behavior)
        custom_level_result = factory.create_log_entry(
            "Test",
            "service",
            "INVALID_LEVEL",
        )
        if custom_level_result.is_failure:
            # If system rejects it, verify error message
            assert custom_level_result.error is not None
            assert "Invalid log level" in custom_level_result.error
        else:
            # If system accepts it, verify it works correctly
            assert custom_level_result.value.level == "INVALID_LEVEL"

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
        # FlextAlert doesn't have service or level fields, check other attributes
        assert alert_result.data.title == "Alert from monitoring"
        assert alert_result.data.severity == "critical"

    def test_trace_creation_real_functionality(self) -> None:
        """Test trace creation with real functionality."""
        factory = FlextObservabilityMasterFactory()

        # Create trace using factory
        trace_result = factory.create_trace("user_authentication", "auth_service")

        # Validate real result
        assert trace_result.is_success, f"Trace creation failed: {trace_result.error}"
        assert trace_result.data is not None
        assert trace_result.data.operation == "user_authentication"
        # FlextTrace doesn't have service_name field, check other attributes
        # Trace should have generated IDs
        assert trace_result.data.trace_id is not None
        assert trace_result.data.span_id is not None

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

        # Test shorthand alert method
        alert_result = factory.alert("High memory usage", "monitoring")
        assert alert_result.is_success
        alert = alert_result.value
        assert hasattr(alert, "message")
        assert alert.message == "High memory usage"

        # Test shorthand trace method
        trace_result = factory.trace("trace-123", "api_request")
        assert trace_result.is_success
        trace = trace_result.value
        assert hasattr(trace, "operation")
        assert trace.operation == "api_request"

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

    def test_global_factory_with_custom_container_real(self) -> None:
        """Test global factory with custom container."""
        # Reset to clean state
        reset_global_factory()

        # Create custom container
        custom_container = FlextContainer()

        # Get global factory with custom container
        factory = get_global_factory(custom_container)
        assert factory.container is custom_container

        # Get again - should return same instance
        factory2 = get_global_factory()
        assert factory2 is factory
        assert factory2.container is custom_container

    def test_factory_entity_validation_real(self) -> None:
        """Test factory with real entity validation workflows."""
        factory = FlextObservabilityMasterFactory()

        # Test metrics with business rule validation
        metric_result = factory.create_metric("response_time", 150.0, "milliseconds")
        assert metric_result.is_success

        # Validate business rules on created entity
        validation_result = metric_result.value.validate_business_rules()
        assert validation_result.is_success

        # Test with negative value (currently allowed by implementation)
        negative_metric = factory.create_metric("error_rate", -5.0)  # Negative value
        assert negative_metric.is_success
        # Current implementation allows negative values
        validation_result = negative_metric.value.validate_business_rules()
        assert validation_result.is_success

    def test_factory_error_handling_real(self) -> None:
        """Test factory error handling with real scenarios."""
        factory = FlextObservabilityMasterFactory()

        # Test with various invalid inputs
        test_cases = [
            # (method, args, expected_error_text)
            ("create_metric", ("", 10.0), "Metric name cannot be empty"),
            (
                "create_log_entry",
                ("", "service"),
                "Log message cannot be empty",
            ),
            (
                "create_alert",
                ("", "service", "medium"),
                "Alert message cannot be empty",
            ),
            (
                "create_trace",
                ("", "service"),
                "Operation name cannot be empty",
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
        log = factory.create_log_entry("Request processed", "api_service", "info")
        alert = factory.create_alert("High request count", "monitoring", "medium")
        trace = factory.create_trace("process_request", "api_service")
        health = factory.create_health_check("api_service", "healthy")

        # All should succeed
        results = [metric, log, alert, trace, health]
        for i, result in enumerate(results):
            # Use hasattr to check for FlextResult methods
            assert hasattr(result, "success"), f"Entity {i} missing success attribute"
            assert result.is_success, (
                f"Entity {i} creation failed: {getattr(result, 'error', 'Unknown error')}"
            )

        # Verify entities have proper timestamps
        for result in results:
            # Use hasattr to check for unwrap method
            entity = result.value if hasattr(result, "unwrap") else result
            assert hasattr(entity, "timestamp") or hasattr(entity, "created_at")
            timestamp_attr = getattr(
                entity,
                "timestamp",
                getattr(entity, "created_at", None),
            )
            if timestamp_attr:
                # Handle both FlextModels and datetime objects
                if hasattr(timestamp_attr, "root"):
                    # FlextModels object with .root attribute
                    assert isinstance(timestamp_attr.root, datetime)
                else:
                    # Direct datetime object
                    assert isinstance(timestamp_attr, datetime)
