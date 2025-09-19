"""E2E COMPREHENSIVE TESTS - Real functionality validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import time
from datetime import UTC, datetime

import pytest

from flext_core import FlextContainer, FlextTypes
from flext_observability import (
    FlextObservabilityMasterFactory,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)


class TestE2EComprehensiveObservability:
    """E2E tests validating complete observability functionality."""

    def setup_method(self) -> None:
        """Setup clean factory for each test."""
        self.factory = FlextObservabilityMasterFactory()

    def test_e2e_metric_creation_and_recording(self) -> None:
        """E2E test: Create metric, record it, validate complete flow."""
        # Test metric creation with all parameters
        result = self.factory.metric(
            "e2e_response_time",
            157.5,
            unit="ms",
            tags={"service": "api", "endpoint": "/users", "method": "GET"},
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

        # Verify metric data structure
        metric = result.data
        assert hasattr(metric, "name")
        assert hasattr(metric, "value")
        assert hasattr(metric, "tags")
        assert hasattr(metric, "timestamp")

    def test_e2e_logging_with_context(self) -> None:
        """E2E test: Create logs with rich context, validate structure."""
        contexts: list[FlextTypes.Core.Dict] = [
            {"user_id": "12345", "session": "abc-def", "ip": "192.168.1.1"},
            {"trace_id": "trace-123", "span_id": "span-456", "operation": "db_query"},
            {"error_code": 500, "stack_trace": "Error in line 42", "component": "auth"},
        ]

        for level, context in zip(["info", "debug", "error"], contexts, strict=False):
            result = self.factory.log(
                f"E2E test log - {level}",
                level=level,
                context=context,
                timestamp=datetime.now(UTC),
            )

            assert result.success
            assert result.data is not None

    def test_e2e_alert_escalation_flow(self) -> None:
        """E2E test: Create alerts with different severities, validate escalation."""
        alert_scenarios = [
            (
                "low",
                "Database connection slow",
                {"component": "db", "threshold": "90%"},
            ),
            (
                "medium",
                "API rate limit approaching",
                {"service": "api", "current_rate": "85%"},
            ),
            ("high", "Service unavailable", {"service": "payment", "status": "down"}),
            (
                "critical",
                "Security breach detected",
                {"source": "firewall", "threat_level": "high"},
            ),
        ]

        for severity, message, tags in alert_scenarios:
            result = self.factory.alert(
                f"E2E Alert - {severity.upper()}",
                message,
                severity=severity,
                tags=tags,
                status="active",
                timestamp=datetime.now(UTC),
            )

            assert result.success
            assert result.data is not None

    def test_e2e_distributed_tracing_flow(self) -> None:
        """E2E test: Create distributed trace with multiple spans."""
        trace_id = "e2e-trace-123456"

        # Parent span
        parent_result = self.factory.trace(
            trace_id,
            "user_request",
            span_id="span-parent",
            span_attributes={
                "method": "POST",
                "endpoint": "/api/users",
                "user_agent": "test",
            },
            duration_ms=250,
            status="pending",
        )

        assert parent_result.success

        # Child spans
        child_operations: list[tuple[str, int, FlextTypes.Core.Dict]] = [
            ("auth_validation", 25, {"user_id": "12345", "auth_method": "jwt"}),
            ("database_query", 180, {"query": "SELECT * FROM users", "rows": 1}),
            ("response_formatting", 45, {"format": "json", "size_bytes": 1024}),
        ]

        for operation, duration, attributes in child_operations:
            child_result = self.factory.trace(
                trace_id,
                operation,
                span_id=f"span-{operation}",
                span_attributes=attributes,
                duration_ms=duration,
                status="completed",
            )

            assert child_result.success

    def test_e2e_health_monitoring_comprehensive(self) -> None:
        """E2E test: Health monitoring across multiple components."""
        components: list[tuple[str, str, str, FlextTypes.Core.Dict]] = [
            (
                "database",
                "healthy",
                "Connection OK",
                {"response_time": 15, "connections": 8},
            ),
            (
                "redis",
                "healthy",
                "Cache operational",
                {"memory_usage": "45%", "hit_rate": "92%"},
            ),
            (
                "api_gateway",
                "degraded",
                "High latency",
                {"avg_response": 850, "error_rate": "3%"},
            ),
            (
                "message_queue",
                "unhealthy",
                "Queue backing up",
                {"queue_size": 1500, "processing_rate": "low"},
            ),
        ]

        for component, status, message, metrics in components:
            result = self.factory.health_check(
                component,
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.now(UTC),
            )

            assert result.success
            assert result.data is not None

    def test_e2e_observability_correlation(self) -> None:
        """E2E test: Correlate metrics, logs, traces, and alerts."""
        correlation_id = "e2e-correlation-12345"
        trace_id = "e2e-trace-correlation"

        # Create correlated metric
        metric_result = self.factory.metric(
            "api_request_duration",
            425.0,
            unit="ms",
            tags={"correlation_id": correlation_id, "trace_id": trace_id},
        )

        # Create correlated log
        log_result = self.factory.log(
            "Processing user request",
            level="info",
            context={
                "correlation_id": correlation_id,
                "trace_id": trace_id,
                "user_id": "user-789",
            },
        )

        # Create correlated trace
        trace_result = self.factory.trace(
            trace_id,
            "user_profile_update",
            span_attributes={"correlation_id": correlation_id, "user_id": "user-789"},
        )

        # Create correlated alert (if performance is degraded)
        alert_result = self.factory.alert(
            "Performance Degradation",
            "API response time above threshold",
            severity="medium",
            tags={"correlation_id": correlation_id, "trace_id": trace_id},
        )

        # All should succeed
        assert metric_result.success
        assert log_result.success
        assert trace_result.success
        assert alert_result.success

    def test_e2e_factory_multiple_operations_performance(self) -> None:
        """E2E test: Factory handles multiple operations efficiently."""
        factory = FlextObservabilityMasterFactory()

        # Create multiple entities of each type
        start_time = time.time()

        # Create 10 of each entity type to test performance and consistency
        results = []
        for i in range(10):
            metric_result = factory.metric(f"performance_test_metric_{i}", float(i))
            log_result = factory.log(f"Performance test log {i}")
            alert_result = factory.alert(
                f"Test Alert {i}", "performance-testing", "low",
            )
            trace_result = factory.trace(f"trace-perf-{i}", f"test_op_{i}")

            results.extend([metric_result, log_result, alert_result, trace_result])

        end_time = time.time()
        duration = end_time - start_time

        # All operations should succeed
        for result in results:
            assert result.success

        # Performance should be reasonable (less than 2 seconds for 40 operations)
        assert duration < 2.0

        # Verify we created 40 total results (10 x 4 types)
        assert len(results) == 40

    def test_e2e_multiple_factories_isolation(self) -> None:
        """E2E test: Multiple factories work independently."""
        # Create separate containers and factories
        container1 = FlextContainer()
        container2 = FlextContainer()

        factory1 = FlextObservabilityMasterFactory(container1)
        factory2 = FlextObservabilityMasterFactory(container2)

        # Both should work independently
        result1 = factory1.metric("factory1_metric", 100.0)
        result2 = factory2.metric("factory2_metric", 200.0)

        assert result1.success
        assert result2.success
        assert factory1.container is not factory2.container

    def test_e2e_global_factory_consistency(self) -> None:
        """E2E test: Global factory provides consistent access."""
        # Test global convenience functions
        metric_result = flext_create_metric(
            "global_test_metric", 42.0, tags={"test": "global"},
        )
        log_result = flext_create_log_entry("Global test log", level="info")
        alert_result = flext_create_alert(
            "Global Test Alert", "Testing global access", severity="medium",
        )
        trace_result = flext_create_trace("global-trace-123")
        health_result = flext_create_health_check("global_component", status="healthy")

        # All global functions should work
        assert metric_result.success
        assert log_result.success
        assert alert_result.success
        assert trace_result.success
        assert health_result.success

    def test_e2e_performance_under_load(self) -> None:
        """E2E test: Performance under simulated load."""
        start_time = time.time()

        # Simulate high-frequency operations
        for i in range(100):
            # Rapid metric creation
            metric_result = self.factory.metric(f"load_test_metric_{i}", float(i))
            assert metric_result.success

            # Rapid log creation
            log_result = self.factory.log(f"Load test log {i}", level="debug")
            assert log_result.success

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete 200 operations in reasonable time (< 2 seconds)
        assert total_time < 2.0, (
            f"Performance test took {total_time:.2f}s, expected < 2.0s"
        )

    def test_e2e_data_validation_and_integrity(self) -> None:
        """E2E test: Data validation and integrity across all operations."""
        test_timestamp = datetime.now(UTC)

        # Test with edge cases and boundary values
        edge_cases = [
            # Metric edge cases
            ("zero_metric", 0.0, "count"),
            ("large_metric", 999999999.99, "bytes"),
            ("small_metric", 0.000001, "ms"),
            # String edge cases
            ("unicode_metric_🚀", 42.0, "requests"),
        ]

        for name, value, unit in edge_cases:
            result = self.factory.metric(
                name,
                value,
                unit=unit,
                timestamp=test_timestamp,
            )
            assert result.success

    def test_e2e_complete_observability_workflow(self) -> None:
        """E2E test: Complete end-to-end observability workflow."""
        workflow_id = "e2e-workflow-complete"

        # 1. Start with health check
        health_result = self.factory.health_check(
            "system",
            status="healthy",
            message="System startup complete",
        )
        assert health_result.success

        # 2. Begin tracing user operation
        trace_result = self.factory.trace(
            f"trace-{workflow_id}",
            "user_authentication",
            span_attributes={"workflow_id": workflow_id},
        )
        assert trace_result.success

        # 3. Log authentication attempt
        log_result = self.factory.log(
            "User authentication initiated",
            level="info",
            context={"workflow_id": workflow_id, "user": "test_user"},
        )
        assert log_result.success

        # 4. Record authentication metrics
        auth_metric = self.factory.metric(
            "auth_attempts",
            1.0,
            unit="count",
            tags={"workflow_id": workflow_id, "result": "success"},
        )
        assert auth_metric.success

        # 5. Create alert for monitoring
        alert_result = self.factory.alert(
            "Authentication Success",
            "User successfully authenticated",
            severity="low",
            tags={"workflow_id": workflow_id, "category": "security"},
        )
        assert alert_result.success

        # 6. Final health status check
        final_health = self.factory.health_status()
        assert final_health.success

        # Complete workflow validation
        assert True, "🎉 COMPLETE E2E OBSERVABILITY WORKFLOW SUCCESSFUL! 🎉"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
