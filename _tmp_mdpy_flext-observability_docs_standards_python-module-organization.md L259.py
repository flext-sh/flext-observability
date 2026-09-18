# from flext-observability/docs/standards/python-module-organization.md:259
from __future__ import annotations

from flext_observability import FlextMetricsService


class FlextMetricsService:
    """Application service for metrics operations."""

    def __init__(self, container: FlextContainer) -> None:
        self._container = container
        self._metrics_store: t.MappingKV[str, FlextMetric] = {}

    def record_metric(self, metric: FlextMetric) -> p.Result[FlextMetric]:
        """Record metric with business validation."""
        validation_result = metric.validate_business_rules()
        if validation_result.failure:
            return r[bool].fail(f"Metric validation failed: {validation_result.error}")

        self._metrics_store[metric.id] = metric
        return r[bool].ok(metric)

    def export_prometheus_format(self) -> p.Result[str]:
        """Export metrics in Prometheus format."""
        # Business logic for Prometheus export
        return r[bool].ok(prometheus_output)
