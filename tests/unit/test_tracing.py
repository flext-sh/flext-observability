"""Unit tests for flext_observability.tracing module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability import FlextObservabilityTracing


class TestFlextObservabilityTracing:
    """Test the FlextObservabilityTracing class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityTracing inherits from FlextCore.Models."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityTracing, FlextCore.Models)

    def test_flext_trace_class_exists(self) -> None:
        """Test that FlextTrace class exists."""
        assert hasattr(FlextObservabilityTracing, "FlextTrace")

    def test_trace_factory_methods(self) -> None:
        """Test trace factory methods exist."""
        methods = [
            "flext_trace",
            "create_span",
            "start_trace",
            "complete_trace",
            "validate_trace_name",
            "validate_span_name",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityTracing, method)
            assert callable(getattr(FlextObservabilityTracing, method))

    def test_trace_operations(self) -> None:
        """Test trace operations exist."""
        operations = [
            "record_trace",
            "get_trace",
            "update_trace",
            "delete_trace",
            "list_traces",
            "search_traces",
            "export_traces",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityTracing, operation)
            assert callable(getattr(FlextObservabilityTracing, operation))

    def test_trace_validation_methods(self) -> None:
        """Test trace validation methods exist."""
        validations = [
            "validate_trace_name_length",
            "validate_span_count",
            "validate_trace_duration",
            "validate_trace_tags",
        ]
        for validation in validations:
            assert hasattr(FlextObservabilityTracing, validation)
            assert callable(getattr(FlextObservabilityTracing, validation))

    def test_trace_constants(self) -> None:
        """Test trace constants are defined."""
        constants = [
            "MAX_TRACE_NAME_LENGTH",
            "MAX_SPAN_COUNT_PER_TRACE",
            "DEFAULT_TRACE_STATUS",
            "SUPPORTED_TRACE_STATUSES",
        ]
        for constant in constants:
            assert hasattr(FlextObservabilityTracing, constant)
