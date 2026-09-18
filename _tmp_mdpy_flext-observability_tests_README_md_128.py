# from flext-observability_tests/README.md:128
from __future__ import annotations


def test_metric_creation_success():
    """Test successful metric creation with r validation."""
    result = flext_create_metric("api_requests", 42.0, "count")

    assert result.success
    assert result.data.name == "api_requests"
    assert result.data.value == 42.0
    assert result.error is None


def test_metric_creation_failure():
    """Test metric creation failure with error handling."""
    result = flext_create_metric("", 42.0, "count")  # Invalid name

    assert result.is_failure
    assert result.data is None
    assert "Invalid metric name" in result.error
