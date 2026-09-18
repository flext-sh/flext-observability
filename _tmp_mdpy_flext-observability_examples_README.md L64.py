# from flext-observability/examples/README.md:64
from __future__ import annotations

# Example from 01_functional.py
from flext_observability import flext_create_metric, flext_create_trace


def create_business_metrics():
    """Demonstrate basic metrics creation."""
    # Performance metric
    response_time = flext_create_metric(
        name="api_response_time",
        value=150.5,
        unit="milliseconds",
        tags={"service": "user-api", "endpoint": "/users"},
    )

    # Business metric
    user_count = flext_create_metric(
        name="active_users",
        value=1250,
        unit="count",
        tags={"region": "us-east", "tier": "premium"},
    )

    return response_time, user_count
