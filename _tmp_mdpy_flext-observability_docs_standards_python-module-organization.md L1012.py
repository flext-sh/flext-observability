# from flext-observability/docs/standards/python-module-organization.md:1012
from __future__ import annotations

from flext_observability import flext_create_metric, flext_create_trace


def test_metric_creation_success():
    """Test successful metric creation."""
    result = flext_create_metric("api_requests", 42.0, "count")

    assert result.success
    assert result.value.name == "api_requests"
    assert result.value.value == 42.0
    assert result.value.unit == "count"
    assert result.error is None


def test_metric_creation_failure():
    """Test metric creation validation failure."""
    result = flext_create_metric("", 42.0, "count")  # Empty name

    assert result.failure
    assert result.value is None
    assert "Invalid metric name" in result.error


def test_observability_chaining():
    """Test railway-oriented chaining of observability operations."""

    def create_observability_data(operation: str) -> p.Result[m.Dict]:
        return flext_create_metric(f"{operation}_requests", 1, "count").flat_map(
            lambda metric: flext_create_trace(operation, "test-service").map(
                lambda trace: {"metric": metric, "trace": trace}
            )
        )

    result = create_observability_data("user_login")

    assert result.success
    assert "metric" in result.value
    assert "trace" in result.value
    assert result.value["metric"].name == "user_login_requests"
    assert result.value["trace"].operation_name == "user_login"


def test_observability_failure_propagation():
    """Test failure propagation in observability chains."""

    def create_invalid_observability() -> p.Result[m.Dict]:
        return flext_create_metric("", 1, "count").flat_map(  # Invalid metric name
            lambda metric: flext_create_trace(
                "operation", "service"
            ).map(  # Should not execute
                lambda trace: {"metric": metric, "trace": trace}
            )
        )

    result = create_invalid_observability()

    assert result.failure
    assert "Invalid metric name" in result.error
