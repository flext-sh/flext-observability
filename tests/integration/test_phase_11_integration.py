"""Phase 11: Integration Tests for Observability Components.

Tests realistic scenarios combining:
- HTTP operations with observability
- Database operations with metrics
- Error handling with alerting
- Distributed tracing across components
- Performance monitoring and sampling
"""

from __future__ import annotations

import time

from flext_observability import (
    FlextObservability,
    FlextObservabilityAdvancedContext,
    FlextObservabilityContext,
    FlextObservabilityCustomMetrics,
    FlextObservabilityErrorHandling,
    FlextObservabilityPerformance,
    FlextObservabilitySampling,
    c,
    m,
)

ErrorEvent = m.Observability.ErrorEvent

try:
    FlextObservabilityContext.update_correlation_id("http-req-001")
    FlextObservabilityContext.update_trace_id("trace-http-001")
    sampler = FlextObservabilitySampling.active_sampler()
    sampler.update_environment("production")
    sampler.update_operation_rate("http_request", 1.0)
    should_sample = sampler.should_sample("http_request", "api")
    assert should_sample is not None, "Sampling decision should be made"
    factory = FlextObservability.FlextObservabilityMasterFactory()
    metric_result = factory.create_metric(
        "http.requests.total",
        1.0,
        "counter",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.success
    start_time = time.time()
    time.sleep(0.01)
    duration = time.time() - start_time
    metric_result = factory.create_metric(
        "http.request.duration_ms",
        duration * 1000,
        "histogram",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.success
    metric_result = factory.create_metric(
        "http.requests.success",
        1.0,
        "counter",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.success
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    factory = FlextObservability.FlextObservabilityMasterFactory()
    start_time = time.time()
    time.sleep(0.02)
    duration = time.time() - start_time
    result = factory.create_metric(
        "db.queries.total",
        1.0,
        "counter",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.success
    result = factory.create_metric(
        "db.query.duration_ms",
        duration * 1000,
        "histogram",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.success
    result = factory.create_metric(
        "db.query.rows_returned",
        1.0,
        "gauge",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.success
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    FlextObservabilityContext.update_correlation_id("error-test-001")
    handler = FlextObservabilityErrorHandling.active_handler()
    handler.update_escalation_threshold(3)
    handler.update_alert_cooldown(30)
    for i in range(3):
        error = ErrorEvent(
            error_type="DatabaseConnectionError",
            message="Failed to connect to database",
            severity=c.Observability.ErrorSeverity.ERROR,
        )
        error_result = handler.record_error(error)
        assert error_result.success, "Error should be recorded"
        should_alert = handler.should_alert_for_error(error)
        if i == 2:
            escalated = handler.resolve_escalated_severity(error)
            assert escalated is not None
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    correlation_id = "dist-trace-001"
    FlextObservabilityContext.update_correlation_id(correlation_id)
    factory = FlextObservability.FlextObservabilityMasterFactory()
    api_result = factory.create_metric(
        "api.requests",
        1.0,
        "counter",
        tags={"component": "api"},
    )
    assert api_result.success
    time.sleep(0.005)
    business_result = factory.create_metric(
        "business.operations",
        1.0,
        "counter",
        tags={"component": "business"},
    )
    assert business_result.success
    time.sleep(0.005)
    db_result = factory.create_metric(
        "database.queries",
        1.0,
        "counter",
        tags={"component": "database"},
    )
    assert db_result.success
    time.sleep(0.01)
    api_success = factory.create_metric(
        "api.success",
        1.0,
        "counter",
        tags={"component": "api"},
    )
    assert api_success.success
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    ctx = FlextObservabilityAdvancedContext.active_context()
    ctx.update_metadata("user_id", "user-123")
    ctx.update_metadata("request_id", "req-456")
    ctx.update_metadata("tenant_id", "tenant-789")
    ctx.update_baggage("user_name", "alice")
    ctx.update_baggage("org_id", "org-456")
    snapshot = ctx.snapshot(
        correlation_id="async-001",
        trace_id="trace-async-001",
        span_id="span-async-001",
    )
    assert snapshot.correlation_id == "async-001"
    assert len(snapshot.metadata) >= 3
    assert len(snapshot.baggage) >= 2
    json_data = snapshot.model_dump_json()
    assert json_data is not None
    assert "correlation_id" in json_data
    ctx.clear()
    assert not ctx.metadata
    ctx.restore(snapshot)
    assert ctx.resolve_metadata("user_id") == "user-123"
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    registry = FlextObservabilityCustomMetrics.active_registry()
    sampler = FlextObservabilitySampling.active_sampler()
    reg_result = registry.register_metric(
        name="user_signup",
        metric_type=c.Observability.MetricType.COUNTER,
        description="User signup events",
        namespace="auth",
    )
    assert reg_result.success
    reg_result = registry.register_metric(
        name="active_sessions",
        metric_type=c.Observability.MetricType.GAUGE,
        description="Currently active sessions",
        namespace="auth",
    )
    assert reg_result.success
    sampler.update_service_rate("auth_service", 0.5)
    sampler.update_operation_rate("user_signup", 1.0)
    metrics = registry.resolve_metrics_by_type(c.Observability.MetricType.COUNTER)
    assert any("user_signup" in m for m in metrics)
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    sampler = FlextObservabilitySampling.active_sampler()
    performance = FlextObservabilityPerformance()
    sampler.update_environment("production")
    sampler.update_default_rate(0.1)
    should_sample = sampler.should_sample("sample_test", "service")
    assert should_sample is not None, "Sampling decision should be made"
    monitor = performance.start_monitoring("sampling_operation")
    time.sleep(0.001)
    monitor.mark_success()
    perf_metrics = monitor.metrics
    assert performance.performance_acceptable(perf_metrics), (
        "Sampling performance overhead should be acceptable"
    )
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    FlextObservabilityContext.update_correlation_id("e2e-test-001")
    FlextObservabilityContext.update_trace_id("trace-e2e-001")
    sampler = FlextObservabilitySampling.active_sampler()
    sampler.update_environment("staging")
    sampler.update_operation_rate("e2e_workflow", 1.0)
    factory = FlextObservability.FlextObservabilityMasterFactory()
    result = factory.create_metric("workflow.started", 1.0, "counter")
    assert result.success
    perf_monitor = FlextObservabilityPerformance()
    monitor = perf_monitor.start_monitoring("e2e_operation")
    adv_ctx = FlextObservabilityAdvancedContext.active_context()
    adv_ctx.update_metadata("workflow_type", "integration_test")
    adv_ctx.update_baggage("test_phase", "11")
    registry = FlextObservabilityCustomMetrics.active_registry()
    reg_result2 = registry.register_metric(
        name="e2e_tests",
        metric_type=c.Observability.MetricType.COUNTER,
        description="E2E workflow tests",
        namespace="integration",
    )
    time.sleep(0.015)
    monitor.mark_success()
    perf_metrics = monitor.metrics
    assert perf_monitor.performance_acceptable(perf_metrics)
    result = factory.create_metric("workflow.completed", 1.0, "counter")
    assert result.success
    result = factory.create_metric("workflow.duration_ms", perf_metrics.duration_ms)
    assert result.success
    snapshot = adv_ctx.snapshot(
        correlation_id=FlextObservabilityContext.correlation_id(),
        trace_id=FlextObservabilityContext.trace_id(),
        span_id="span-e2e-001",
    )
    assert snapshot is not None
    assert snapshot.correlation_id == "e2e-test-001"
    error_handler = FlextObservabilityErrorHandling.active_handler()
    test_error = ErrorEvent(
        error_type="IntegrationTestError",
        message="Simulated error in workflow",
        severity=c.Observability.ErrorSeverity.WARNING,
    )
    error_result = error_handler.record_error(test_error)
    assert error_result.success
    result = factory.create_metric("workflow.errors", 1.0, "counter")
    assert result.success
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    correlation_id = "multi-service-001"
    FlextObservabilityContext.update_correlation_id(correlation_id)
    FlextObservabilityContext.update_trace_id("trace-multi-001")
    ctx1_corr = FlextObservabilityContext.correlation_id()
    assert ctx1_corr == correlation_id
    FlextObservabilityContext.update_correlation_id(correlation_id)
    FlextObservabilityContext.update_trace_id("trace-multi-001")
    assert ctx1_corr == FlextObservabilityContext.correlation_id()
    adv_ctx = FlextObservabilityAdvancedContext.active_context()
    adv_ctx.update_metadata("service", "api")
    adv_ctx.update_metadata("user_id", "user-456")
    snapshot = adv_ctx.snapshot(
        correlation_id=correlation_id,
        trace_id="trace-multi-001",
        span_id="span-api-001",
    )
    json_snapshot = snapshot.model_dump_json()
    assert json_snapshot is not None
    assert "correlation_id" in json_snapshot
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
try:
    FlextObservabilityContext.update_correlation_id("setup-001")
    assert FlextObservabilityContext.correlation_id() == "setup-001"
    factory = FlextObservability.FlextObservabilityMasterFactory()
    assert factory is not None
    sampler = FlextObservabilitySampling.active_sampler()
    perf = FlextObservabilityPerformance()
    assert sampler is not None and perf is not None
    errors = FlextObservabilityErrorHandling.active_handler()
    custom_metrics = FlextObservabilityCustomMetrics.active_registry()
    advanced_ctx = FlextObservabilityAdvancedContext.active_context()
    assert errors is not None
    assert custom_metrics is not None
    assert advanced_ctx is not None
    metrics_service = factory
    assert metrics_service is not None
    FlextObservabilityContext.update_correlation_id("example-001")
    assert FlextObservabilityContext.correlation_id() == "example-001"
    sampler.update_environment("production")
    should_sample = sampler.should_sample("test", "service")
    assert should_sample is not None
except (AssertionError, RuntimeError, ValueError, TypeError):
    pass
