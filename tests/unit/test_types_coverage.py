"""Test coverage for types module using real functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import flext_observability.typings as types_module
from flext_observability import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)
from flext_observability.typings import t


class TestTypesModuleCoverage:
    """Test coverage for types module definitions and protocols."""

    def test_protocol_structure_validation(self) -> None:
        """Test that protocols define expected attributes using real entities."""
        # Create real entities instead of mock implementations
        metric_result = flext_create_metric("test_metric", 42.0, "count")
        trace_result = flext_create_trace("test_trace", "test_op")
        alert_result = flext_create_alert("Test alert", "test_service", "warning")
        health_result = flext_create_health_check("test_service", "healthy")
        log_result = flext_create_log_entry("Test log", "INFO", "test_service")

        # Verify all entities were created successfully
        assert metric_result.is_success
        assert trace_result.is_success
        assert alert_result.is_success
        assert health_result.is_success
        assert log_result.is_success

        # Extract real instances
        metric_instance = metric_result.data
        trace_instance = trace_result.data
        alert_instance = alert_result.data
        health_instance = health_result.data
        log_instance = log_result.data

        # Verify instances are dicts with expected keys
        assert isinstance(metric_instance, dict)
        assert "name" in metric_instance
        assert "value" in metric_instance
        assert "unit" in metric_instance
        assert "timestamp" in metric_instance

        assert isinstance(trace_instance, dict)
        assert "operation" in trace_instance
        assert "span_id" in trace_instance
        assert "trace_id" in trace_instance
        # Check for context or attributes (whichever is present)
        assert "context" in trace_instance or "attributes" in trace_instance

        assert isinstance(alert_instance, dict)
        assert "title" in alert_instance
        assert "message" in alert_instance
        assert "severity" in alert_instance
        assert "timestamp" in alert_instance

        assert isinstance(health_instance, dict)
        assert "service_name" in health_instance  # or "component"
        assert "status" in health_instance
        assert "timestamp" in health_instance
        assert "details" in health_instance  # or "message"

        assert isinstance(log_instance, dict)
        assert "message" in log_instance
        assert "level" in log_instance
        assert "service" in log_instance
        assert "timestamp" in log_instance

    def test_flext_observability_types_class(self) -> None:
        """Test FlextObservabilityTypes class structure."""
        # Test that the class exists and has expected structure
        assert hasattr(FlextObservabilityTypes, "Project")
        assert hasattr(FlextObservabilityTypes, "ObservabilityCore")
        assert hasattr(FlextObservabilityTypes, "Protocols")

        # Test protocol structure
        assert hasattr(t.Protocols, "MetricProtocol")
        assert hasattr(t.Protocols, "TraceProtocol")
        assert hasattr(t.Protocols, "AlertProtocol")
        assert hasattr(t.Protocols, "HealthCheckProtocol")
        assert hasattr(t.Protocols, "LogEntryProtocol")

    def test_module_all_exports(self) -> None:
        """Test that all expected exports are available."""
        # Test that __all__ contains expected items
        expected_exports = {
            "FlextObservabilityTypes",
            "T",
        }

        actual_exports = set(types_module.__all__)
        assert expected_exports == actual_exports

        # Test that all exports are actually available
        for export_name in types_module.__all__:
            assert hasattr(types_module, export_name), f"Missing export: {export_name}"
            exported_item = getattr(types_module, export_name)
            assert exported_item is not None, f"Null export: {export_name}"
