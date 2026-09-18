# from flext-observability_docs/architecture/README.md:289
from __future__ import annotations


class FlextObservabilityMasterFactory:
    """Central factory for all observability entities."""

    def create_metric(
        self, name: str, value: float, unit: str = ""
    ) -> p.Result[FlextMetric]:
        """Create validated metric with domain rules."""
        # Domain validation
        # Entity creation
        # r wrapping
        return r[bool].ok(metric)
