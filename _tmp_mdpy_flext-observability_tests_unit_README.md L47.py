# from flext-observability/tests/unit/README.md:47
from __future__ import annotations


def test_flext_metric_domain_validation():
    """Test domain validation in isolation."""
    metric = FlextMetric(name="test_metric", value=42.0, unit="count")
    validation_result = metric.validate_business_rules()
    assert validation_result.success
