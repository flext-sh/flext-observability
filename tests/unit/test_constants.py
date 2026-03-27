"""Unit tests for flext_observability.constants module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from flext_tests import tm

from flext_observability import FlextObservabilityConstants


class TestFlextObservabilityConstants:
    """Test the FlextObservabilityConstants class."""

    def test_inherits_from_flext_constants(self) -> None:
        """Test that FlextObservabilityConstants inherits from FlextConstants."""
        tm.that(FlextConstants in FlextObservabilityConstants.__mro__, eq=True)

    def test_metric_constants(self) -> None:
        """Test metric-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(obs.METRIC_UNIT_COUNT, eq="count")
        tm.that(obs.METRIC_UNIT_PERCENT, eq="percent")
        tm.that(obs.METRIC_UNIT_BYTES, eq="bytes")
        tm.that(obs.METRIC_UNIT_SECONDS, eq="seconds")

    def test_alert_constants(self) -> None:
        """Test alert-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs, "ALERT_LEVEL_INFO"), eq=True)
        tm.that(hasattr(obs, "ALERT_LEVEL_WARNING"), eq=True)
        tm.that(hasattr(obs, "ALERT_LEVEL_ERROR"), eq=True)
        tm.that(hasattr(obs, "ALERT_LEVEL_CRITICAL"), eq=True)
        tm.that(FlextObservabilityConstants.Observability.ALERT_LEVEL_INFO, eq="info")
        tm.that(
            FlextObservabilityConstants.Observability.ALERT_LEVEL_WARNING, eq="warning"
        )
        tm.that(FlextObservabilityConstants.Observability.ALERT_LEVEL_ERROR, eq="error")
        tm.that(
            FlextObservabilityConstants.Observability.ALERT_LEVEL_CRITICAL,
            eq="critical",
        )

    def test_trace_constants(self) -> None:
        """Test trace-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs, "TRACE_STATUS_STARTED"), eq=True)
        tm.that(hasattr(obs, "TRACE_STATUS_RUNNING"), eq=True)
        tm.that(hasattr(obs, "TRACE_STATUS_COMPLETED"), eq=True)
        tm.that(hasattr(obs, "TRACE_STATUS_FAILED"), eq=True)
        tm.that(
            FlextObservabilityConstants.Observability.TRACE_STATUS_STARTED, eq="started"
        )
        tm.that(
            FlextObservabilityConstants.Observability.TRACE_STATUS_RUNNING, eq="running"
        )
        tm.that(
            FlextObservabilityConstants.Observability.TRACE_STATUS_COMPLETED,
            eq="completed",
        )
        tm.that(
            FlextObservabilityConstants.Observability.TRACE_STATUS_FAILED, eq="failed"
        )

    def test_health_constants(self) -> None:
        """Test health-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs, "HEALTH_STATUS_HEALTHY"), eq=True)
        tm.that(hasattr(obs, "HEALTH_STATUS_DEGRADED"), eq=True)
        tm.that(hasattr(obs, "HEALTH_STATUS_UNHEALTHY"), eq=True)
        tm.that(
            FlextObservabilityConstants.Observability.HEALTH_STATUS_HEALTHY,
            eq="healthy",
        )
        tm.that(
            FlextObservabilityConstants.Observability.HEALTH_STATUS_DEGRADED,
            eq="degraded",
        )
        tm.that(
            FlextObservabilityConstants.Observability.HEALTH_STATUS_UNHEALTHY,
            eq="unhealthy",
        )

    def test_log_constants(self) -> None:
        """Test logging-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs, "LOG_LEVEL_DEBUG"), eq=True)
        tm.that(hasattr(obs, "LOG_LEVEL_INFO"), eq=True)
        tm.that(hasattr(obs, "LOG_LEVEL_WARNING"), eq=True)
        tm.that(hasattr(obs, "LOG_LEVEL_ERROR"), eq=True)
        tm.that(hasattr(obs, "LOG_LEVEL_CRITICAL"), eq=True)
        tm.that(FlextObservabilityConstants.Observability.LOG_LEVEL_DEBUG, eq="debug")
        tm.that(FlextObservabilityConstants.Observability.LOG_LEVEL_INFO, eq="info")
        tm.that(
            FlextObservabilityConstants.Observability.LOG_LEVEL_WARNING, eq="warning"
        )
        tm.that(FlextObservabilityConstants.Observability.LOG_LEVEL_ERROR, eq="error")
        tm.that(
            FlextObservabilityConstants.Observability.LOG_LEVEL_CRITICAL, eq="critical"
        )

    def test_validation_constants(self) -> None:
        """Test validation-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs, "MAX_METRIC_NAME_LENGTH"), eq=True)
        tm.that(hasattr(obs, "MAX_TRACE_NAME_LENGTH"), eq=True)
        tm.that(hasattr(obs, "MAX_ALERT_MESSAGE_LENGTH"), eq=True)
        tm.that(hasattr(obs, "MAX_LOG_MESSAGE_LENGTH"), eq=True)
        tm.that(FlextObservabilityConstants.Observability.MAX_METRIC_NAME_LENGTH, gt=0)
        tm.that(FlextObservabilityConstants.Observability.MAX_TRACE_NAME_LENGTH, gt=0)
        tm.that(
            FlextObservabilityConstants.Observability.MAX_ALERT_MESSAGE_LENGTH, gt=0
        )
        tm.that(FlextObservabilityConstants.Observability.MAX_LOG_MESSAGE_LENGTH, gt=0)

    def test_service_constants(self) -> None:
        """Test service-related constants."""
        obs = FlextObservabilityConstants.Observability
        tm.that(hasattr(obs.Defaults, "DEFAULT_SERVICE_NAME"), eq=True)
        tm.that(hasattr(obs, "DEFAULT_ENVIRONMENT"), eq=True)
        tm.that(
            FlextObservabilityConstants.Observability.Defaults.DEFAULT_SERVICE_NAME,
            eq="flext-service",
        )
        tm.that(
            FlextObservabilityConstants.Observability.DEFAULT_ENVIRONMENT,
            eq="development",
        )
