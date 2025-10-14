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

    def test_nested_factory_classes(self) -> None:
        """Test that nested factory classes exist."""
        assert hasattr(FlextObservabilityFactories, "MetricFactory")
        assert hasattr(FlextObservabilityFactories, "TraceFactory")
        assert hasattr(FlextObservabilityFactories, "AlertFactory")
        assert hasattr(FlextObservabilityFactories, "HealthCheckFactory")
        assert hasattr(FlextObservabilityFactories, "LogEntryFactory")

    def test_metric_factory_methods(self) -> None:
        """Test MetricFactory has required methods."""
        factory = FlextObservabilityFactories.MetricFactory
        methods = [
            "create_metric",
            "create_counter",
            "create_gauge",
            "create_histogram",
        ]
        for method in methods:
            assert hasattr(factory, method)
            assert callable(getattr(factory, method))

    def test_trace_factory_methods(self) -> None:
        """Test TraceFactory has required methods."""
        factory = FlextObservabilityFactories.TraceFactory
        methods = ["create_trace", "create_span", "start_trace", "complete_trace"]
        for method in methods:
            assert hasattr(factory, method)
            assert callable(getattr(factory, method))

    def test_alert_factory_methods(self) -> None:
        """Test AlertFactory has required methods."""
        factory = FlextObservabilityFactories.AlertFactory
        methods = [
            "create_alert",
            "create_info_alert",
            "create_warning_alert",
            "create_error_alert",
        ]
        for method in methods:
            assert hasattr(factory, method)
            assert callable(getattr(factory, method))

    def test_health_check_factory_methods(self) -> None:
        """Test HealthCheckFactory has required methods."""
        factory = FlextObservabilityFactories.HealthCheckFactory
        methods = [
            "create_health_check",
            "create_database_health_check",
            "create_service_health_check",
        ]
        for method in methods:
            assert hasattr(factory, method)
            assert callable(getattr(factory, method))

    def test_log_entry_factory_methods(self) -> None:
        """Test LogEntryFactory has required methods."""
        factory = FlextObservabilityFactories.LogEntryFactory
        methods = [
            "create_log_entry",
            "create_debug_log",
            "create_info_log",
            "create_warning_log",
            "create_error_log",
        ]
        for method in methods:
            assert hasattr(factory, method)
            assert callable(getattr(factory, method))
