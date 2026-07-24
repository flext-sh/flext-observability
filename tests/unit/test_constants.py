"""Behavioral tests for flext_observability.constants public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c


class TestsFlextObservabilityConstantsUnit:
    """Public-contract behavior of the observability constants facade."""

    def test_facade_extends_flext_core_constants(self) -> None:
        """The facade must inherit the flext-core constants contract via MRO."""
        tm.that(c in c.__mro__, eq=True)

    @pytest.mark.parametrize(
        ("member", "expected"),
        [
            (c.Observability.MetricType.COUNTER, "counter"),
            (c.Observability.MetricType.GAUGE, "gauge"),
            (c.Observability.MetricType.HISTOGRAM, "histogram"),
            (c.Observability.MetricType.SUMMARY, "summary"),
            (c.Observability.AlertLevel.INFO, "info"),
            (c.Observability.AlertLevel.WARNING, "warning"),
            (c.Observability.AlertLevel.ERROR, "error"),
            (c.Observability.AlertLevel.CRITICAL, "critical"),
            (c.Observability.TraceStatus.STARTED, "started"),
            (c.Observability.TraceStatus.RUNNING, "running"),
            (c.Observability.TraceStatus.COMPLETED, "completed"),
            (c.Observability.TraceStatus.FAILED, "failed"),
            (c.Observability.HealthStatus.HEALTHY, "healthy"),
            (c.Observability.HealthStatus.DEGRADED, "degraded"),
            (c.Observability.HealthStatus.UNHEALTHY, "unhealthy"),
            (c.Observability.ErrorSeverity.DEBUG, "debug"),
            (c.Observability.ErrorSeverity.CRITICAL, "critical"),
        ],
    )
    def test_strenum_members_carry_stable_string_values(
        self, member: str, expected: str
    ) -> None:
        """Each StrEnum member is usable as its documented string value."""
        tm.that(member, eq=expected)

    @pytest.mark.parametrize(
        ("alias", "source"),
        [
            (c.Observability.ALERT_LEVEL_INFO, c.Observability.AlertLevel.INFO),
            (c.Observability.ALERT_LEVEL_WARNING, c.Observability.AlertLevel.WARNING),
            (c.Observability.ALERT_LEVEL_ERROR, c.Observability.AlertLevel.ERROR),
            (c.Observability.ALERT_LEVEL_CRITICAL, c.Observability.AlertLevel.CRITICAL),
            (c.Observability.TRACE_STATUS_STARTED, c.Observability.TraceStatus.STARTED),
            (c.Observability.TRACE_STATUS_RUNNING, c.Observability.TraceStatus.RUNNING),
            (
                c.Observability.TRACE_STATUS_COMPLETED,
                c.Observability.TraceStatus.COMPLETED,
            ),
            (c.Observability.TRACE_STATUS_FAILED, c.Observability.TraceStatus.FAILED),
            (
                c.Observability.HEALTH_STATUS_HEALTHY,
                c.Observability.HealthStatus.HEALTHY,
            ),
            (
                c.Observability.HEALTH_STATUS_DEGRADED,
                c.Observability.HealthStatus.DEGRADED,
            ),
            (
                c.Observability.HEALTH_STATUS_UNHEALTHY,
                c.Observability.HealthStatus.UNHEALTHY,
            ),
            (c.Observability.LOG_LEVEL_DEBUG, c.Observability.ErrorSeverity.DEBUG),
            (c.Observability.LOG_LEVEL_INFO, c.Observability.ErrorSeverity.INFO),
            (c.Observability.LOG_LEVEL_WARNING, c.Observability.ErrorSeverity.WARNING),
            (c.Observability.LOG_LEVEL_ERROR, c.Observability.ErrorSeverity.ERROR),
            (
                c.Observability.LOG_LEVEL_CRITICAL,
                c.Observability.ErrorSeverity.CRITICAL,
            ),
        ],
    )
    def test_flat_alias_stays_consistent_with_its_enum_source(
        self, alias: str, source: str
    ) -> None:
        """Flat string aliases must equal the value of the enum they derive from."""
        tm.that(alias, eq=source)

    @pytest.mark.parametrize(
        "unit",
        [
            c.Observability.METRIC_UNIT_COUNT,
            c.Observability.METRIC_UNIT_PERCENT,
            c.Observability.METRIC_UNIT_BYTES,
            c.Observability.METRIC_UNIT_SECONDS,
        ],
    )
    def test_metric_unit_alias_is_a_recognized_valid_unit(self, unit: str) -> None:
        """Every exposed metric-unit alias belongs to the valid-units set."""
        tm.that(c.Observability.METRIC_VALID_UNITS, has=unit)

    def test_strenum_values_are_unique_per_enum(self) -> None:
        """The @unique contract holds: no duplicate values within an enum."""
        for enum_cls in (
            c.Observability.MetricType,
            c.Observability.AlertLevel,
            c.Observability.TraceStatus,
            c.Observability.HealthStatus,
            c.Observability.ErrorSeverity,
        ):
            values = [member.value for member in enum_cls]
            tm.that(len(set(values)), eq=len(values))

    @pytest.mark.parametrize(
        "length",
        [
            c.Observability.MAX_METRIC_NAME_LENGTH,
            c.Observability.MAX_TRACE_NAME_LENGTH,
            c.Observability.MAX_ALERT_MESSAGE_LENGTH,
            c.Observability.MAX_LOG_MESSAGE_LENGTH,
        ],
    )
    def test_validation_length_limits_are_positive(self, length: int) -> None:
        """All maximum-length limits are strictly positive bounds."""
        tm.that(length, gt=0)

    def test_message_limits_are_wider_than_name_limits(self) -> None:
        """Free-text message limits must exceed the stricter name limits."""
        tm.that(
            c.Observability.MAX_ALERT_MESSAGE_LENGTH,
            gt=c.Observability.MAX_METRIC_NAME_LENGTH,
        )
        tm.that(
            c.Observability.MAX_LOG_MESSAGE_LENGTH,
            gt=c.Observability.MAX_TRACE_NAME_LENGTH,
        )

    def test_service_defaults_expose_documented_values(self) -> None:
        """Default service identity constants match their published contract."""
        tm.that(c.Observability.DEFAULT_SERVICE_NAME, eq="flext-service")
        tm.that(c.Observability.DEFAULT_ENVIRONMENT, eq="development")
        tm.that(c.Observability.DEFAULT_SETTINGS_SERVICE_NAME, eq="flext-observability")


__all__: list[str] = ["TestsFlextObservabilityConstantsUnit"]
