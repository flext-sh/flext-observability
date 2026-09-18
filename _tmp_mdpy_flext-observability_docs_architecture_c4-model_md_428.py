# from flext-observability_docs/architecture/c4-model.md:428
from __future__ import annotations


class FlextObservabilityMasterFactory:
    """Central factory for all observability entities."""

    def create_metric(
        self, name: str, value: float, unit: str
    ) -> p.Result[FlextMetric]:
        """Create validated metric entity."""

    def create_trace(self, operation: str, context: dict) -> p.Result[FlextTrace]:
        """Create validated trace entity."""
