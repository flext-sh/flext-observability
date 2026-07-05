"""Behavioral tests for the flext-observability public API surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_core import FlextContainer, c as core_c
from flext_observability import (
    FlextObservability,
    __version__ as pkg_version,
    __version_info__ as pkg_version_info,
)
from tests.constants import c

__all__ = ["TestsFlextObservabilityInit"]

flext_alert = FlextObservability.flext_alert
flext_health_check = FlextObservability.flext_health_check
flext_metric = FlextObservability.flext_metric
flext_trace = FlextObservability.flext_trace
global_factory = FlextObservability.global_factory
clear_global_factory = FlextObservability.clear_global_factory


class TestsFlextObservabilityInit:
    """Public contract of the observability factory API and package exports."""

    def test_version_is_non_empty_string(self) -> None:
        """__version__ is a non-empty version string."""
        tm.that(pkg_version, is_=str)
        tm.that(bool(pkg_version), eq=True)

    def test_version_info_is_tuple_with_at_least_three_parts(self) -> None:
        """__version_info__ exposes at least major/minor/patch."""
        tm.that(pkg_version_info, is_=tuple)
        tm.that(len(pkg_version_info) >= 3, eq=True)

    def test_core_reexports_are_usable(self) -> None:
        """flext-core primitives are re-exported and usable through the package."""
        tm.that(callable(FlextContainer), eq=True)
        tm.that(core_c, none=False)

    @pytest.mark.parametrize(
        ("name", "value", "unit"),
        [
            ("requests", 1.0, "count"),
            ("latency", 12.5, "ms"),
            ("throughput", 3.0, "rps"),
        ],
    )
    def test_flext_metric_returns_metric_with_provided_state(
        self,
        name: str,
        value: float,
        unit: str,
    ) -> None:
        """flext_metric succeeds and exposes the supplied fields on the entity."""
        result = flext_metric(name, value, unit)

        tm.that(result.success, eq=True)
        metric = result.value
        tm.that(metric.name, eq=name)
        tm.that(metric.value, eq=value)
        tm.that(metric.unit, eq=unit)

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            ("", 1.0),
            ("valid", float("nan")),
        ],
    )
    def test_flext_metric_fails_on_invalid_input(
        self,
        name: str,
        value: float,
    ) -> None:
        """flext_metric reports failure with an error for invalid inputs."""
        result = flext_metric(name, value)

        tm.that(result.success, eq=False)
        tm.that(bool(result.error), eq=True)

    def test_flext_trace_generates_trace_id_when_absent(self) -> None:
        """flext_trace succeeds and synthesizes a non-empty trace id."""
        result = flext_trace("checkout")

        tm.that(result.success, eq=True)
        trace = result.value
        tm.that(trace.name, eq="checkout")
        tm.that(bool(trace.trace_id), eq=True)

    def test_flext_trace_preserves_explicit_trace_id(self) -> None:
        """A caller-supplied trace id is retained on the entity."""
        result = flext_trace("checkout", trace_id="trace-123")

        tm.that(result.success, eq=True)
        tm.that(result.value.trace_id, eq="trace-123")

    def test_flext_trace_fails_on_empty_name(self) -> None:
        """flext_trace rejects an empty name with a failure result."""
        result = flext_trace("")

        tm.that(result.success, eq=False)
        tm.that(bool(result.error), eq=True)

    def test_flext_alert_applies_defaults_and_provided_fields(self) -> None:
        """flext_alert builds an alert with supplied title/message and defaults."""
        result = flext_alert(title="Disk full", message="Root volume at 95%")

        tm.that(result.success, eq=True)
        alert = result.value
        tm.that(alert.title, eq="Disk full")
        tm.that(alert.message, eq="Root volume at 95%")
        tm.that(bool(alert.severity), eq=True)

    @pytest.mark.parametrize(
        "status",
        [
            c.Observability.HealthStatus.HEALTHY,
            c.Observability.HealthStatus.DEGRADED,
            c.Observability.HealthStatus.UNHEALTHY,
        ],
    )
    def test_flext_health_check_records_component_and_status(
        self,
        status: c.Observability.HealthStatus,
    ) -> None:
        """flext_health_check echoes the component and status on the entity."""
        result = flext_health_check("flext-observability", status)

        tm.that(result.success, eq=True)
        health = result.value
        tm.that(health.component, eq="flext-observability")
        tm.that(health.status, eq=status.value)

    def test_flext_health_check_fails_on_empty_component(self) -> None:
        """flext_health_check rejects an empty component name."""
        result = flext_health_check("")

        tm.that(result.success, eq=False)
        tm.that(bool(result.error), eq=True)

    def test_global_factory_is_idempotent(self) -> None:
        """global_factory returns the same instance until it is cleared."""
        clear_global_factory()
        first = global_factory()
        second = global_factory()

        tm.that(first is second, eq=True)

    def test_clear_global_factory_forces_a_fresh_instance(self) -> None:
        """clear_global_factory resets the cached instance."""
        clear_global_factory()
        original = global_factory()
        clear_global_factory()
        replacement = global_factory()

        tm.that(replacement is original, eq=False)
