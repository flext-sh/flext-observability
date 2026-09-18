# from flext-observability/tests/integration/README.md:53
from __future__ import annotations


def test_metrics_service_with_factory_integration():
    """Test metrics service integration with factory."""
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)
    metrics_service = FlextMetricsService(container)

    # Create metric via factory
    metric_result = factory.create_metric("integration_test", 42.0)
    assert metric_result.success

    # Process via service
    record_result = metrics_service.record_metric(metric_result.data)
    assert record_result.success
