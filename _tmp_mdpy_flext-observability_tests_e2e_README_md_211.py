# from flext-observability_tests/e2e/README.md:211
from __future__ import annotations


def test_performance_under_load(benchmark):
    """Benchmark observability performance under load."""

    def create_observability_data():
        factory = FlextObservabilityMasterFactory()
        return factory.create_metric("perf_test", 1.0, "count")

    result = benchmark(create_observability_data)
    assert result.success
