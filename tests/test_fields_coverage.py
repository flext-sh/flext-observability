"""Test coverage for fields module - FlextObservabilityFields only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import flext_observability.fields as fields_module
from flext_observability import (
    FlextObservabilityFields,
)


class TestFlextObservabilityFields:
    """Test coverage for FlextObservabilityFields unified field system."""

    def test_flext_observability_fields_exists(self) -> None:
        """Test that FlextObservabilityFields is properly exported."""
        assert FlextObservabilityFields is not None
        assert hasattr(FlextObservabilityFields, "MetricFields")
        assert hasattr(FlextObservabilityFields, "AlertFields")
        assert hasattr(FlextObservabilityFields, "TraceFields")
        assert hasattr(FlextObservabilityFields, "HealthFields")

    def test_fields_module_exports(self) -> None:
        """Test that fields module exports are properly maintained."""
        # Test that all exports from __all__ exist and are not None
        for export_name in fields_module.__all__:
            assert hasattr(fields_module, export_name), f"Missing export: {export_name}"
            exported_item = getattr(fields_module, export_name)
            assert exported_item is not None, f"Null export: {export_name}"

    def test_field_creation_methods_exist(self) -> None:
        """Test that field creation methods are available."""
        # Test metric field creation methods
        assert hasattr(
            FlextObservabilityFields.MetricFields, "create_metric_name_field"
        )
        assert hasattr(
            FlextObservabilityFields.MetricFields, "create_metric_value_field"
        )
        assert hasattr(
            FlextObservabilityFields.MetricFields, "create_metric_unit_field"
        )

        # Test alert field creation methods
        assert hasattr(
            FlextObservabilityFields.AlertFields, "create_alert_message_field"
        )

        # Test trace field creation methods
        assert hasattr(FlextObservabilityFields.TraceFields, "create_trace_name_field")

        # Test timestamp field creation
        assert hasattr(FlextObservabilityFields, "create_timestamp_field")
