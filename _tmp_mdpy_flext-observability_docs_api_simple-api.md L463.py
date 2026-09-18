# from flext-observability/docs/api/simple-api.md:463
from __future__ import annotations


def create_system_metrics() -> t.SequenceOf[r[FlextMetric]]:
    """Create multiple metrics with error handling."""
    metrics_to_create = [
        ("cpu_usage", 75.2, "percent"),
        ("memory_usage", 1024, "MB"),
        ("disk_usage", 85.5, "percent"),
        ("active_connections", 42, "count"),
    ]

    results = []
    for name, value, unit in metrics_to_create:
        result = flext_create_metric(name, value, unit)
        results.append(result)

        if result.failure:
            print(f"⚠️  Failed to create {name}: {result.error}")

    return results
