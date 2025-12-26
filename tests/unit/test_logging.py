"""Unit tests for flext_observability.logging module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_core import FlextModels

from flext_observability import FlextObservabilityLogging


class TestFlextObservabilityLogging:
    """Test the FlextObservabilityLogging class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityLogging inherits from FlextModels."""
        assert issubclass(FlextObservabilityLogging, FlextModels)

    def test_flext_log_entry_class_exists(self) -> None:
        """Test that FlextLogEntry class exists."""
        assert hasattr(FlextObservabilityLogging, "FlextLogEntry")

    def test_logging_factory_methods(self) -> None:
        """Test logging factory methods exist."""
        methods = [
            "flext_log_entry",
            "create_debug_log",
            "create_info_log",
            "create_warning_log",
            "create_error_log",
            "create_critical_log",
            "validate_log_message",
            "validate_log_level",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityLogging, method)
            assert callable(getattr(FlextObservabilityLogging, method))

    def test_logging_operations(self) -> None:
        """Test logging operations exist."""
        operations = [
            "write_log",
            "read_logs",
            "search_logs",
            "delete_logs",
            "export_logs",
            "get_log_levels",
            "set_log_level",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityLogging, operation)
            assert callable(getattr(FlextObservabilityLogging, operation))

    def test_logging_validation_methods(self) -> None:
        """Test logging validation methods exist."""
        validations = [
            "validate_log_message_length",
            "validate_log_level",
            "validate_log_tags",
            "validate_log_timestamp",
        ]
        for validation in validations:
            assert hasattr(FlextObservabilityLogging, validation)
            assert callable(getattr(FlextObservabilityLogging, validation))

    def test_logging_constants(self) -> None:
        """Test logging constants are defined."""
        constants = [
            "MAX_LOG_MESSAGE_LENGTH",
            "DEFAULT_LOG_LEVEL",
            "LOG_LEVEL_DEBUG",
            "LOG_LEVEL_INFO",
            "LOG_LEVEL_WARNING",
            "LOG_LEVEL_ERROR",
            "LOG_LEVEL_CRITICAL",
            "SUPPORTED_LOG_LEVELS",
        ]
        for constant in constants:
            assert hasattr(FlextObservabilityLogging, constant)
