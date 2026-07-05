"""Behavioral tests for FlextObservabilityMasterFactory public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

These tests assert observable public behavior only: the ``r[T]`` outcome of the
factory's fallible creation methods, the public model fields of the produced
entities, and the error messages returned on invalid input. No private
attributes, no internal-collaborator spying, no monkeypatching of the unit
under test.

NOTE (honest scope limit): the *success* path of ``create_log_entry`` /
``log`` cannot currently be exercised through the public API because the
source ``FlextObservability.LogEntry`` model is not fully defined at runtime
(``PydanticUserError: LogEntry is not fully defined`` / unresolved
``Annotated`` forward reference). This is a pre-existing SRC defect outside
this file's editable scope. The verifiable log behavior -- input validation,
which runs *before* model construction -- is covered below; the blocked
success path is documented here rather than faked.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

import pytest
from flext_tests import tm

from flext_core import FlextContainer, p, r
from flext_observability import FlextObservability

__all__ = ["TestsFlextObservabilityFactory"]

_Factory = FlextObservability.FlextObservabilityMasterFactory


class TestsFlextObservabilityFactory:
    """Behavioral contract tests for the observability master factory."""

    # -- construction / container contract ---------------------------------

    def test_container_passed_at_construction_is_exposed(self) -> None:
        """The container supplied at construction is the one the factory exposes."""
        container = FlextContainer()
        factory = _Factory(container)
        tm.that(factory.container is container, eq=True)

    def test_factory_constructs_with_default_container(self) -> None:
        """Constructing without a container still yields a usable factory."""
        factory = _Factory()
        tm.that(factory.container, none=False)

    # -- metric ------------------------------------------------------------

    def test_create_metric_returns_metric_with_public_fields(self) -> None:
        """A valid metric request succeeds and echoes name, value and unit."""
        result = _Factory().create_metric("test_metric", 42.5, "gauge")
        tm.that(result.success, eq=True)
        metric = result.value
        tm.that(metric.name, eq="test_metric")
        tm.that(abs(metric.value - 42.5), lt=1e-9)
        tm.that(metric.unit, eq="gauge")

    def test_metric_shorthand_matches_create_metric_contract(self) -> None:
        """The ``metric`` shorthand produces the same public contract."""
        result = _Factory().metric("cpu_usage", 85.2)
        tm.that(result.success, eq=True)
        metric = result.value
        tm.that(metric.name, eq="cpu_usage")
        tm.that(abs(metric.value - 85.2), lt=1e-9)

    def test_create_metric_empty_name_fails_with_message(self) -> None:
        """An empty metric name is rejected as a failure result, not a raise."""
        result = _Factory().create_metric("", 10.0)
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="must be non-empty string")

    def test_metric_creation_is_repeatable_with_distinct_identity(self) -> None:
        """Repeating a metric request yields equal public fields but distinct identity."""
        factory = _Factory()
        first = factory.create_metric("cpu", 50.0).value
        second = factory.create_metric("cpu", 50.0).value
        tm.that(first.name, eq=second.name)
        tm.that(abs(first.value - second.value), lt=1e-9)
        tm.that(first.unique_id != second.unique_id, eq=True)

    # -- log (validation path only; success path blocked by SRC defect) ----

    def test_create_log_entry_empty_message_fails_with_message(self) -> None:
        """An empty log message is rejected before model construction."""
        result = _Factory().create_log_entry("")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Log message cannot be empty")

    # -- alert -------------------------------------------------------------

    def test_create_alert_builds_titled_alert(self) -> None:
        """``create_alert`` derives the title from the service and keeps the message."""
        result = _Factory().create_alert(
            "Critical error detected", "monitoring", "critical"
        )
        tm.that(result.success, eq=True)
        alert = result.value
        tm.that(alert.title, eq="Alert: monitoring")
        tm.that(alert.message, eq="Critical error detected")
        tm.that(alert.severity, eq="critical")

    def test_alert_shorthand_uses_explicit_title_and_message(self) -> None:
        """The ``alert`` shorthand takes title and message positionally."""
        result = _Factory().alert("High memory usage", "monitoring")
        tm.that(result.success, eq=True)
        alert = result.value
        tm.that(alert.title, eq="High memory usage")
        tm.that(alert.message, eq="monitoring")

    @pytest.mark.parametrize(
        ("severity_in", "severity_out"),
        [
            ("low", "info"),
            ("medium", "warning"),
            ("high", "error"),
            ("critical", "critical"),
            ("info", "info"),
            ("unrecognized", "warning"),
        ],
    )
    def test_alert_severity_is_normalized(
        self, severity_in: str, severity_out: str
    ) -> None:
        """Alert severity aliases normalize to the canonical severity level."""
        result = _Factory().create_alert("msg", "svc", severity_in)
        tm.that(result.success, eq=True)
        tm.that(result.value.severity, eq=severity_out)

    # -- trace -------------------------------------------------------------

    def test_create_trace_returns_named_trace_with_id(self) -> None:
        """A trace request succeeds with the operation name and a non-empty id."""
        result = _Factory().create_trace("user_authentication", "auth_service")
        tm.that(result.success, eq=True)
        trace = result.value
        tm.that(trace.name, eq="user_authentication")
        tm.that(trace.trace_id, ne="")

    def test_trace_shorthand_sets_explicit_trace_id(self) -> None:
        """The ``trace`` shorthand takes trace_id and operation positionally."""
        result = _Factory().trace("trace-123", "api_request")
        tm.that(result.success, eq=True)
        trace = result.value
        tm.that(trace.name, eq="api_request")
        tm.that(trace.trace_id, eq="trace-123")

    def test_create_trace_empty_operation_fails_with_message(self) -> None:
        """An empty trace operation is rejected as a failure result."""
        result = _Factory().create_trace("", "service")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="must be non-empty string")

    # -- health ------------------------------------------------------------

    def test_create_health_check_returns_component_status(self) -> None:
        """A health check request succeeds with the component and status."""
        result = _Factory().create_health_check("database", "healthy")
        tm.that(result.success, eq=True)
        health = result.value
        tm.that(health.component, eq="database")
        tm.that(health.status, eq="healthy")

    def test_create_health_check_empty_component_fails_with_message(self) -> None:
        """An empty component name is rejected as a failure result."""
        result = _Factory().create_health_check("")
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Component name cannot be empty")

    def test_health_status_reports_system_component(self) -> None:
        """``health_status`` reports the overall ``system`` component health."""
        result = _Factory().health_status()
        tm.that(result.success, eq=True)
        tm.that(result.value.component, eq="system")

    # -- cross-entity invariants -------------------------------------------

    @pytest.mark.parametrize(
        "creator",
        [
            lambda f: f.create_metric("request_count", 100.0, "counter"),
            lambda f: f.create_alert("High request count", "monitoring", "medium"),
            lambda f: f.create_trace("process_request", "api_service"),
            lambda f: f.create_health_check("api_service", "healthy"),
        ],
    )
    def test_created_entities_expose_datetime_creation_timestamp(
        self,
        creator: Callable[
            [FlextObservability.FlextObservabilityMasterFactory],
            r[p.HasModelDump],
        ],
    ) -> None:
        """Every successfully created entity exposes a datetime ``created_at``."""
        result = creator(_Factory())
        tm.that(result.success, eq=True)
        entity = result.value
        created_at = entity.model_dump()["created_at"]
        tm.that(created_at, is_=datetime)

    @pytest.mark.parametrize(
        ("creator", "expected_error"),
        [
            (lambda f: f.create_metric("", 10.0), "must be non-empty string"),
            (lambda f: f.create_log_entry(""), "Log message cannot be empty"),
            (lambda f: f.create_trace("", "service"), "must be non-empty string"),
            (lambda f: f.create_health_check(""), "Component name cannot be empty"),
        ],
    )
    def test_invalid_input_returns_failure_with_expected_message(
        self,
        creator: _Create,
        expected_error: str,
    ) -> None:
        """Each fallible creator surfaces a failure result with a descriptive error."""
        result = creator(_Factory())
        tm.that(result.failure, eq=True)
        tm.that(result.error, none=False)
        tm.that(result.error, has=expected_error)
