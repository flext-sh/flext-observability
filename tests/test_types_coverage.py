"""Test coverage for types module using real functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import math
from decimal import Decimal

import flext_observability.types as types_module
from flext_observability import (
    AlertLevel,
    AlertProtocol,
    FlextTypes,
    HealthCheckProtocol,
    HealthStatus,
    LogEntryProtocol,
    LogLevel,
    MetricProtocol,
    MetricValue,
    ObservabilityTypes,
    TagsDict,
    TraceProtocol,
    TraceStatus,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)


class TestTypesModuleCoverage:
    """Test coverage for types module definitions and protocols."""

    def test_type_aliases_definition(self) -> None:
        """Test that type aliases are correctly defined."""
        # Test MetricValue accepts various numeric types
        value1: MetricValue = 42.0  # float
        value2: MetricValue = 42  # int
        value3: MetricValue = Decimal("42.5")  # Decimal

        assert isinstance(value1, float)
        assert isinstance(value2, int)
        assert isinstance(value3, Decimal)

    def test_tags_dict_type(self) -> None:
        """Test TagsDict type alias supports expected values."""
        tags: TagsDict = {
            "string_tag": "value",
            "int_tag": 42,
            "float_tag": math.pi,
            "bool_tag": True,
        }

        assert tags["string_tag"] == "value"
        assert tags["int_tag"] == 42
        assert tags["float_tag"] == math.pi
        assert tags["bool_tag"] is True

    def test_string_type_aliases(self) -> None:
        """Test string-based type aliases."""
        log_level: LogLevel = "INFO"
        alert_level: AlertLevel = "warning"
        trace_status: TraceStatus = "completed"
        health_status: HealthStatus = "healthy"

        assert log_level == "INFO"
        assert alert_level == "warning"
        assert trace_status == "completed"
        assert health_status == "healthy"

    def test_protocol_structure_validation(self) -> None:
        """Test that protocols define expected attributes using real entities."""
        # Create real entities instead of mock implementations
        metric_result = flext_create_metric("test_metric", 42.0, "count")
        trace_result = flext_create_trace("test_op")
        alert_result = flext_create_alert("Test alert", "test_service", "medium")
        health_result = flext_create_health_check("test_service", "healthy")
        log_result = flext_create_log_entry("Test log", "test_service", "info")

        # Verify all entities were created successfully
        assert metric_result.success
        assert trace_result.success
        assert alert_result.success
        assert health_result.success
        assert log_result.success

        # Extract real instances
        metric_instance = metric_result.data
        trace_instance = trace_result.data
        alert_instance = alert_result.data
        health_instance = health_result.data
        log_instance = log_result.data

        # Test protocol compatibility by accessing attributes
        assert hasattr(metric_instance, "name")
        assert hasattr(metric_instance, "value")
        assert hasattr(metric_instance, "unit")
        assert hasattr(metric_instance, "timestamp")
        assert hasattr(metric_instance, "tags")

        assert hasattr(trace_instance, "operation")
        assert hasattr(trace_instance, "span_id")
        assert hasattr(trace_instance, "trace_id")
        assert hasattr(trace_instance, "span_attributes")
        assert hasattr(trace_instance, "duration_ms")
        assert hasattr(trace_instance, "status")
        assert hasattr(trace_instance, "timestamp")

        assert hasattr(alert_instance, "title")
        assert hasattr(alert_instance, "message")
        assert hasattr(alert_instance, "severity")
        assert hasattr(alert_instance, "status")
        assert hasattr(alert_instance, "tags")
        assert hasattr(alert_instance, "timestamp")
        assert hasattr(health_instance, "component")
        assert hasattr(health_instance, "status")
        assert hasattr(health_instance, "message")
        assert hasattr(health_instance, "metrics")
        assert hasattr(health_instance, "timestamp")

        assert hasattr(log_instance, "message")
        assert hasattr(log_instance, "level")
        assert hasattr(log_instance, "context")
        assert hasattr(log_instance, "timestamp")

    def test_observability_types_class(self) -> None:
        """Test ObservabilityTypes class attributes."""
        # Test that class attributes are correctly assigned
        assert ObservabilityTypes.MetricValue == MetricValue
        assert ObservabilityTypes.TagsDict == TagsDict
        assert ObservabilityTypes.LogLevel == LogLevel
        assert ObservabilityTypes.AlertLevel == AlertLevel
        assert ObservabilityTypes.TraceStatus == TraceStatus
        assert ObservabilityTypes.HealthStatus == HealthStatus

        # Test protocol assignments
        assert ObservabilityTypes.MetricProtocol == MetricProtocol
        assert ObservabilityTypes.TraceProtocol == TraceProtocol
        assert ObservabilityTypes.AlertProtocol == AlertProtocol
        assert ObservabilityTypes.HealthCheckProtocol == HealthCheckProtocol
        assert ObservabilityTypes.LogEntryProtocol == LogEntryProtocol

    def test_flext_types_alias(self) -> None:
        """Test FlextTypes alias works correctly."""
        # Test that FlextTypes is an alias for ObservabilityTypes
        assert FlextTypes == ObservabilityTypes

        # Test that they have the same attributes
        assert FlextTypes.MetricValue == ObservabilityTypes.MetricValue
        assert FlextTypes.MetricProtocol == ObservabilityTypes.MetricProtocol

    def test_module_all_exports(self) -> None:
        """Test that all expected exports are available."""
        # Test that __all__ contains expected items
        expected_exports = {
            "AlertLevel",
            "AlertProtocol",
            "E",
            "F",
            "FlextTypes",
            "HealthCheckProtocol",
            "HealthStatus",
            "LogEntryProtocol",
            "LogLevel",
            "MetricProtocol",
            "MetricValue",
            "ObservabilityTypes",
            "P",
            "R",
            "T",
            "TagsDict",
            "TraceProtocol",
            "TraceStatus",
            "U",
            "V",
        }

        actual_exports = set(types_module.__all__)
        assert expected_exports == actual_exports

        # Test that all exports are actually available
        for export_name in types_module.__all__:
            assert hasattr(types_module, export_name), f"Missing export: {export_name}"
            exported_item = getattr(types_module, export_name)
            assert exported_item is not None, f"Null export: {export_name}"
