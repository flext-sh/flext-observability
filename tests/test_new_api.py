"""Tests for the new observability API structure.

Tests the refactored modules


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import FlextCore

from flext_observability import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextObservabilityConstants,
    FlextObservabilityMasterFactory,
    FlextTrace,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
    get_global_factory,
    reset_global_factory,
)


class TestSimpleAPI:
    """Test the simple API functions."""

    def test_create_metric_success(self) -> None:
        """Test successful metric creation."""
        result = flext_create_metric("test_metric", 42.0, "count")

        assert result.is_success
        assert isinstance(result.data, FlextMetric)
        assert result.data.name == "test_metric"
        assert result.data.value == 42.0
        assert result.data.unit == "count"

    def test_create_trace_success(self) -> None:
        """Test successful trace creation."""
        result = flext_create_trace("test_operation")

        assert result.is_success
        assert isinstance(result.data, FlextTrace)
        assert result.data.operation == "test_operation"

    def test_create_alert_success(self) -> None:
        """Test successful alert creation."""
        result = flext_create_alert("Test Alert", "Test alert message", "medium")

        assert result.is_success
        assert isinstance(result.data, FlextAlert)
        assert result.data.title == "Test Alert"
        assert result.data.message == "Test alert message"
        assert result.data.severity == "medium"

    def test_create_health_check_success(self) -> None:
        """Test successful health check creation."""
        result = flext_create_health_check("test_service", "healthy")

        assert result.is_success
        assert isinstance(result.data, FlextHealthCheck)
        assert result.data.component == "test_service"
        assert result.data.status == "healthy"

    def test_create_log_entry_success(self) -> None:
        """Test successful log entry creation."""
        result = flext_create_log_entry("Test message", "test_service", "info")

        assert result.is_success
        assert isinstance(result.data, FlextLogEntry)
        assert result.data.message == "[test_service] Test message"
        assert result.data.level == "info"


class TestFactoryPattern:
    """Test the factory pattern functionality."""

    def test_global_factory(self) -> None:
        """Test global factory usage."""
        reset_global_factory()
        factory = get_global_factory()

        result = factory.create_metric("global_test", 100.0, "count")
        assert result.is_success
        assert result.unwrap().name == "global_test"

    def test_custom_factory(self) -> None:
        """Test custom factory creation."""
        # FlextCore.Container imported at top level

        container = FlextCore.Container()
        factory = FlextObservabilityMasterFactory(container)

        result = factory.create_metric("custom_test", 200.0, "count")
        assert result.is_success
        assert result.unwrap().name == "custom_test"


class TestEntityValidation:
    """Test entity validation functionality."""

    def test_metric_validation_success(self) -> None:
        """Test successful metric validation."""
        result = flext_create_metric("valid_metric", 50.0, "count")
        assert result.is_success

        validation = result.unwrap().validate_business_rules()
        assert validation.is_success

    def test_metric_validation_empty_name(self) -> None:
        """Test metric validation with empty name."""
        result = flext_create_metric("", 50.0, "count")
        # Should be caught by pydantic validation
        assert (
            not result.is_success
            or not result.unwrap().validate_business_rules().is_success
        )

    def test_trace_validation_success(self) -> None:
        """Test successful trace validation."""
        result = flext_create_trace("valid_operation")
        assert result.is_success

        validation = result.unwrap().validate_business_rules()
        assert validation.is_success

    def test_alert_validation_success(self) -> None:
        """Test successful alert validation."""
        result = flext_create_alert("Valid alert", "service", "low")
        assert result.is_success

        validation = result.unwrap().validate_business_rules()
        assert validation.is_success

    def test_health_check_validation_success(self) -> None:
        """Test successful health check validation."""
        result = flext_create_health_check("service", "healthy")
        assert result.is_success

        validation = result.unwrap().validate_business_rules()
        assert validation.is_success


class TestConstants:
    """Test observability constants."""

    def test_constants_available(self) -> None:
        """Test that constants are properly defined."""
        assert hasattr(FlextObservabilityConstants, "METRIC_TYPE_COUNTER")
        assert hasattr(FlextObservabilityConstants, "ALERT_LEVEL_WARNING")
        assert hasattr(FlextObservabilityConstants, "TRACE_STATUS_STARTED")
        assert hasattr(FlextObservabilityConstants, "HEALTH_STATUS_HEALTHY")

    def test_constants_values(self) -> None:
        """Test constant values are correct."""
        assert FlextObservabilityConstants.METRIC_TYPE_COUNTER == "counter"
        assert FlextObservabilityConstants.ALERT_LEVEL_WARNING == "warning"
        assert FlextObservabilityConstants.TRACE_STATUS_STARTED == "started"
        assert FlextObservabilityConstants.HEALTH_STATUS_HEALTHY == "healthy"


class TestEntityTypes:
    """Test entity type verification."""

    def test_entity_types(self) -> None:
        """Test that entities are of correct types."""
        metric_result = flext_create_metric("test", 1.0, "count")
        trace_result = flext_create_trace("test")
        alert_result = flext_create_alert("test", "service", "medium")
        health_result = flext_create_health_check("service", "healthy")
        log_result = flext_create_log_entry("test", "service", "info")

        assert isinstance(metric_result.data, FlextMetric)
        assert isinstance(trace_result.data, FlextTrace)
        assert isinstance(alert_result.data, FlextAlert)
        assert isinstance(health_result.data, FlextHealthCheck)
        assert isinstance(log_result.data, FlextLogEntry)

    def test_entity_attributes(self) -> None:
        """Test that entities have required attributes."""
        metric = flext_create_metric("test", 1.0, "count").data

        assert hasattr(metric, "name")
        assert hasattr(metric, "value")
        assert hasattr(metric, "unit")
        assert hasattr(metric, "timestamp")
        assert hasattr(metric, "validate_business_rules")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
