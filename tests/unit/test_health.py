"""Unit tests for flext_observability.health module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityHealth


class TestFlextObservabilityHealth:
    """Test the FlextObservabilityHealth class."""

    def test_inherits_from_flext_models(self) -> None:
        """Test that FlextObservabilityHealth inherits from FlextCore.Models."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityHealth, FlextCore.Models)

    def test_flext_health_check_class_exists(self) -> None:
        """Test that FlextHealthCheck class exists."""
        assert hasattr(FlextObservabilityHealth, "FlextHealthCheck")

    def test_health_factory_methods(self) -> None:
        """Test health factory methods exist."""
        methods = [
            "flext_health_check",
            "create_database_health_check",
            "create_service_health_check",
            "create_system_health_check",
            "validate_health_check_name",
            "validate_health_status",
        ]
        for method in methods:
            assert hasattr(FlextObservabilityHealth, method)
            assert callable(getattr(FlextObservabilityHealth, method))

    def test_health_operations(self) -> None:
        """Test health operations exist."""
        operations = [
            "execute_health_check",
            "register_health_check",
            "unregister_health_check",
            "get_health_status",
            "list_health_checks",
            "update_health_check",
            "run_all_health_checks",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityHealth, operation)
            assert callable(getattr(FlextObservabilityHealth, operation))

    def test_health_validation_methods(self) -> None:
        """Test health validation methods exist."""
        validations = [
            "validate_health_check_name_length",
            "validate_health_status",
            "validate_health_check_interval",
            "validate_health_check_timeout",
        ]
        for validation in validations:
            assert hasattr(FlextObservabilityHealth, validation)
            assert callable(getattr(FlextObservabilityHealth, validation))

    def test_health_constants(self) -> None:
        """Test health constants are defined."""
        constants = [
            "DEFAULT_HEALTH_CHECK_INTERVAL",
            "DEFAULT_HEALTH_CHECK_TIMEOUT",
            "HEALTH_STATUS_HEALTHY",
            "HEALTH_STATUS_DEGRADED",
            "HEALTH_STATUS_UNHEALTHY",
            "SUPPORTED_HEALTH_STATUSES",
        ]
        for constant in constants:
            assert hasattr(FlextObservabilityHealth, constant)
