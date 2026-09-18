# from flext-observability/docs/api/simple-api.md:126
from __future__ import annotations

from flext_observability import flext_create_metric

# Basic metric
result = flext_create_metric("response_time", 150.5, "milliseconds")
if result.success:
    print(f"Created: {result.value.name} = {result.value.value}")

# Business metric with tags
result = flext_create_metric(
    name="orders_processed",
    value=42,
    unit="count",
    tags={"service": "order-api", "region": "us-east"},
    metric_type="counter",
)

# High-precision financial metric
from decimal import Decimal

result = flext_create_metric(
    name="transaction_amount",
    value=Decimal("1234.56"),
    unit="USD",
    tags={"account_type": "premium"},
)
