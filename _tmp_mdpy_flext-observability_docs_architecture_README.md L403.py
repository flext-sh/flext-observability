# from flext-observability/docs/architecture/README.md:403
from __future__ import annotations


# Future extension point example
class FlextObservabilityPlugin(Protocol):
    """Plugin interface for extending observability."""

    def on_metric_created(self, metric: FlextMetric) -> p.Result[bool]:
        """Hook called when metrics are created."""

    def on_trace_started(self, trace: FlextTrace) -> p.Result[bool]:
        """Hook called when traces are started."""
