# from flext-observability_tests/README.md:170
from __future__ import annotations


def test_metrics_service_integration(metrics_service, observability_factory):
    """Test service integration with factory patterns."""
    # Create metric via factory
    metric_result = observability_factory.create_metric("test_metric", 100.0)
    assert metric_result.success

    # Record via service
    record_result = metrics_service.record_metric(metric_result.data)
    assert record_result.success
    assert record_result.data.name == "test_metric"
