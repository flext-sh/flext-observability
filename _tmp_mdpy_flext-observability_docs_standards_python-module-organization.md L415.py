# from flext-observability/docs/standards/python-module-organization.md:415
from __future__ import annotations

from flext_observability import FlextObservabilityRepository

class FlextObservabilityRepository:
    """Repository for observability data access."""

    def __init__(self) -> None:
        self._metrics: t.MappingKV[str, FlextMetric] = {}
        self._traces: t.MappingKV[str, FlextTrace] = {}
        self._alerts: t.MappingKV[str, FlextAlert] = {}

    def store_metric(self, metric: FlextMetric) -> p.Result[bool]:
        """Store metric with validation."""
        if not metric.id:
            return r[bool].fail("Metric must have ID")

        self._metrics[metric.id] = metric
        return r[bool].| ok(value=True)

    def find_metrics_by_name(self, name: str) -> p.Result[Sequence[FlextMetric]]:
        """Find metrics by name pattern."""
        matching_metrics = [
            metric for metric in self._metrics.values()
            if metric.name == name
        ]
        return r[bool].ok(matching_metrics)
