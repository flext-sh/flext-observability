# from flext-observability/tests/e2e/README.md:111
from __future__ import annotations


def test_factory_service_monitor_integration():
    """Test integration across factory, service, and monitoring components."""

    # 1. Create via factory
    factory = FlextObservabilityMasterFactory()
    metric_result = factory.create_metric("integration_test", 42.0)

    # 2. Process via service
    container = FlextContainer()
    service = FlextMetricsService(container)
    record_result = service.record_metric(metric_result.data)

    # 3. Monitor via decorators
    @flext_monitor_function("e2e_test")
    def test_function():
        return "monitored_result"

    function_result = test_function()

    # 4. Validate end-to-end data flow
    assert metric_result.success
    assert record_result.success
    assert function_result == "monitored_result"
