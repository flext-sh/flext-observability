# from flext-observability_tests/README.md:153
from __future__ import annotations


def test_metric_domain_validation():
    """Test domain rule validation for metrics."""
    metric = FlextMetric(name="cpu_usage", value=75.5, unit="percent")

    validation_result = metric.validate_business_rules()

    assert validation_result.success
    assert metric.name == "cpu_usage"
    assert metric.value == 75.5
