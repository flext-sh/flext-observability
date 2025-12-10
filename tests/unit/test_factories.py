"""Unit tests for flext_observability.factories module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability import FlextObservabilityFactories


class TestFlextObservabilityFactories:
    """Test the FlextObservabilityFactories class."""

    def test_factory_class_exists(self) -> None:
        """Test that FlextObservabilityFactories class exists."""
        assert FlextObservabilityFactories is not None

    def test_factory_methods_exist(self) -> None:
        """Test that factory methods exist."""
        methods = [
            "create_metric",
            "create_trace",
            "create_alert",
            "create_health_check",
            "create_log_entry",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityFactories, method)
            assert callable(getattr(FlextObservabilityFactories, method))

    def test_create_metric_success(self) -> None:
        """Test creating a metric successfully."""
        result = FlextObservabilityFactories.create_metric("test_metric", 42.0)
        assert result.is_success
        metric = result.value
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.unit == "count"
        assert metric.source == "application"

    def test_create_trace_success(self) -> None:
        """Test creating a trace successfully."""
        result = FlextObservabilityFactories.create_trace(
            "test_operation",
            "test_service",
        )
        assert result.is_success
        trace = result.value
        assert trace.operation_name == "test_operation"
        assert trace.service_name == "test_service"

    def test_create_alert_success(self) -> None:
        """Test creating an alert successfully."""
        result = FlextObservabilityFactories.create_alert("test_alert", "test message")
        assert result.is_success
        alert = result.value
        assert alert.name == "test_alert"
        assert alert.message == "test message"
        assert alert.severity == "info"

    def test_create_health_check_success(self) -> None:
        """Test creating a health check successfully."""
        result = FlextObservabilityFactories.create_health_check("test_check")
        assert result.is_success
        health_check = result.value
        assert health_check.name == "test_check"
        assert health_check.status == "healthy"

    def test_create_log_entry_success(self) -> None:
        """Test creating a log entry successfully."""
        result = FlextObservabilityFactories.create_log_entry("test message")
        assert result.is_success
        log_entry = result.value
        assert log_entry.message == "test message"
        assert log_entry.level == "info"

    def test_create_metric_validation_failure(self) -> None:
        """Test metric creation validation failure."""
        result = FlextObservabilityFactories.create_metric("", 42.0)
        assert result.is_failure

    def test_create_trace_validation_failure(self) -> None:
        """Test trace creation validation failure."""
        result = FlextObservabilityFactories.create_trace("", "test_service")
        assert result.is_failure

    def test_create_alert_validation_failure(self) -> None:
        """Test alert creation validation failure."""
        result = FlextObservabilityFactories.create_alert("", "message")
        assert result.is_failure

    def test_create_health_check_validation_failure(self) -> None:
        """Test health check creation validation failure."""
        result = FlextObservabilityFactories.create_health_check("")
        assert result.is_failure

    def test_create_log_entry_validation_failure(self) -> None:
        """Test log entry creation validation failure."""
        result = FlextObservabilityFactories.create_log_entry("")
        assert result.is_failure
