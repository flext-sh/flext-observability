# from flext-observability_tests/e2e/README.md:58
from __future__ import annotations


def test_complete_observability_workflow():
    """Test complete observability workflow from creation to export."""

    # 1. Initialize platform
    platform = FlextObservabilityPlatformV2()

    # 2. Create observability data
    metric_result = platform.metric("api_requests", 1, "count")
    trace_result = platform.trace("user_workflow", "web-service")
    alert_result = platform.alert("high_cpu", "warning", "CPU usage high")

    # 3. Validate all operations succeeded
    assert metric_result.success
    assert trace_result.success
    assert alert_result.success

    # 4. Verify data flow and storage
    # Test that metrics are properly stored and retrievable

    # 5. Test export functionality (when implemented)
    # Validate Prometheus-compatible export
