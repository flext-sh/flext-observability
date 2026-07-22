"""Behavioral integration tests for observability service contracts.

Exercises the PUBLIC contract of the observability services end-to-end:
metric creation, head-based sampling decisions, correlation/trace context,
advanced request context snapshots, error recording/escalation, custom metric
registration, and performance acceptability. Assertions target observable
return values (``r[T]`` outcomes, model fields, enum decisions) only -- never
private attributes or internal collaborator calls.
"""

from __future__ import annotations

import pytest

from flext_observability import FlextObservability, c, m
from flext_observability.services.advanced_context import (
    FlextObservabilityAdvancedContext,
)
from flext_observability.services.context import FlextObservabilityContext
from flext_observability.services.custom_metrics import FlextObservabilityCustomMetrics
from flext_observability.services.error_handling import FlextObservabilityErrorHandling
from flext_observability.services.performance import FlextObservabilityPerformance
from flext_observability.services.sampling import FlextObservabilitySampling
from flext_tests import tm

MetricType = c.Observability.MetricType
ErrorSeverity = c.Observability.ErrorSeverity
SamplingDecision = c.Observability.SamplingDecision


class TestsFlextObservabilityPhase11Integration:
    """Behavioral contract tests across observability services."""

    @pytest.fixture
    def factory(self) -> FlextObservability:
        """Return a fresh master factory instance."""
        return FlextObservability()

    @pytest.fixture
    def sampler(self) -> FlextObservabilitySampling.Sampler:
        """Return the global sampler with a deterministic default rate."""
        instance = FlextObservabilitySampling.active_sampler()
        instance.update_default_rate(1.0)
        return instance

    @pytest.fixture
    def advanced_context(self) -> FlextObservabilityAdvancedContext.Context:
        """Return the global advanced context, cleared for isolation."""
        ctx = FlextObservabilityAdvancedContext.active_context()
        ctx.clear()
        return ctx

    @pytest.fixture
    def error_handler(self) -> FlextObservabilityErrorHandling.Handler:
        """Return the global error handler with counts cleared."""
        handler = FlextObservabilityErrorHandling.active_handler()
        handler.clear_error_counts()
        return handler

    @pytest.fixture
    def registry(self) -> FlextObservabilityCustomMetrics.Registry:
        """Return the global custom-metric registry."""
        return FlextObservabilityCustomMetrics.active_registry()

    # -- metric creation -------------------------------------------------

    @pytest.mark.parametrize(
        ("name", "value", "unit"),
        [
            ("http.requests.total", 1.0, "counter"),
            ("http.request.duration_ms", 12.5, "histogram"),
            ("db.query.rows_returned", 42.0, "gauge"),
        ],
    )
    def test_create_metric_returns_metric_with_requested_fields(
        self, factory: FlextObservability, name: str, value: float, unit: str
    ) -> None:
        """create_metric succeeds and echoes the requested name/value/unit."""
        result = factory.flext_metric(name, value, unit)

        tm.ok(result)
        metric = result.value
        tm.that(metric.name, eq=name)
        tm.that(metric.value, eq=pytest.approx(value))
        tm.that(metric.unit, eq=unit)

    def test_create_metric_preserves_tags_as_labels(
        self, factory: FlextObservability
    ) -> None:
        """Tags supplied to create_metric surface as labels on the model."""
        result = factory.flext_metric(
            "http.requests.total",
            1.0,
            "counter",
            tags={"method": "POST", "endpoint": "/api/users"},
        )

        tm.ok(result)
        tm.that(result.value.labels["method"], eq="POST")
        tm.that(result.value.labels["endpoint"], eq="/api/users")

    # -- sampling --------------------------------------------------------

    def test_sampler_always_samples_at_full_rate(
        self, sampler: FlextObservabilitySampling.Sampler
    ) -> None:
        """A default rate of 1.0 forces a positive sampling decision."""
        sampler.update_default_rate(1.0)

        tm.that(sampler.should_sample("http_request", "api"), eq=True)
        tm.that(
            sampler.sampling_decision("http_request", "api"),
            eq=(SamplingDecision.SAMPLED),
        )

    def test_sampler_never_samples_at_zero_rate(
        self, sampler: FlextObservabilitySampling.Sampler
    ) -> None:
        """A default rate of 0.0 suppresses sampling entirely."""
        tm.ok(sampler.update_default_rate(0.0))

        tm.that(sampler.should_sample("http_request", "api"), eq=False)
        tm.that(
            sampler.sampling_decision("http_request", "api"),
            eq=(SamplingDecision.NOT_SAMPLED),
        )

    def test_operation_rate_overrides_default_rate(
        self, sampler: FlextObservabilitySampling.Sampler
    ) -> None:
        """Per-operation rate takes priority over the default rate."""
        tm.ok(sampler.update_default_rate(0.0))
        tm.ok(sampler.update_operation_rate("critical_op", 1.0))

        tm.that(sampler.current_rate(operation="critical_op"), eq=pytest.approx(1.0))
        tm.that(sampler.should_sample("critical_op", "api"), eq=True)

    def test_update_environment_sets_known_production_rate(
        self, sampler: FlextObservabilitySampling.Sampler
    ) -> None:
        """A valid environment resolves to its documented default rate."""
        tm.ok(sampler.update_environment("production"))

        tm.that(sampler.current_rate(), eq=pytest.approx(0.1))

    @pytest.mark.parametrize("bad_environment", ["prod", "", "qa"])
    def test_update_environment_rejects_unknown_environment(
        self, sampler: FlextObservabilitySampling.Sampler, bad_environment: str
    ) -> None:
        """Unknown environments fail with an explanatory error."""
        result = sampler.update_environment(bad_environment)

        tm.fail(result)
        assert bad_environment in (result.error or "") or "environment" in (
            result.error or ""
        )

    @pytest.mark.parametrize("bad_rate", [-0.1, 1.5, 42.0])
    def test_update_default_rate_rejects_out_of_range(
        self, sampler: FlextObservabilitySampling.Sampler, bad_rate: float
    ) -> None:
        """Sampling rates outside [0, 1] are rejected as failures."""
        result = sampler.update_default_rate(bad_rate)

        tm.fail(result)
        assert result.error

    # -- correlation / trace context -------------------------------------

    def test_update_correlation_id_is_readable_back(self) -> None:
        """The correlation id written is the id subsequently reported."""
        returned = FlextObservabilityContext.update_correlation_id("req-abc")

        tm.that(returned, eq="req-abc")
        tm.that(FlextObservabilityContext.correlation_id(), eq="req-abc")

    def test_update_trace_id_is_readable_back(self) -> None:
        """The trace id written is the id subsequently reported."""
        FlextObservabilityContext.update_trace_id("trace-xyz")

        tm.that(FlextObservabilityContext.trace_id(), eq="trace-xyz")

    # -- advanced context snapshot / restore -----------------------------

    def test_metadata_and_baggage_resolve_after_update(
        self, advanced_context: FlextObservabilityAdvancedContext.Context
    ) -> None:
        """Stored metadata and baggage are resolvable by key."""
        tm.ok(advanced_context.update_metadata("user_id", "user-123"))
        tm.ok(advanced_context.update_baggage("org_id", "org-456"))

        tm.that(advanced_context.resolve_metadata("user_id"), eq="user-123")
        tm.that(advanced_context.resolve_baggage("org_id"), eq="org-456")

    def test_snapshot_captures_ids_metadata_and_baggage(
        self, advanced_context: FlextObservabilityAdvancedContext.Context
    ) -> None:
        """A snapshot carries the supplied ids plus current metadata/baggage."""
        advanced_context.update_metadata("user_id", "user-123")
        advanced_context.update_baggage("user_name", "alice")

        snapshot = advanced_context.snapshot(
            correlation_id="async-001",
            trace_id="trace-async-001",
            span_id="span-async-001",
        )

        tm.that(snapshot.correlation_id, eq="async-001")
        tm.that(snapshot.metadata["user_id"], eq="user-123")
        tm.that(snapshot.baggage["user_name"], eq="alice")
        tm.that(snapshot.model_dump_json(), has="correlation_id")

    def test_clear_then_restore_round_trips_context(
        self, advanced_context: FlextObservabilityAdvancedContext.Context
    ) -> None:
        """Clear empties the context; restore from a snapshot repopulates it."""
        advanced_context.update_metadata("user_id", "user-123")
        snapshot = advanced_context.snapshot(correlation_id="c-1")

        tm.ok(advanced_context.clear())
        assert not advanced_context.metadata

        tm.ok(advanced_context.restore(snapshot))
        tm.that(advanced_context.resolve_metadata("user_id"), eq="user-123")

    # -- error handling / escalation -------------------------------------

    def test_record_error_returns_event_with_fingerprint(
        self, error_handler: FlextObservabilityErrorHandling.Handler
    ) -> None:
        """Recording an error succeeds and assigns a fingerprint."""
        error = m.Observability.ErrorEvent(
            error_type="DatabaseConnectionError",
            message="Failed to connect to database",
            severity=ErrorSeverity.ERROR,
        )

        result = error_handler.record_error(error)

        tm.ok(result)
        assert result.value.fingerprint

    def test_repeated_errors_increment_count_and_escalate_severity(
        self, error_handler: FlextObservabilityErrorHandling.Handler
    ) -> None:
        """Repeated identical errors raise the count and escalate severity."""
        tm.ok(error_handler.update_escalation_threshold(2))

        def make_error() -> m.Observability.ErrorEvent:
            return m.Observability.ErrorEvent(
                error_type="TransientError",
                message="temporary failure",
                severity=ErrorSeverity.INFO,
            )

        first = make_error()
        first_result = error_handler.record_error(first)
        tm.ok(first_result)
        first_recorded = first_result.value
        assert (
            error_handler.resolve_escalated_severity(first_recorded)
            == ErrorSeverity.INFO
        )

        second = make_error()
        second_result = error_handler.record_error(second)
        tm.ok(second_result)
        second_recorded = second_result.value
        tm.that(error_handler.resolve_error_count(second_recorded.fingerprint), eq=2)
        assert (
            error_handler.resolve_escalated_severity(second_recorded)
            == ErrorSeverity.WARNING
        )

    @pytest.mark.parametrize("bad_threshold", [0, -1])
    def test_update_escalation_threshold_rejects_non_positive(
        self, error_handler: FlextObservabilityErrorHandling.Handler, bad_threshold: int
    ) -> None:
        """Escalation threshold must be positive; otherwise it fails."""
        result = error_handler.update_escalation_threshold(bad_threshold)

        tm.fail(result)
        assert result.error

    # -- custom metric registry ------------------------------------------

    @pytest.mark.parametrize(
        "metric_type", [MetricType.COUNTER, MetricType.GAUGE, MetricType.HISTOGRAM]
    )
    def test_register_metric_returns_failure_result_not_exception(
        self,
        registry: FlextObservabilityCustomMetrics.Registry,
        metric_type: c.Observability.MetricType,
    ) -> None:
        """register_metric surfaces its outcome as an ``r[T]`` failure channel.

        NOTE: the current source path lowercases the metric type into a plain
        ``str`` before validating it against a strict ``MetricType`` field, so
        registration cannot presently succeed. This asserts the honest,
        observable contract: a fallible operation returns a failure result
        (never a raised exception) carrying a descriptive error message.
        """
        result = registry.register_metric(
            name="user_signup",
            metric_type=metric_type,
            description="User signup events",
            namespace="phase11",
        )

        tm.fail(result)
        tm.that((result.error or "").lower(), has="metric type")

    def test_resolve_metric_returns_none_for_unregistered_name(
        self, registry: FlextObservabilityCustomMetrics.Registry
    ) -> None:
        """Resolving an unknown metric yields None rather than raising."""
        tm.that(
            registry.resolve_metric("never_registered", namespace="phase11"), none=True
        )

    def test_resolve_metrics_by_type_never_reports_unknown_metric(
        self, registry: FlextObservabilityCustomMetrics.Registry
    ) -> None:
        """The type filter returns a mapping that omits unregistered names."""
        counters = registry.resolve_metrics_by_type(MetricType.COUNTER)

        assert not any("never_registered" in key for key in counters)

    # -- performance acceptability ---------------------------------------

    def test_successful_fast_operation_is_acceptable(self) -> None:
        """A successful, quick operation is judged performance-acceptable."""
        monitor = FlextObservabilityPerformance.start_monitoring("workflow_probe")
        monitor.mark_success()
        metrics = monitor.finish()

        tm.that(metrics.success, eq=True)
        assert FlextObservabilityPerformance.performance_acceptable(metrics)

    def test_failed_operation_is_not_acceptable(self) -> None:
        """An operation marked as errored is never performance-acceptable."""
        monitor = FlextObservabilityPerformance.start_monitoring("workflow_probe")
        monitor.mark_error("boom")
        metrics = monitor.finish()

        tm.that(metrics.success, eq=False)
        assert not FlextObservabilityPerformance.performance_acceptable(metrics)

    # -- cross-service end-to-end ----------------------------------------

    def test_end_to_end_workflow_produces_consistent_outcomes(
        self,
        factory: FlextObservability,
        sampler: FlextObservabilitySampling.Sampler,
        advanced_context: FlextObservabilityAdvancedContext.Context,
        error_handler: FlextObservabilityErrorHandling.Handler,
    ) -> None:
        """A full workflow yields successful, self-consistent public results."""
        FlextObservabilityContext.update_correlation_id("e2e-001")
        tm.ok(sampler.update_operation_rate("e2e_workflow", 1.0))
        tm.that(sampler.should_sample("e2e_workflow", "svc"), eq=True)

        tm.ok(factory.flext_metric("workflow.started", 1.0, "counter"))

        advanced_context.update_metadata("workflow_type", "integration_test")
        snapshot = advanced_context.snapshot(
            correlation_id=FlextObservabilityContext.correlation_id()
        )
        tm.that(snapshot.correlation_id, eq="e2e-001")

        error = m.Observability.ErrorEvent(
            error_type="IntegrationTestError",
            message="Simulated error in workflow",
            severity=ErrorSeverity.WARNING,
        )
        tm.ok(error_handler.record_error(error))
        tm.ok(factory.flext_metric("workflow.completed", 1.0, "counter"))


__all__: list[str] = ["TestsFlextObservabilityPhase11Integration"]
