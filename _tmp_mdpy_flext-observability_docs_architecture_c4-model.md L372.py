# from flext-observability/docs/architecture/c4-model.md:372
from __future__ import annotations


# Core Domain Entities
class FlextMetric(FlextModels.Entity):
    """Immutable metric entity with domain validation."""

    name: str
    value: float
    unit: str
    timestamp: datetime
    tags: t.StrMapping


class FlextTrace(FlextModels.Entity):
    """Distributed trace entity with span hierarchy."""

    trace_id: str
    spans: t.SequenceOf[Span]
    context: TraceContext


class FlextAlert(FlextModels.Entity):
    """Alert entity with severity and routing."""

    name: str
    severity: AlertLevel
    message: str
    condition: AlertCondition
