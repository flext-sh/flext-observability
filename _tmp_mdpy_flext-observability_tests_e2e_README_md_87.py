# from flext-observability_tests/e2e/README.md:87
from __future__ import annotations


def test_production_monitoring_scenario():
    """Test production-like monitoring scenario."""

    # Simulate production load
    for i in range(100):
        # Create various metrics as they would appear in production
        api_metric = flext_create_metric(f"api_request_{i}", 1, "count")
        response_time = flext_create_metric(
            "response_time", random.uniform(50, 500), "ms"
        )

        # Validate each metric creation
        assert api_metric.success
        assert response_time.success

    # Validate aggregation and performance under load
