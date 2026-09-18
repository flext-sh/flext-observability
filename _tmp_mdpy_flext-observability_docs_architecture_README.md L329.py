# from flext-observability/docs/architecture/README.md:329
from __future__ import annotations


class FlextMetricsRepository(Protocol):
    """Repository interface for metrics persistence."""

    def store_metric(self, metric: FlextMetric) -> p.Result[bool]:
        """Store metric with persistence abstraction."""

    def query_metrics(self, criteria: MetricsCriteria) -> p.Result[List[FlextMetric]]:
        """Query metrics with filtering."""
