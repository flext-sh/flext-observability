# from flext-observability/docs/standards/python-module-organization.md:357
from __future__ import annotations

from flext_observability import flext_create_metric, flext_create_trace


def flext_create_metric(
    name: str, value: float, unit: str = ""
) -> p.Result[FlextMetric]:
    """Simple API for metric creation."""
    factory = global_factory()
    return factory.create_metric(name, value, unit)


def flext_create_trace(operation_name: str, service_name: str) -> p.Result[FlextTrace]:
    """Simple API for trace creation."""
    factory = global_factory()
    return factory.create_trace(operation_name, service_name)
