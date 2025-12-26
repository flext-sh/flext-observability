"""Unit tests for flext_observability.alerting module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_core import FlextModels

from flext_observability import FlextObservabilityAlerting


class TestFlextObservabilityAlerting:
    """Test the FlextObservabilityAlerting class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityAlerting inherits from FlextModels."""
        assert issubclass(FlextObservabilityAlerting, FlextModels)

    def test_flext_alert_class_exists(self) -> None:
        """Test that FlextAlert class exists."""
        assert hasattr(FlextObservabilityAlerting, "FlextAlert")

    def test_alert_factory_methods(self) -> None:
        """Test alert factory methods exist."""
        methods = [
            "flext_alert",
            "create_info_alert",
            "create_warning_alert",
            "create_error_alert",
            "create_critical_alert",
            "validate_alert_message",
            "validate_alert_level",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityAlerting, method)
            assert callable(getattr(FlextObservabilityAlerting, method))

    def test_alert_operations(self) -> None:
        """Test alert operations exist."""
        operations = [
            "trigger_alert",
            "resolve_alert",
            "escalate_alert",
            "acknowledge_alert",
            "get_alert",
            "list_alerts",
            "delete_alert",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityAlerting, operation)
            assert callable(getattr(FlextObservabilityAlerting, operation))

    def test_alert_validation_methods(self) -> None:
        """Test alert validation methods exist."""
        validations = [
            "validate_alert_message_length",
            "validate_alert_level",
            "validate_alert_tags",
            "validate_alert_timestamp",
        ]
        for validation in validations:
            assert hasattr(FlextObservabilityAlerting, validation)
            assert callable(getattr(FlextObservabilityAlerting, validation))

    def test_alert_constants(self) -> None:
        """Test alert constants are defined."""
        constants = [
            "MAX_ALERT_MESSAGE_LENGTH",
            "DEFAULT_ALERT_LEVEL",
            "SUPPORTED_ALERT_LEVELS",
            "ALERT_STATUS_ACTIVE",
            "ALERT_STATUS_RESOLVED",
            "ALERT_STATUS_ESCALATED",
        ]
        for constant in constants:
            assert hasattr(FlextObservabilityAlerting, constant)
