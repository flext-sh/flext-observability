# from flext-observability_docs/architecture/c4-model.md:406
from __future__ import annotations


class FlextObservabilityServices(u):
    """Unified service class with all observability operations."""

    @classmethod
    def record_counter(cls, name: str, value: float = 1.0) -> p.Result[bool]:
        """Record counter metric with thread safety."""

    @classmethod
    def create_trace(cls, operation: str) -> p.Result[FlextTrace]:
        """Create new distributed trace."""

    @classmethod
    def evaluate_alert(cls, alert: FlextAlert) -> p.Result[bool]:
        """Evaluate alert conditions."""
