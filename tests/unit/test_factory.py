"""Behavioral tests for the FlextObservability facade creation contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

These tests assert observable public behavior only: the ``r[T]`` outcome of the
facade's fallible creation methods, the public model fields of the produced
entities, and the error messages returned on invalid input. No private
attributes, no internal-collaborator spying, no monkeypatching of the unit
under test.

The ``FlextObservabilityMasterFactory`` class was retired; the canonical
creation surface is now the ``FlextObservability`` facade itself
(``flext_metric`` / ``flext_alert`` / ``flext_log_entry`` / ``flext_trace`` /
``flext_health_check``), constructed with an optional container.
"""

from __future__ import annotations

from datetime import datetime

from flext_tests import tm

from flext_core import FlextContainer
from flext_observability import FlextObservability, c, p

__all__ = ["TestsFlextObservabilityFactory"]


class TestsFlextObservabilityFactory:
    """Behavioral contract tests for the observability facade creation API."""

    # -- construction / container contract ---------------------------------

    def test_container_passed_at_construction_is_exposed(self) -> None:
        """The container supplied at construction is the one the facade exposes."""
        container = FlextContainer()
        facade = FlextObservability(container)
        tm.that(facade.container is container, eq=True)

    def test_facade_constructs_with_default_container(self) -> None:
        """Constructing without a container still yields a usable facade."""
        facade = FlextObservability()
        tm.that(facade.container, none=False)

    # -- metric ------------------------------------------------------------

    def test_flext_metric_returns_metric_with_public_fields(self) -> None:
        """A valid metric request succeeds and echoes name, value and unit."""
        result = FlextObservability().flext_metric("test_metric", 42.5, "gauge")
        tm.that(result.success, eq=True)
        metric = result.value
        tm.that(metric.name, eq="test_metric")
        tm.that(abs(metric.value - 42.5), lt=1e-9)
        tm.that(metric.unit, eq="gauge")

    def test_flext_metric_defaults_unit_to_count(self) -> None:
        """Omitting the unit produces the canonical default unit."""
        result = FlextObservability().flext_metric("cpu_usage", 85.2)
        tm.that(result.success, eq=True)
        metric = result.value
        tm.that(metric.name, eq="cpu_usage")
        tm.that(abs(metric.value - 85.2), lt=1e-9)
        tm.that(metric.unit, eq="count")

    def test_flext_metric_empty_name_fails_with_message(self) -> None:
        """An empty metric name is rejected as a failure result, not a raise."""
        result = FlextObservability().flext_metric("", 10.0)
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="must be non-empty string")

    def test_flext_metric_repeatable_with_distinct_identity(self) -> None:
        """Repeating a metric request yields equal fields but distinct identity."""
        facade = FlextObservability()
        first = facade.flext_metric("cpu", 50.0).value
        second = facade.flext_metric("cpu", 50.0).value
        tm.that(first.name, eq=second.name)
        tm.that(abs(first.value - second.value), lt=1e-9)
        tm.that(first.unique_id != second.unique_id, eq=True)

    # -- log ---------------------------------------------------------------

    def test_flext_log_entry_creates_entry_with_message(self) -> None:
        """A valid log message produces a log entry echoing the message."""
        result = FlextObservability().flext_log_entry("hello world")
        tm.that(result.success, eq=True)
        tm.that(result.value.message, eq="hello world")

    def test_flext_log_entry_empty_message_fails_with_message(self) -> None:
        """An empty log message is rejected before model construction."""
        result = FlextObservability().flext_log_entry("")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Log message cannot be empty")

    # -- alert -------------------------------------------------------------

    def test_flext_alert_builds_alert_with_explicit_title(self) -> None:
        """``flext_alert`` keeps the explicit title, message and severity."""
        result = FlextObservability().flext_alert(
            title="Alert: monitoring",
            message="Critical error detected",
            severity="critical",
        )
        tm.that(result.success, eq=True)
        alert = result.value
        tm.that(alert.title, eq="Alert: monitoring")
        tm.that(alert.message, eq="Critical error detected")
        tm.that(alert.severity, eq="critical")

    # -- trace -------------------------------------------------------------

    def test_flext_trace_returns_named_trace_with_id(self) -> None:
        """A trace request succeeds with the operation name and a non-empty id."""
        result = FlextObservability().flext_trace("user_authentication")
        tm.that(result.success, eq=True)
        trace = result.value
        tm.that(trace.name, eq="user_authentication")
        tm.that(trace.trace_id, ne="")

    def test_flext_trace_preserves_explicit_trace_id(self) -> None:
        """An explicit trace_id is preserved on the produced trace."""
        result = FlextObservability().flext_trace("api_request", trace_id="trace-123")
        tm.that(result.success, eq=True)
        trace = result.value
        tm.that(trace.name, eq="api_request")
        tm.that(trace.trace_id, eq="trace-123")

    def test_flext_trace_empty_name_fails_with_message(self) -> None:
        """An empty trace name is rejected as a failure result."""
        result = FlextObservability().flext_trace("")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="must be non-empty string")

    # -- health ------------------------------------------------------------

    def test_flext_health_check_returns_component_status(self) -> None:
        """A health check request succeeds with the component and status."""
        result = FlextObservability().flext_health_check(
            "database", c.Observability.HealthStatus.HEALTHY
        )
        tm.that(result.success, eq=True)
        health = result.value
        tm.that(health.component, eq="database")
        tm.that(health.status, eq="healthy")

    def test_flext_health_check_empty_component_fails_with_message(self) -> None:
        """An empty component name is rejected as a failure result."""
        result = FlextObservability().flext_health_check("")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Component name cannot be empty")

    # -- cross-entity invariants -------------------------------------------

    def test_created_metric_exposes_datetime_creation_timestamp(self) -> None:
        """A successfully created metric exposes a datetime ``created_at``."""
        result: p.Result[FlextObservability.Metric] = FlextObservability().flext_metric(
            "request_count", 100.0, "counter"
        )
        tm.that(result.success, eq=True)
        created_at = result.value.model_dump()["created_at"]
        tm.that(created_at, is_=datetime)

    def test_invalid_metric_input_returns_failure_with_expected_message(self) -> None:
        """An invalid metric request surfaces a descriptive failure result."""
        result: p.Result[FlextObservability.Metric] = FlextObservability().flext_metric(
            "", 10.0
        )
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="must be non-empty string")
