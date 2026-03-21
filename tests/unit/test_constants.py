"""Unit tests for flext_observability.constants module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from flext_tests import u

from flext_observability import FlextObservabilityConstants


class TestFlextObservabilityConstants:
    """Test the FlextObservabilityConstants class."""

    def test_inherits_from_flext_constants(self) -> None:
        """Test that FlextObservabilityConstants inherits from FlextConstants."""
        u.Tests.Matchers.that(
            issubclass(FlextObservabilityConstants, FlextConstants), eq=True
        )

    def test_metric_constants(self) -> None:
        """Test metric-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "DEFAULT_METRIC_UNIT"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "METRIC_UNIT_COUNT"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "METRIC_UNIT_PERCENT"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "METRIC_UNIT_BYTES"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "METRIC_UNIT_SECONDS"), eq=True
        )

    def test_alert_constants(self) -> None:
        """Test alert-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "ALERT_LEVEL_INFO"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "ALERT_LEVEL_WARNING"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "ALERT_LEVEL_ERROR"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "ALERT_LEVEL_CRITICAL"), eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.ALERT_LEVEL_INFO == "info", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.ALERT_LEVEL_WARNING == "warning", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.ALERT_LEVEL_ERROR == "error", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.ALERT_LEVEL_CRITICAL == "critical", eq=True
        )

    def test_trace_constants(self) -> None:
        """Test trace-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "TRACE_STATUS_STARTED"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "TRACE_STATUS_RUNNING"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "TRACE_STATUS_COMPLETED"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "TRACE_STATUS_FAILED"), eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.TRACE_STATUS_STARTED == "started", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.TRACE_STATUS_RUNNING == "running", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.TRACE_STATUS_COMPLETED == "completed", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.TRACE_STATUS_FAILED == "failed", eq=True
        )

    def test_health_constants(self) -> None:
        """Test health-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "HEALTH_STATUS_HEALTHY"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "HEALTH_STATUS_DEGRADED"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "HEALTH_STATUS_UNHEALTHY"), eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.HEALTH_STATUS_HEALTHY == "healthy", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.HEALTH_STATUS_DEGRADED == "degraded", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.HEALTH_STATUS_UNHEALTHY == "unhealthy", eq=True
        )

    def test_log_constants(self) -> None:
        """Test logging-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "LOG_LEVEL_DEBUG"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "LOG_LEVEL_INFO"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "LOG_LEVEL_WARNING"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "LOG_LEVEL_ERROR"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "LOG_LEVEL_CRITICAL"), eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.LOG_LEVEL_DEBUG == "debug", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.LOG_LEVEL_INFO == "info", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.LOG_LEVEL_WARNING == "warning", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.LOG_LEVEL_ERROR == "error", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.LOG_LEVEL_CRITICAL == "critical", eq=True
        )

    def test_validation_constants(self) -> None:
        """Test validation-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "MAX_METRIC_NAME_LENGTH"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "MAX_TRACE_NAME_LENGTH"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "MAX_ALERT_MESSAGE_LENGTH"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "MAX_LOG_MESSAGE_LENGTH"), eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.MAX_METRIC_NAME_LENGTH > 0, eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.MAX_TRACE_NAME_LENGTH > 0, eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.MAX_ALERT_MESSAGE_LENGTH > 0, eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.MAX_LOG_MESSAGE_LENGTH > 0, eq=True
        )

    def test_service_constants(self) -> None:
        """Test service-related constants."""
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "DEFAULT_SERVICE_NAME"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "DEFAULT_ENVIRONMENT"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextObservabilityConstants, "DEFAULT_HEALTH_CHECK_INTERVAL"),
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.DEFAULT_SERVICE_NAME == "flext-observability",
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.DEFAULT_ENVIRONMENT == "development", eq=True
        )
        u.Tests.Matchers.that(
            FlextObservabilityConstants.DEFAULT_HEALTH_CHECK_INTERVAL > 0, eq=True
        )
