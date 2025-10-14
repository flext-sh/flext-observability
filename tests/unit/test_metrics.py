"""Unit tests for flext_observability.metrics module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability import FlextObservabilityMetrics


class TestFlextObservabilityMetrics:
    """Test the FlextObservabilityMetrics class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityMetrics inherits from FlextCore.Models."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityMetrics, FlextCore.Models)

    def test_flext_metric_class_exists(self) -> None:
        """Test that FlextMetric class exists."""
        assert hasattr(FlextObservabilityMetrics, "FlextMetric")

    def test_metric_factory_methods(self) -> None:
        """Test metric factory methods exist."""
        methods = [
            "flext_metric",
            "create_counter",
            "create_gauge",
            "create_histogram",
            "validate_metric_name",
            "validate_metric_value",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityMetrics, method)
            assert callable(getattr(FlextObservabilityMetrics, method))

    def test_metric_operations(self) -> None:
        """Test metric operations exist."""
        operations = [
            "record_metric",
            "get_metric",
            "update_metric",
            "delete_metric",
            "list_metrics",
            "aggregate_metrics",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityMetrics, operation)
            assert callable(getattr(FlextObservabilityMetrics, operation))

    def test_metric_validation_methods(self) -> None:
        """Test metric validation methods exist."""
        validations = [
            "validate_metric_name_length",
            "validate_metric_unit",
            "validate_metric_tags",
            "validate_metric_timestamp",
        ]
        for validation in validations:
            assert hasattr(FlextObservabilityMetrics, validation)
            assert callable(getattr(FlextObservabilityMetrics, validation))

    def test_metric_constants(self) -> None:
        """Test metric constants are defined."""
        constants = [
            "DEFAULT_METRIC_UNIT",
            "MAX_METRIC_NAME_LENGTH",
            "SUPPORTED_METRIC_TYPES",
        ]
        for constant in constants:
            assert hasattr(FlextObservabilityMetrics, constant)
