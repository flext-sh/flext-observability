"""Unit tests for flext_observability.monitoring module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityMonitor


class TestFlextObservabilityMonitor:
    """Test the FlextObservabilityMonitor class."""

    def test_monitor_class_exists(self) -> None:
        """Test that FlextObservabilityMonitor class exists."""
        assert FlextObservabilityMonitor is not None

    def test_monitoring_helpers_nested_class(self) -> None:
        """Test that MonitoringHelpers nested class exists."""
        assert hasattr(FlextObservabilityMonitor, "MonitoringHelpers")

    def test_monitoring_helpers_methods(self) -> None:
        """Test MonitoringHelpers has required methods."""
        helpers = FlextObservabilityMonitor.MonitoringHelpers
        methods = ["call_any_function", "execute_monitored_function"]
        for method in methods:
            assert hasattr(helpers, method)
            assert callable(getattr(helpers, method))

    def test_monitor_operations_exist(self) -> None:
        """Test key monitor operations are available."""
        operations = [
            "initialize_monitoring",
            "start_monitoring",
            "stop_monitoring",
            "monitor_function",
            "monitor_async_function",
            "record_function_call",
            "record_exception",
            "record_performance_metric",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityMonitor, operation)
            assert callable(getattr(FlextObservabilityMonitor, operation))

    def test_monitor_configuration(self) -> None:
        """Test monitor configuration attributes."""
        config_attrs = [
            "service_name",
            "environment",
            "metrics_enabled",
            "tracing_enabled",
            "alerting_enabled",
            "health_check_enabled",
        ]
        for attr in config_attrs:
            assert hasattr(FlextObservabilityMonitor, attr)

    def test_monitor_decorators(self) -> None:
        """Test monitoring decorators are available."""
        decorators = ["monitor_sync", "monitor_async", "monitor_method"]
        for decorator in decorators:
            assert hasattr(FlextObservabilityMonitor, decorator)
            assert callable(getattr(FlextObservabilityMonitor, decorator))
