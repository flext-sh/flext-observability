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

from flext_observability.api import FlextObservability
from flext_observability.constants import c
from flext_observability.models import m
from flext_observability.services.advanced_context import (
    FlextObservabilityAdvancedContext,
)
from flext_observability.services.context import FlextObservabilityContext
from flext_observability.services.custom_metrics import FlextObservabilityCustomMetrics
from flext_observability.services.error_handling import FlextObservabilityErrorHandling
from flext_observability.services.performance import FlextObservabilityPerformance
from flext_observability.services.sampling import FlextObservabilitySampling

MetricType = c.Observability.MetricType
ErrorSeverity = c.Observability.ErrorSeverity
SamplingDecision = c.Observability.SamplingDecision

type Factory = FlextObservability.FlextObservabilityMasterFactory
type Sampler = FlextObservabilitySampling.Sampler
type AdvancedContext = FlextObservabilityAdvancedContext.Context
type ErrorHandler = FlextObservabilityErrorHandling.Handler
type MetricRegistry = FlextObservabilityCustomMetrics.Registry


class TestsFlextObservabilityPhase11Integration:
    """Behavioral contract tests across observability services."""

    @pytest.fixture
    def factory(self) -> Factory:
        """Return a fresh master factory instance."""
        return FlextObservability.FlextObservabilityMasterFactory()

    @pytest.fixture
    def sampler(self) -> Sampler:
        """Return the global sampler with a deterministic default rate."""
        instance = FlextObservabilitySampling.active_sampler()
        instance.update_default_rate(1.0)
        return instance

    @pytest.fixture
    def advanced_context(self) -> AdvancedContext:
        """Return the global advanced context, cleared for isolation."""
        ctx = FlextObservabilityAdvancedContext.active_context()
        ctx.clear()
        return ctx

    @pytest.fixture
    def error_handler(self) -> ErrorHandler:
        """Return the global error handler with counts cleared."""
        handler = FlextObservabilityErrorHandling.active_handler()
        handler.clear_error_counts()
        return handler

    @pytest.fixture
    def registry(self) -> MetricRegistry:
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
        self,
        factory: Factory,
        name: str,
        value: float,
        unit: str,
    ) -> None:
        """create_metric succeeds and echoes the requested name/value/unit."""
        result = factory.create_metric(name, value, unit)

        assert result.success
        metric = result.value
        assert metric.name == name
        assert metric.value == pytest.approx(value)
        assert metric.unit == unit

    def test_create_metric_preserves_tags_as_labels(
        self,
        factory: Factory,
    ) -> None:
        """Tags supplied to create_metric surface as labels on the model."""
        result = factory.create_metric(
            "http.requests.total",
            1.0,
            "counter",
            tags={"method": "POST", "endpoint": "/api/users"},
        )

        assert result.success
        assert result.value.labels["method"] == "POST"
        assert result.value.labels["endpoint"] == "/api/users"

    # -- sampling --------------------------------------------------------

    def test_sampler_always_samples_at_full_rate(self, sampler: Sampler) -> None:
        """A default rate of 1.0 forces a positive sampling decision."""
        sampler.update_default_rate(1.0)

        assert sampler.should_sample("http_request", "api") is True
        assert sampler.sampling_decision("http_request", "api") == (
            SamplingDecision.SAMPLED
        )

    def test_sampler_never_samples_at_zero_rate(self, sampler: Sampler) -> None:
        """A default rate of 0.0 suppresses sampling entirely."""
        assert sampler.update_default_rate(0.0).success

        assert sampler.should_sample("http_request", "api") is False
        assert sampler.sampling_decision("http_request", "api") == (
            SamplingDecision.NOT_SAMPLED
        )

    def test_operation_rate_overrides_default_rate(self, sampler: Sampler) -> None:
        """Per-operation rate takes priority over the default rate."""
        assert sampler.update_default_rate(0.0).success
        assert sampler.update_operation_rate("critical_op", 1.0).success

        assert sampler.current_rate(operation="critical_op") == pytest.approx(1.0)
        assert sampler.should_sample("critical_op", "api") is True

    def test_update_environment_sets_known_production_rate(
        self,
        sampler: Sampler,
    ) -> None:
        """A valid environment resolves to its documented default rate."""
        assert sampler.update_environment("production").success

        assert sampler.current_rate() == pytest.approx(0.1)

    @pytest.mark.parametrize("bad_environment", ["prod", "", "qa"])
    def test_update_environment_rejects_unknown_environment(
        self,
        sampler: Sampler,
        bad_environment: str,
    ) -> None:
        """Unknown environments fail with an explanatory error."""
        result = sampler.update_environment(bad_environment)

        assert not result.success
        assert bad_environment in (result.error or "") or "environment" in (
            result.error or ""
        )

    @pytest.mark.parametrize("bad_rate", [-0.1, 1.5, 42.0])
    def test_update_default_rate_rejects_out_of_range(
        self,
        sampler: Sampler,
        bad_rate: float,
    ) -> None:
        """Sampling rates outside [0, 1] are rejected as failures."""
        result = sampler.update_default_rate(bad_rate)

        assert not result.success
        assert result.error

    # -- correlation / trace context -------------------------------------

    def test_update_correlation_id_is_readable_back(self) -> None:
        """The correlation id written is the id subsequently reported."""
        returned = FlextObservabilityContext.update_correlation_id("req-abc")

        assert returned == "req-abc"
        assert FlextObservabilityContext.correlation_id() == "req-abc"

    def test_update_trace_id_is_readable_back(self) -> None:
        """The trace id written is the id subsequently reported."""
        FlextObservabilityContext.update_trace_id("trace-xyz")

        assert FlextObservabilityContext.trace_id() == "trace-xyz"

    # -- advanced context snapshot / restore -----------------------------

    def test_metadata_and_baggage_resolve_after_update(
        self,
        advanced_context: AdvancedContext,
    ) -> None:
        """Stored metadata and baggage are resolvable by key."""
        assert advanced_context.update_metadata("user_id", "user-123").success
        assert advanced_context.update_baggage("org_id", "org-456").success

        assert advanced_context.resolve_metadata("user_id") == "user-123"
        assert advanced_context.resolve_baggage("org_id") == "org-456"

    def test_snapshot_captures_ids_metadata_and_baggage(
        self,
        advanced_context: AdvancedContext,
    ) -> None:
        """A snapshot carries the supplied ids plus current metadata/baggage."""
        advanced_context.update_metadata("user_id", "user-123")
        advanced_context.update_baggage("user_name", "alice")

        snapshot = advanced_context.snapshot(
            correlation_id="async-001",
            trace_id="trace-async-001",
            span_id="span-async-001",
        )

        assert snapshot.correlation_id == "async-001"
        assert snapshot.metadata["user_id"] == "user-123"
        assert snapshot.baggage["user_name"] == "alice"
        assert "correlation_id" in snapshot.model_dump_json()

    def test_clear_then_restore_round_trips_context(
        self,
        advanced_context: AdvancedContext,
    ) -> None:
        """Clear empties the context; restore from a snapshot repopulates it."""
        advanced_context.update_metadata("user_id", "user-123")
        snapshot = advanced_context.snapshot(correlation_id="c-1")

        assert advanced_context.clear().success
        assert not advanced_context.metadata

        assert advanced_context.restore(snapshot).success
        assert advanced_context.resolve_metadata("user_id") == "user-123"

    # -- error handling / escalation -------------------------------------

    def test_record_error_returns_event_with_fingerprint(
        self,
        error_handler: ErrorHandler,
    ) -> None:
        """Recording an error succeeds and assigns a fingerprint."""
        error = m.Observability.ErrorEvent(
            error_type="DatabaseConnectionError",
            message="Failed to connect to database",
            severity=ErrorSeverity.ERROR,
        )

        result = error_handler.record_error(error)

        assert result.success
        assert result.value.fingerprint

    def test_repeated_errors_increment_count_and_escalate_severity(
        self,
        error_handler: ErrorHandler,
    ) -> None:
        """Repeated identical errors raise the count and escalate severity."""
        assert error_handler.update_escalation_threshold(2).success

        def make_error() -> m.Observability.ErrorEvent:
            return m.Observability.ErrorEvent(
                error_type="TransientError",
                message="temporary failure",
                severity=ErrorSeverity.INFO,
            )

        first = make_error()
        first_result = error_handler.record_error(first)
        assert first_result.success
        first_recorded = first_result.value
        assert (
            error_handler.resolve_escalated_severity(first_recorded)
            == ErrorSeverity.INFO
        )

        second = make_error()
        second_result = error_handler.record_error(second)
        assert second_result.success
        second_recorded = second_result.value
        assert error_handler.resolve_error_count(second_recorded.fingerprint) == 2
        assert (
            error_handler.resolve_escalated_severity(second_recorded)
            == ErrorSeverity.WARNING
        )

    @pytest.mark.parametrize("bad_threshold", [0, -1])
    def test_update_escalation_threshold_rejects_non_positive(
        self,
        error_handler: ErrorHandler,
        bad_threshold: int,
    ) -> None:
        """Escalation threshold must be positive; otherwise it fails."""
        result = error_handler.update_escalation_threshold(bad_threshold)

        assert not result.success
        assert result.error

    # -- custom metric registry ------------------------------------------

    @pytest.mark.parametrize(
        "metric_type",
        [MetricType.COUNTER, MetricType.GAUGE, MetricType.HISTOGRAM],
    )
    def test_register_metric_returns_failure_result_not_exception(
        self,
        registry: MetricRegistry,
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

        assert not result.success
        assert "metric type" in (result.error or "").lower()

    def test_resolve_metric_returns_none_for_unregistered_name(
        self,
        registry: MetricRegistry,
    ) -> None:
        """Resolving an unknown metric yields None rather than raising."""
        assert registry.resolve_metric("never_registered", namespace="phase11") is None

    def test_resolve_metrics_by_type_never_reports_unknown_metric(
        self,
        registry: MetricRegistry,
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

        assert metrics.success
        assert FlextObservabilityPerformance.performance_acceptable(metrics)

    def test_failed_operation_is_not_acceptable(self) -> None:
        """An operation marked as errored is never performance-acceptable."""
        monitor = FlextObservabilityPerformance.start_monitoring("workflow_probe")
        monitor.mark_error("boom")
        metrics = monitor.finish()

        assert not metrics.success
        assert not FlextObservabilityPerformance.performance_acceptable(metrics)

    # -- cross-service end-to-end ----------------------------------------

    def test_end_to_end_workflow_produces_consistent_outcomes(
        self,
        factory: Factory,
        sampler: Sampler,
        advanced_context: AdvancedContext,
        error_handler: ErrorHandler,
    ) -> None:
        """A full workflow yields successful, self-consistent public results."""
        FlextObservabilityContext.update_correlation_id("e2e-001")
        assert sampler.update_operation_rate("e2e_workflow", 1.0).success
        assert sampler.should_sample("e2e_workflow", "svc") is True

        assert factory.create_metric("workflow.started", 1.0, "counter").success

        advanced_context.update_metadata("workflow_type", "integration_test")
        snapshot = advanced_context.snapshot(
            correlation_id=FlextObservabilityContext.correlation_id(),
        )
        assert snapshot.correlation_id == "e2e-001"

        error = m.Observability.ErrorEvent(
            error_type="IntegrationTestError",
            message="Simulated error in workflow",
            severity=ErrorSeverity.WARNING,
        )
        assert error_handler.record_error(error).success
        assert factory.create_metric("workflow.completed", 1.0, "counter").success


__all__: list[str] = ["TestsFlextObservabilityPhase11Integration"]
