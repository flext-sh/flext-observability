# from flext-observability_docs/standards/python-module-organization.md:1296
from __future__ import annotations


# ✅ Complete type annotations for observability functions
def create_business_metric(
    operation: str, value: float | Decimal, tags: t.StringDict | None = None
) -> p.Result[FlextMetric]:
    """Create business metric with complete type safety."""
    return flext_create_metric(
        name=f"business_{operation}", value=value, unit="count", tags=tags or {}
    )


# ✅ Generic type usage for observability utilities
from collections.abc import Callable
import typing


def map_observability_result[T, U](
    result: p.Result[T], func: Callable[[T], U]
) -> p.Result[U]:
    """Generic result mapping for observability operations."""
    if result.success:
        return r[bool].ok(func(result.value))
    return r[bool].fail(result.error)


# ✅ Protocol definitions for observability interfaces
class ObservabilityCollector(typing.Protocol):
    """Protocol for observability data collectors."""

    def collect_metric(self, metric: FlextMetric) -> p.Result[bool]:
        """Collect metric data."""
        ...

    def collect_trace(self, trace: FlextTrace) -> p.Result[bool]:
        """Collect trace data."""
        ...


# ❌ Missing type annotations
def create_metric(name, value, unit):  # Missing types
    return flext_create_metric(name, value, unit)
