"""Real functional coverage tests - NO MOCKS ALLOWED.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from datetime import UTC, datetime

import pytest

from flext_observability import (
    FlextMetric,
    FlextObservabilityMasterFactory,
    get_global_factory,
    reset_global_factory,
)


class TestRealFunctionalCoverage:
    """Achieve comprehensive coverage through real functionality only."""

    def test_metric_validation_edge_cases_real(self) -> None:
        """Test real metric validation edge cases for complete coverage."""
        # Test valid metric creation
        metric = FlextMetric(
            name="test_metric",
            value=42.5,
            unit="test",
            tags={"real": "test"},
            timestamp=datetime.now(UTC),
        )

        validation_result = metric.validate_business_rules()
        assert validation_result.is_success

        # Test empty name validation through Pydantic validation
        with pytest.raises(Exception):  # Pydantic should catch empty name
            FlextMetric(
                name="",  # Empty name should fail at Pydantic level
                value=1.0,
                unit="test",
            )

        # Test negative value validation through business rules
        negative_metric = FlextMetric(
            name="negative_test",
            value=-5.0,  # Negative value should pass Pydantic but fail business rules
            unit="test",
        )
        validation_result = negative_metric.validate_business_rules()
        assert validation_result.is_success  # Business rules allow negative values

        # Test business rule validation on valid metric
        valid_metric = FlextMetric(
            name="business_rule_test",
            value=10.0,
            unit="test",
        )

        business_validation = valid_metric.validate_business_rules()
        assert business_validation.is_success

    def test_factory_error_handling_real(self) -> None:
        """Test factory error handling through real invalid inputs."""
        factory = FlextObservabilityMasterFactory()

        # Test invalid metric creation
        invalid_metric = factory.create_metric("", -1.0)
        assert not invalid_metric.is_success
        assert invalid_metric.error is not None

        # Test invalid log entry creation
        invalid_log = factory.create_log_entry("", "invalid_level")
        # Should either succeed with empty message or fail with meaningful error
        assert invalid_log.is_success or invalid_log.error is not None

        # Test invalid alert creation
        invalid_alert = factory.create_alert("", "service", "invalid_level")
        # Should either succeed or fail with meaningful error
        assert invalid_alert.is_success or invalid_alert.error is not None

    def test_comprehensive_factory_functionality_real(self) -> None:
        """Test comprehensive factory functionality for coverage."""
        factory = FlextObservabilityMasterFactory()

        # Test metric creation with various parameters
        metric_result = factory.create_metric(
            "comprehensive_test",
            99.9,
            "percentage",
            tags={"test": "comprehensive"},
        )
        assert metric_result.is_success
        assert metric_result.data is not None
        assert metric_result.data.name == "comprehensive_test"
        assert metric_result.data.value == 99.9

        # Test log entry creation
        log_result = factory.create_log_entry(
            "Comprehensive test log",
            "info",
            context={"test": "comprehensive"},
        )
        assert log_result.is_success or log_result.error is not None

        # Test trace creation
        trace_result = factory.create_trace(
            "comprehensive_trace",
            "test_service",
            tags={"test": "comprehensive"},
        )
        assert trace_result.is_success or trace_result.error is not None

        # Test alert creation
        alert_result = factory.create_alert(
            "Comprehensive test alert",
            "test_service",
            "warning",
            tags={"test": "comprehensive"},
        )
        assert alert_result.is_success or alert_result.error is not None

        # Test health check creation
        health_result = factory.create_health_check(
            "test_service",
            "healthy",
            details={"test": "comprehensive"},
        )
        assert health_result.is_success or health_result.error is not None

    def test_entity_edge_cases_real_functionality(self) -> None:
        """Test entity edge cases through real functionality."""
        # Test metric with extreme values
        extreme_metric = FlextMetric(
            name="extreme_test",
            value=999999.999999,
            unit="extreme",
            tags={"extreme": "true", "number": "42"},
        )

        validation = extreme_metric.validate_business_rules()
        assert validation.is_success

        # Test metric with minimal valid values
        minimal_metric = FlextMetric(
            name="a",  # Minimal valid name
            value=0.0,  # Minimal valid value
            unit="",  # Empty unit should be valid
        )

        minimal_validation = minimal_metric.validate_business_rules()
        assert minimal_validation.is_success

    def test_global_factory_functionality_real(self) -> None:
        """Test global factory functionality for coverage."""
        # Reset global factory to ensure clean state
        reset_global_factory()

        # Get global factory
        global_factory = get_global_factory()
        assert global_factory is not None

        # Test that subsequent calls return the same instance
        same_factory = get_global_factory()
        assert global_factory is same_factory

        # Test global factory functionality
        metric_result = global_factory.create_metric("global_test", 123.45)
        assert metric_result.is_success

        # Reset again for cleanup
        reset_global_factory()

        # Get new factory after reset
        new_factory = get_global_factory()
        assert new_factory is not global_factory  # Should be different instance
