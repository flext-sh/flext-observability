"""Domain Services - Business logic using flext-core bases.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Domain Layer
Following SOLID, KISS, DRY principles using flext-core as foundation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import BaseDomainService, ServiceResult

if TYPE_CHECKING:
    from flext_observability.domain.entities import (
        Alert,
        HealthCheck,
        LogEntry,
        Metric,
        Trace,
    )


class MetricsDomainService(BaseDomainService):
    """Domain service for metrics business logic - Single Responsibility."""

    def validate_metric(self, metric: Metric) -> ServiceResult[bool]:
        """Validate metric according to business rules."""
        if not metric.name:
            return ServiceResult.error("Metric name is required")

        if metric.value < 0 and metric.unit in ["count", "percentage"]:
            return ServiceResult.error("Count and percentage metrics cannot be negative")

        return ServiceResult.ok(True)


class AlertDomainService(BaseDomainService):
    """Domain service for alert business logic - Single Responsibility."""

    def should_escalate(self, alert: Alert) -> ServiceResult[bool]:
        """Determine if alert should be escalated based on business rules."""
        if alert.severity == "critical":
            return ServiceResult.ok(True)

        return ServiceResult.ok(False)


class HealthDomainService(BaseDomainService):
    """Domain service for health check business logic - Single Responsibility."""

    def calculate_overall_health(self, health_checks: list[HealthCheck]) -> ServiceResult[str]:
        """Calculate overall system health from individual checks."""
        if not health_checks:
            return ServiceResult.ok("unknown")

        if any(hc.status == "failed" for hc in health_checks):
            return ServiceResult.ok("unhealthy")

        if any(hc.status == "degraded" for hc in health_checks):
            return ServiceResult.ok("degraded")

        if all(hc.status == "healthy" for hc in health_checks):
            return ServiceResult.ok("healthy")

        return ServiceResult.ok("unknown")
