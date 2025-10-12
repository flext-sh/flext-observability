"""Unit tests for flext_observability.constants module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityConstants


class TestFlextObservabilityConstants:
    """Test the FlextObservabilityConstants class."""

    def test_inherits_from_flext_constants(self) -> None:
        """Test that FlextObservabilityConstants inherits from FlextCore.Constants."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityConstants, FlextCore.Constants)

    def test_metric_constants(self) -> None:
        """Test metric-related constants."""
        assert hasattr(FlextObservabilityConstants, "DEFAULT_METRIC_UNIT")
        assert hasattr(FlextObservabilityConstants, "METRIC_UNIT_COUNT")
        assert hasattr(FlextObservabilityConstants, "METRIC_UNIT_PERCENT")
        assert hasattr(FlextObservabilityConstants, "METRIC_UNIT_BYTES")
        assert hasattr(FlextObservabilityConstants, "METRIC_UNIT_SECONDS")

    def test_alert_constants(self) -> None:
        """Test alert-related constants."""
        assert hasattr(FlextObservabilityConstants, "ALERT_LEVEL_INFO")
        assert hasattr(FlextObservabilityConstants, "ALERT_LEVEL_WARNING")
        assert hasattr(FlextObservabilityConstants, "ALERT_LEVEL_ERROR")
        assert hasattr(FlextObservabilityConstants, "ALERT_LEVEL_CRITICAL")

        # Test specific values
        assert FlextObservabilityConstants.ALERT_LEVEL_INFO == "info"
        assert FlextObservabilityConstants.ALERT_LEVEL_WARNING == "warning"
        assert FlextObservabilityConstants.ALERT_LEVEL_ERROR == "error"
        assert FlextObservabilityConstants.ALERT_LEVEL_CRITICAL == "critical"

    def test_trace_constants(self) -> None:
        """Test trace-related constants."""
        assert hasattr(FlextObservabilityConstants, "TRACE_STATUS_STARTED")
        assert hasattr(FlextObservabilityConstants, "TRACE_STATUS_RUNNING")
        assert hasattr(FlextObservabilityConstants, "TRACE_STATUS_COMPLETED")
        assert hasattr(FlextObservabilityConstants, "TRACE_STATUS_FAILED")

        # Test specific values
        assert FlextObservabilityConstants.TRACE_STATUS_STARTED == "started"
        assert FlextObservabilityConstants.TRACE_STATUS_RUNNING == "running"
        assert FlextObservabilityConstants.TRACE_STATUS_COMPLETED == "completed"
        assert FlextObservabilityConstants.TRACE_STATUS_FAILED == "failed"

    def test_health_constants(self) -> None:
        """Test health-related constants."""
        assert hasattr(FlextObservabilityConstants, "HEALTH_STATUS_HEALTHY")
        assert hasattr(FlextObservabilityConstants, "HEALTH_STATUS_DEGRADED")
        assert hasattr(FlextObservabilityConstants, "HEALTH_STATUS_UNHEALTHY")

        # Test specific values
        assert FlextObservabilityConstants.HEALTH_STATUS_HEALTHY == "healthy"
        assert FlextObservabilityConstants.HEALTH_STATUS_DEGRADED == "degraded"
        assert FlextObservabilityConstants.HEALTH_STATUS_UNHEALTHY == "unhealthy"

    def test_log_constants(self) -> None:
        """Test logging-related constants."""
        assert hasattr(FlextObservabilityConstants, "LOG_LEVEL_DEBUG")
        assert hasattr(FlextObservabilityConstants, "LOG_LEVEL_INFO")
        assert hasattr(FlextObservabilityConstants, "LOG_LEVEL_WARNING")
        assert hasattr(FlextObservabilityConstants, "LOG_LEVEL_ERROR")
        assert hasattr(FlextObservabilityConstants, "LOG_LEVEL_CRITICAL")

        # Test specific values
        assert FlextObservabilityConstants.LOG_LEVEL_DEBUG == "debug"
        assert FlextObservabilityConstants.LOG_LEVEL_INFO == "info"
        assert FlextObservabilityConstants.LOG_LEVEL_WARNING == "warning"
        assert FlextObservabilityConstants.LOG_LEVEL_ERROR == "error"
        assert FlextObservabilityConstants.LOG_LEVEL_CRITICAL == "critical"

    def test_validation_constants(self) -> None:
        """Test validation-related constants."""
        assert hasattr(FlextObservabilityConstants, "MAX_METRIC_NAME_LENGTH")
        assert hasattr(FlextObservabilityConstants, "MAX_TRACE_NAME_LENGTH")
        assert hasattr(FlextObservabilityConstants, "MAX_ALERT_MESSAGE_LENGTH")
        assert hasattr(FlextObservabilityConstants, "MAX_LOG_MESSAGE_LENGTH")

        # Test reasonable limits
        assert FlextObservabilityConstants.MAX_METRIC_NAME_LENGTH > 0
        assert FlextObservabilityConstants.MAX_TRACE_NAME_LENGTH > 0
        assert FlextObservabilityConstants.MAX_ALERT_MESSAGE_LENGTH > 0
        assert FlextObservabilityConstants.MAX_LOG_MESSAGE_LENGTH > 0

    def test_service_constants(self) -> None:
        """Test service-related constants."""
        assert hasattr(FlextObservabilityConstants, "DEFAULT_SERVICE_NAME")
        assert hasattr(FlextObservabilityConstants, "DEFAULT_ENVIRONMENT")
        assert hasattr(FlextObservabilityConstants, "DEFAULT_HEALTH_CHECK_INTERVAL")

        assert FlextObservabilityConstants.DEFAULT_SERVICE_NAME == "flext-observability"
        assert FlextObservabilityConstants.DEFAULT_ENVIRONMENT == "development"
        assert FlextObservabilityConstants.DEFAULT_HEALTH_CHECK_INTERVAL > 0
