"""Behavioral tests for flext_observability.constants public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c

_Obs = c.Observability


class TestsFlextObservabilityConstantsUnit:
    """Public-contract behavior of the observability constants facade."""

    def test_facade_extends_flext_core_constants(self) -> None:
        """The facade must inherit the flext-core constants contract via MRO."""
        tm.that(c in c.__mro__, eq=True)

    @pytest.mark.parametrize(
        ("member", "expected"),
        [
            (_Obs.MetricType.COUNTER, "counter"),
            (_Obs.MetricType.GAUGE, "gauge"),
            (_Obs.MetricType.HISTOGRAM, "histogram"),
            (_Obs.MetricType.SUMMARY, "summary"),
            (_Obs.AlertLevel.INFO, "info"),
            (_Obs.AlertLevel.WARNING, "warning"),
            (_Obs.AlertLevel.ERROR, "error"),
            (_Obs.AlertLevel.CRITICAL, "critical"),
            (_Obs.TraceStatus.STARTED, "started"),
            (_Obs.TraceStatus.RUNNING, "running"),
            (_Obs.TraceStatus.COMPLETED, "completed"),
            (_Obs.TraceStatus.FAILED, "failed"),
            (_Obs.HealthStatus.HEALTHY, "healthy"),
            (_Obs.HealthStatus.DEGRADED, "degraded"),
            (_Obs.HealthStatus.UNHEALTHY, "unhealthy"),
            (_Obs.ErrorSeverity.DEBUG, "debug"),
            (_Obs.ErrorSeverity.CRITICAL, "critical"),
        ],
    )
    def test_strenum_members_carry_stable_string_values(
        self,
        member: str,
        expected: str,
    ) -> None:
        """Each StrEnum member is usable as its documented string value."""
        tm.that(member, eq=expected)

    @pytest.mark.parametrize(
        ("alias", "source"),
        [
            (_Obs.ALERT_LEVEL_INFO, _Obs.AlertLevel.INFO),
            (_Obs.ALERT_LEVEL_WARNING, _Obs.AlertLevel.WARNING),
            (_Obs.ALERT_LEVEL_ERROR, _Obs.AlertLevel.ERROR),
            (_Obs.ALERT_LEVEL_CRITICAL, _Obs.AlertLevel.CRITICAL),
            (_Obs.TRACE_STATUS_STARTED, _Obs.TraceStatus.STARTED),
            (_Obs.TRACE_STATUS_RUNNING, _Obs.TraceStatus.RUNNING),
            (_Obs.TRACE_STATUS_COMPLETED, _Obs.TraceStatus.COMPLETED),
            (_Obs.TRACE_STATUS_FAILED, _Obs.TraceStatus.FAILED),
            (_Obs.HEALTH_STATUS_HEALTHY, _Obs.HealthStatus.HEALTHY),
            (_Obs.HEALTH_STATUS_DEGRADED, _Obs.HealthStatus.DEGRADED),
            (_Obs.HEALTH_STATUS_UNHEALTHY, _Obs.HealthStatus.UNHEALTHY),
            (_Obs.LOG_LEVEL_DEBUG, _Obs.ErrorSeverity.DEBUG),
            (_Obs.LOG_LEVEL_INFO, _Obs.ErrorSeverity.INFO),
            (_Obs.LOG_LEVEL_WARNING, _Obs.ErrorSeverity.WARNING),
            (_Obs.LOG_LEVEL_ERROR, _Obs.ErrorSeverity.ERROR),
            (_Obs.LOG_LEVEL_CRITICAL, _Obs.ErrorSeverity.CRITICAL),
        ],
    )
    def test_flat_alias_stays_consistent_with_its_enum_source(
        self,
        alias: str,
        source: str,
    ) -> None:
        """Flat string aliases must equal the value of the enum they derive from."""
        tm.that(alias, eq=source)

    @pytest.mark.parametrize(
        "unit",
        [
            _Obs.METRIC_UNIT_COUNT,
            _Obs.METRIC_UNIT_PERCENT,
            _Obs.METRIC_UNIT_BYTES,
            _Obs.METRIC_UNIT_SECONDS,
        ],
    )
    def test_metric_unit_alias_is_a_recognized_valid_unit(self, unit: str) -> None:
        """Every exposed metric-unit alias belongs to the valid-units set."""
        tm.that(_Obs.METRIC_VALID_UNITS, has=unit)

    def test_strenum_values_are_unique_per_enum(self) -> None:
        """The @unique contract holds: no duplicate values within an enum."""
        for enum_cls in (
            _Obs.MetricType,
            _Obs.AlertLevel,
            _Obs.TraceStatus,
            _Obs.HealthStatus,
            _Obs.ErrorSeverity,
        ):
            values = [member.value for member in enum_cls]
            tm.that(len(set(values)), eq=len(values))

    @pytest.mark.parametrize(
        "length",
        [
            _Obs.MAX_METRIC_NAME_LENGTH,
            _Obs.MAX_TRACE_NAME_LENGTH,
            _Obs.MAX_ALERT_MESSAGE_LENGTH,
            _Obs.MAX_LOG_MESSAGE_LENGTH,
        ],
    )
    def test_validation_length_limits_are_positive(self, length: int) -> None:
        """All maximum-length limits are strictly positive bounds."""
        tm.that(length, gt=0)

    def test_message_limits_are_wider_than_name_limits(self) -> None:
        """Free-text message limits must exceed the stricter name limits."""
        tm.that(_Obs.MAX_ALERT_MESSAGE_LENGTH, gt=_Obs.MAX_METRIC_NAME_LENGTH)
        tm.that(_Obs.MAX_LOG_MESSAGE_LENGTH, gt=_Obs.MAX_TRACE_NAME_LENGTH)

    def test_service_defaults_expose_documented_values(self) -> None:
        """Default service identity constants match their published contract."""
        tm.that(_Obs.DEFAULT_SERVICE_NAME, eq="flext-service")
        tm.that(_Obs.DEFAULT_ENVIRONMENT, eq="development")
        tm.that(_Obs.DEFAULT_SETTINGS_SERVICE_NAME, eq="flext-observability")


__all__: list[str] = ["TestsFlextObservabilityConstantsUnit"]
