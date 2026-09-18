# from flext-observability_docs/standards/python-module-organization.md:1162
from __future__ import annotations

from flext_observability import FlextMetricsService, FlextObservabilityMasterFactory


@pytest.fixture
def clean_container():
    """Provide clean container for each test."""
    return FlextContainer()


@pytest.fixture
def metrics_service(clean_container):
    """Provide metrics service with clean container."""
    return FlextMetricsService(clean_container)


@pytest.fixture
def observability_factory():
    """Provide fresh observability factory."""
    return FlextObservabilityMasterFactory()


def test_metrics_service_record_metric(metrics_service, observability_factory):
    """Test metrics service metric recording."""
    # Create metric using factory
    metric_result = observability_factory.create_metric("test_metric", 100.0, "count")
    assert metric_result.success

    # Record metric using service
    record_result = metrics_service.record_metric(metric_result.value)

    assert record_result.success
    assert record_result.value.name == "test_metric"
    assert record_result.value.value == 100.0


def test_metrics_service_prometheus_export(metrics_service, observability_factory):
    """Test Prometheus format export."""
    # Create and record multiple metrics
    metrics_data = [
        ("api_requests", 150.0, "count"),
        ("response_time", 250.5, "milliseconds"),
        ("error_rate", 0.05, "ratio"),
    ]

    for name, value, unit in metrics_data:
        metric_result = observability_factory.create_metric(name, value, unit)
        assert metric_result.success

        record_result = metrics_service.record_metric(metric_result.value)
        assert record_result.success

    # Export to Prometheus format
    export_result = metrics_service.export_prometheus_format()

    assert export_result.success
    prometheus_output = export_result.value

    # Verify Prometheus format
    assert "# TYPE api_requests gauge" in prometheus_output
    assert "api_requests 150.0" in prometheus_output
    assert "# TYPE response_time gauge" in prometheus_output
    assert "response_time 250.5" in prometheus_output


def test_metrics_service_memory_management(metrics_service, observability_factory):
    """Test metrics service memory management."""
    # Create metrics beyond memory limit to test cleanup
    for i in range(1200):  # Exceeds default limit of 1000
        metric_result = observability_factory.create_metric(
            f"test_metric_{i}", float(i), "count"
        )
        assert metric_result.success

        record_result = metrics_service.record_metric(metric_result.value)
        assert record_result.success

    # Verify memory management kicked in
    total_metrics = len(metrics_service._metrics_store)
    assert total_metrics <= 1000  # Should have cleaned up to stay within limits
