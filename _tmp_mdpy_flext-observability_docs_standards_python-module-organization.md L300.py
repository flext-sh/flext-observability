# from flext-observability/docs/standards/python-module-organization.md:300
from __future__ import annotations

from flext_observability import FlextObservabilityMasterFactory


class FlextObservabilityMasterFactory:
    """Central factory for all observability entities."""

    def create_metric(
        self, name: str, value: float, unit: str = ""
    ) -> p.Result[FlextMetric]:
        """Create validated metric with domain rules."""
        try:
            metric = FlextMetric(
                name=name, value=value, unit=unit, timestamp=datetime.now(UTC)
            )

            validation_result = metric.validate_business_rules()
            if validation_result.failure:
                return validation_result

            return r[bool].ok(metric)
        except Exception as e:
            return r[bool].fail(f"Metric creation failed: {e!s}")

    def create_trace(
        self, operation_name: str, service_name: str
    ) -> p.Result[FlextTrace]:
        """Create validated trace span."""
        try:
            trace = FlextTrace(
                operation_name=operation_name,
                service_name=service_name,
                start_time=datetime.now(UTC),
            )
            return r[bool].ok(trace)
        except Exception as e:
            return r[bool].fail(f"Trace creation failed: {e!s}")
