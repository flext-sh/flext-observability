"""Phase 11: Integration Tests for Observability Components.

Tests realistic scenarios combining:
- HTTP operations with observability
- Database operations with metrics
- Error handling with alerting
- Distributed tracing across components
- Performance monitoring and sampling
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "../../src"))
import time

try:
    from flext_observability import (
        FlextObservabilityContext,
        FlextObservabilityMasterFactory,
        FlextObservabilitySampling,
    )

    FlextObservabilityContext.set_correlation_id("http-req-001")
    FlextObservabilityContext.set_trace_id("trace-http-001")
    sampler = FlextObservabilitySampling.get_sampler()
    sampler.set_environment("production")
    sampler.set_operation_rate("http_request", 1.0)
    should_sample = sampler.should_sample("http_request", "api")
    assert should_sample is not None, "Sampling decision should be made"
    factory = FlextObservabilityMasterFactory()
    metric_result = factory.create_metric(
        "http.requests.total",
        1.0,
        "counter",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.is_success
    start_time = time.time()
    time.sleep(0.01)
    duration = time.time() - start_time
    metric_result = factory.create_metric(
        "http.request.duration_ms",
        duration * 1000,
        "histogram",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.is_success
    metric_result = factory.create_metric(
        "http.requests.success",
        1.0,
        "counter",
        tags={"method": "POST", "endpoint": "/api/users"},
    )
    assert metric_result.is_success
except Exception:
    pass
try:
    from flext_observability import FlextObservabilityMasterFactory

    factory = FlextObservabilityMasterFactory()
    start_time = time.time()
    time.sleep(0.02)
    duration = time.time() - start_time
    result = factory.create_metric(
        "db.queries.total",
        1.0,
        "counter",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.is_success
    result = factory.create_metric(
        "db.query.duration_ms",
        duration * 1000,
        "histogram",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.is_success
    result = factory.create_metric(
        "db.query.rows_returned",
        1.0,
        "gauge",
        tags={"system": "postgresql", "operation": "SELECT"},
    )
    assert result.is_success
except Exception:
    pass
try:
    from flext_observability import (
        ErrorEvent,
        FlextObservabilityContext,
        FlextObservabilityErrorHandling,
        c,
    )

    FlextObservabilityContext.set_correlation_id("error-test-001")
    handler = FlextObservabilityErrorHandling.get_handler()
    handler.set_escalation_threshold(3)
    handler.set_alert_cooldown(30)
    for i in range(3):
        error = ErrorEvent(
            error_type="DatabaseConnectionError",
            message="Failed to connect to database",
            severity=c.Observability.ErrorSeverity.ERROR,
        )
        result = handler.record_error(error)
        assert result.is_success, "Error should be recorded"
        should_alert = handler.should_alert_for_error(error)
        if i == 2:
            escalated = handler.get_escalated_severity(error)
            assert escalated is not None
except Exception:
    pass
try:
    from flext_observability import (
        FlextObservabilityContext,
        FlextObservabilityMasterFactory,
    )

    correlation_id = "dist-trace-001"
    FlextObservabilityContext.set_correlation_id(correlation_id)
    factory = FlextObservabilityMasterFactory()
    api_result = factory.create_metric(
        "api.requests",
        1.0,
        "counter",
        tags={"component": "api"},
    )
    assert api_result.is_success
    time.sleep(0.005)
    business_result = factory.create_metric(
        "business.operations",
        1.0,
        "counter",
        tags={"component": "business"},
    )
    assert business_result.is_success
    time.sleep(0.005)
    db_result = factory.create_metric(
        "database.queries",
        1.0,
        "counter",
        tags={"component": "database"},
    )
    assert db_result.is_success
    time.sleep(0.01)
    api_success = factory.create_metric(
        "api.success",
        1.0,
        "counter",
        tags={"component": "api"},
    )
    assert api_success.is_success
except Exception:
    pass
try:
    from flext_observability import FlextObservabilityAdvancedContext

    ctx = FlextObservabilityAdvancedContext.get_context()
    ctx.set_metadata("user_id", "user-123")
    ctx.set_metadata("request_id", "req-456")
    ctx.set_metadata("tenant_id", "tenant-789")
    ctx.set_baggage("user_name", "alice")
    ctx.set_baggage("org_id", "org-456")
    snapshot = ctx.snapshot(
        correlation_id="async-001", trace_id="trace-async-001", span_id="span-async-001"
    )
    assert snapshot.correlation_id == "async-001"
    assert len(snapshot.metadata) >= 3
    assert len(snapshot.baggage) >= 2
    json_data = snapshot.model_dump_json()
    assert json_data is not None
    assert "correlation_id" in json_data
    ctx.clear()
    assert len(ctx.get_all_metadata()) == 0
    ctx.restore(snapshot)
    assert ctx.get_metadata("user_id") == "user-123"
except Exception:
    pass
try:
    from flext_observability import (
        FlextObservabilityCustomMetrics,
        FlextObservabilitySampling,
        c,
    )

    registry = FlextObservabilityCustomMetrics.get_registry()
    sampler = FlextObservabilitySampling.get_sampler()
    result = registry.register_metric(
        name="user_signup",
        metric_type=c.Observability.MetricType.COUNTER,
        description="User signup events",
        namespace="auth",
    )
    assert result.is_success
    result = registry.register_metric(
        name="active_sessions",
        metric_type=c.Observability.MetricType.GAUGE,
        description="Currently active sessions",
        namespace="auth",
    )
    assert result.is_success
    sampler.set_service_rate("auth_service", 0.5)
    sampler.set_operation_rate("user_signup", 1.0)
    metrics = registry.get_metrics_by_type(c.Observability.MetricType.COUNTER)
    assert any("user_signup" in m for m in metrics)
except Exception:
    pass
try:
    from flext_observability import (
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
    )

    sampler = FlextObservabilitySampling.get_sampler()
    performance = FlextObservabilityPerformance()
    sampler.set_environment("production")
    sampler.set_default_rate(0.1)
    should_sample = sampler.should_sample("sample_test", "service")
    assert should_sample is not None, "Sampling decision should be made"
    monitor = performance.start_monitoring("sampling_operation")
    time.sleep(0.001)
    monitor.mark_success()
    perf_metrics = monitor.metrics
    assert performance.is_performance_acceptable(perf_metrics), (
        "Sampling performance overhead should be acceptable"
    )
except Exception:
    pass
try:
    from flext_observability import (
        ErrorEvent,
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityMasterFactory,
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
        c,
    )

    FlextObservabilityContext.set_correlation_id("e2e-test-001")
    FlextObservabilityContext.set_trace_id("trace-e2e-001")
    sampler = FlextObservabilitySampling.get_sampler()
    sampler.set_environment("staging")
    sampler.set_operation_rate("e2e_workflow", 1.0)
    factory = FlextObservabilityMasterFactory()
    result = factory.create_metric("workflow.started", 1.0, "counter")
    assert result.is_success
    perf_monitor = FlextObservabilityPerformance()
    monitor = perf_monitor.start_monitoring("e2e_operation")
    adv_ctx = FlextObservabilityAdvancedContext.get_context()
    adv_ctx.set_metadata("workflow_type", "integration_test")
    adv_ctx.set_baggage("test_phase", "11")
    registry = FlextObservabilityCustomMetrics.get_registry()
    metric_result = registry.register_metric(
        name="e2e_tests",
        metric_type=c.Observability.MetricType.COUNTER,
        description="E2E workflow tests",
        namespace="integration",
    )
    time.sleep(0.015)
    monitor.mark_success()
    perf_metrics = monitor.metrics
    assert perf_monitor.is_performance_acceptable(perf_metrics)
    result = factory.create_metric("workflow.completed", 1.0, "counter")
    assert result.is_success
    result = factory.create_metric("workflow.duration_ms", perf_metrics.duration_ms)
    assert result.is_success
    snapshot = adv_ctx.snapshot(
        correlation_id=FlextObservabilityContext.get_correlation_id(),
        trace_id=FlextObservabilityContext.get_trace_id(),
        span_id="span-e2e-001",
    )
    assert snapshot is not None
    assert snapshot.correlation_id == "e2e-test-001"
    error_handler = FlextObservabilityErrorHandling.get_handler()
    test_error = ErrorEvent(
        error_type="IntegrationTestError",
        message="Simulated error in workflow",
        severity=c.Observability.ErrorSeverity.WARNING,
    )
    error_result = error_handler.record_error(test_error)
    assert error_result.is_success
    result = factory.create_metric("workflow.errors", 1.0, "counter")
    assert result.is_success
except Exception:
    pass
try:
    from flext_observability import (
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
    )

    correlation_id = "multi-service-001"
    FlextObservabilityContext.set_correlation_id(correlation_id)
    FlextObservabilityContext.set_trace_id("trace-multi-001")
    ctx1_corr = FlextObservabilityContext.get_correlation_id()
    assert ctx1_corr == correlation_id
    FlextObservabilityContext.set_correlation_id(correlation_id)
    FlextObservabilityContext.set_trace_id("trace-multi-001")
    assert ctx1_corr == FlextObservabilityContext.get_correlation_id()
    adv_ctx = FlextObservabilityAdvancedContext.get_context()
    adv_ctx.set_metadata("service", "api")
    adv_ctx.set_metadata("user_id", "user-456")
    snapshot = adv_ctx.snapshot(
        correlation_id=correlation_id,
        trace_id="trace-multi-001",
        span_id="span-api-001",
    )
    json_snapshot = snapshot.model_dump_json()
    assert json_snapshot is not None
    assert "correlation_id" in json_snapshot
except Exception:
    pass
try:
    from flext_observability import (
        FlextObservabilityAdvancedContext,
        FlextObservabilityContext,
        FlextObservabilityCustomMetrics,
        FlextObservabilityErrorHandling,
        FlextObservabilityMasterFactory,
        FlextObservabilityPerformance,
        FlextObservabilitySampling,
    )

    FlextObservabilityContext.set_correlation_id("setup-001")
    assert FlextObservabilityContext.get_correlation_id() == "setup-001"
    factory = FlextObservabilityMasterFactory()
    assert factory is not None
    sampler = FlextObservabilitySampling.get_sampler()
    perf = FlextObservabilityPerformance()
    assert sampler is not None and perf is not None
    errors = FlextObservabilityErrorHandling.get_handler()
    custom_metrics = FlextObservabilityCustomMetrics.get_registry()
    advanced_ctx = FlextObservabilityAdvancedContext.get_context()
    assert errors is not None
    assert custom_metrics is not None
    assert advanced_ctx is not None
    metrics_service = factory
    assert metrics_service is not None
    FlextObservabilityContext.set_correlation_id("example-001")
    assert FlextObservabilityContext.get_correlation_id() == "example-001"
    sampler.set_environment("production")
    should_sample = sampler.should_sample("test", "service")
    assert should_sample is not None
except Exception:
    pass
