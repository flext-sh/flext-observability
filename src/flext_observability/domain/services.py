"""Domain Services - Business logic using flext-core bases.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Domain Layer
Following SOLID, KISS, DRY principles using flext-core as foundation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextDomainService, FlextResult

if TYPE_CHECKING:
    from flext_observability.domain.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextMetric,
    )


class FlextMetricsDomainService(FlextDomainService):
    """Domain service for metrics business logic - Single Responsibility."""

    def validate_metric(self, metric: FlextMetric) -> FlextResult[bool]:
        """Validate metric according to business rules."""
        if not metric.name:
            return FlextResult.fail("Metric name is required")

        if metric.value < 0 and metric.unit in {"count", "percentage"}:
            return FlextResult.fail("Count and percentage metrics cannot be negative")

        return FlextResult.ok(success=True)


class FlextAlertDomainService(FlextDomainService):
    """Domain service for alert business logic - Single Responsibility."""

    def should_escalate(self, alert: FlextAlert) -> FlextResult[bool]:
        """Determine if alert should be escalated based on business rules."""
        if alert.severity == "critical":
            return FlextResult.ok(success=True)

        return FlextResult.ok(success=False)


class FlextHealthDomainService(FlextDomainService):
    """Domain service for health check business logic - Single Responsibility."""

    def calculate_overall_health(
        self,
        health_checks: list[FlextHealthCheck],
    ) -> FlextResult[str]:
        """Calculate overall system health from individual checks."""
        if not health_checks:
            return FlextResult.ok("unknown")

        if any(hc.status == "failed" for hc in health_checks):
            return FlextResult.ok("unhealthy")

        if any(hc.status == "degraded" for hc in health_checks):
            return FlextResult.ok("degraded")

        if all(hc.status == "healthy" for hc in health_checks):
            return FlextResult.ok("healthy")

        return FlextResult.ok("unknown")


# Backwards compatibility aliases
MetricsDomainService = FlextMetricsDomainService
AlertDomainService = FlextAlertDomainService
HealthDomainService = FlextHealthDomainService
