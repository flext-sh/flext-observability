"""Unit tests for flext_observability.constants module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from flext_tests import tm

from tests import c


class TestsFlextObservabilityConstantsUnit:
    """Test the c class."""

    def test_inherits_from_flext_constants(self) -> None:
        """Test that c inherits from FlextConstants."""
        tm.that(FlextConstants in c.__mro__, eq=True)

    def test_metric_constants(self) -> None:
        """Test metric-related constants."""
        obs = c.Observability
        tm.that(obs.METRIC_UNIT_COUNT, eq="count")
        tm.that(obs.METRIC_UNIT_PERCENT, eq="percent")
        tm.that(obs.METRIC_UNIT_BYTES, eq="bytes")
        tm.that(obs.METRIC_UNIT_SECONDS, eq="seconds")

    def test_alert_constants(self) -> None:
        """Test alert-related constants."""
        tm.that(c.Observability.ALERT_LEVEL_INFO, eq="info")
        tm.that(c.Observability.ALERT_LEVEL_WARNING, eq="warning")
        tm.that(c.Observability.ALERT_LEVEL_ERROR, eq="error")
        tm.that(
            c.Observability.ALERT_LEVEL_CRITICAL,
            eq="critical",
        )

    def test_trace_constants(self) -> None:
        """Test trace-related constants."""
        tm.that(c.Observability.TRACE_STATUS_STARTED, eq="started")
        tm.that(c.Observability.TRACE_STATUS_RUNNING, eq="running")
        tm.that(
            c.Observability.TRACE_STATUS_COMPLETED,
            eq="completed",
        )
        tm.that(c.Observability.TRACE_STATUS_FAILED, eq="failed")

    def test_health_constants(self) -> None:
        """Test health-related constants."""
        tm.that(
            c.Observability.HEALTH_STATUS_HEALTHY,
            eq="healthy",
        )
        tm.that(
            c.Observability.HEALTH_STATUS_DEGRADED,
            eq="degraded",
        )
        tm.that(
            c.Observability.HEALTH_STATUS_UNHEALTHY,
            eq="unhealthy",
        )

    def test_log_constants(self) -> None:
        """Test logging-related constants."""
        tm.that(c.Observability.LOG_LEVEL_DEBUG, eq="debug")
        tm.that(c.Observability.LOG_LEVEL_INFO, eq="info")
        tm.that(c.Observability.LOG_LEVEL_WARNING, eq="warning")
        tm.that(c.Observability.LOG_LEVEL_ERROR, eq="error")
        tm.that(c.Observability.LOG_LEVEL_CRITICAL, eq="critical")

    def test_validation_constants(self) -> None:
        """Test validation-related constants."""
        tm.that(c.Observability.MAX_METRIC_NAME_LENGTH, gt=0)
        tm.that(c.Observability.MAX_TRACE_NAME_LENGTH, gt=0)
        tm.that(c.Observability.MAX_ALERT_MESSAGE_LENGTH, gt=0)
        tm.that(c.Observability.MAX_LOG_MESSAGE_LENGTH, gt=0)

    def test_service_constants(self) -> None:
        """Test service-related constants."""
        tm.that(
            c.Observability.Defaults.DEFAULT_SERVICE_NAME,
            eq="flext-service",
        )
        tm.that(
            c.Observability.DEFAULT_ENVIRONMENT,
            eq="development",
        )
