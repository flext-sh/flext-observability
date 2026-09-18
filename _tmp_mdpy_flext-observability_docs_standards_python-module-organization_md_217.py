# from flext-observability_docs/standards/python-module-organization.md:217
from __future__ import annotations

from flext_cli import u
from flext_core import FlextSettings
from flext_observability import FlextMetric, FlextTrace

class FlextMetric(FlextModels.Entity):
    """Observability metric with domain validation."""
    name: str
    value: float | Decimal
    unit: str = ""
    tags: t.StringDict = field(default_factory=dict)
    metric_type: str = "gauge"

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate metric domain rules."""
        if not self.name or not isinstance(self.name, str):
            return r[bool].fail("Invalid metric name")
        try:
            float(self.value)
        except (ValueError, TypeError):
            return r[bool].fail("Invalid metric value")
        return r[bool].| ok(value=True)
