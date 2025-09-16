"""Unified observability service implementing FLEXT patterns.

REFACTORED: Eliminated factory patterns, wrappers, and multiple classes.
Uses unified service with direct composition following zero tolerance policy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from datetime import UTC, datetime

from flext_core import (
    FlextContainer,
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextTypes,
)

from flext_observability.entities import (
    FlextUtilitiesGenerators,
)
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


def _generate_utc_datetime() -> datetime:
    """Generate UTC datetime using flext-core pattern."""
    return datetime.now(tz=UTC)


class FlextObservabilityService(FlextDomainService):
    """Unified observability service implementing FLEXT patterns.

    REFACTORED: No longer a factory pattern - uses direct service composition.
    Single responsibility for observability operations with proper SOLID principles.
    """

    def __init__(self, **data: object) -> None:
        """Initialize observability service with proper composition."""
        super().__init__(**data)
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Direct service composition - no factory patterns
        self._metrics_service = FlextMetricsService(self._container)
        self._logging_service = FlextLoggingService(self._container)
        self._tracing_service = FlextTracingService(self._container)
        self._alert_service = FlextAlertService(self._container)
        self._health_service = FlextHealthService(self._container)

    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = "",
        tags: dict[str, str] | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextMetric]:
        """Record metric using direct service call - no wrapper patterns."""
        if not name or not isinstance(value, (int, float)):
            return FlextResult[FlextMetric].fail("Invalid metric parameters")

        metric = FlextMetric(
            name=name,
            value=float(value),
            unit=unit,
            tags=tags or {},
            timestamp=timestamp or _generate_utc_datetime(),
        )

        return self._metrics_service.record_metric(metric)

    def create_log_entry(
        self,
        message: str,
        level: str = "info",
        context: FlextTypes.Core.Dict | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextLogEntry]:
        """Create log entry using direct service call - no wrapper patterns."""
        if not message:
            return FlextResult[FlextLogEntry].fail("Message is required")

        log_entry = FlextLogEntry(
            message=message,
            level=level,
            context=context or {},
            timestamp=timestamp or _generate_utc_datetime(),
        )

        return self._logging_service.log_entry(log_entry)

    def create_alert(
        self,
        title: str,
        message: str,
        severity: str = "low",
        tags: dict[str, str] | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextAlert]:
        """Create alert using direct service call - no wrapper patterns."""
        if not title or not message:
            return FlextResult[FlextAlert].fail("Title and message are required")

        alert = FlextAlert(
            title=title,
            message=message,
            severity=severity,
            timestamp=timestamp or _generate_utc_datetime(),
            tags=tags or {},
        )

        return self._alert_service.create_alert(alert)

    def start_trace(
        self,
        operation: str,
        trace_id: str | None = None,
        span_id: str | None = None,
        status: str = "pending",
        span_attributes: FlextTypes.Core.Dict | None = None,
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextTrace]:
        """Start trace using direct service call - no wrapper patterns."""
        if not operation:
            return FlextResult[FlextTrace].fail("Operation is required")

        trace = FlextTrace(
            operation=operation,
            trace_id=trace_id or FlextUtilitiesGenerators.generate_uuid(),
            span_id=span_id or f"span-{int(time.time() * 1000)}",
            status=status,
            timestamp=timestamp or _generate_utc_datetime(),
            span_attributes=span_attributes or {},
        )

        return self._tracing_service.start_trace(trace)

    def perform_health_check(
        self,
        component: str,
        status: str = "healthy",
        message: str = "",
        timestamp: datetime | None = None,
    ) -> FlextResult[FlextHealthCheck]:
        """Perform health check using direct service call - no wrapper patterns."""
        if not component:
            return FlextResult[FlextHealthCheck].fail("Component is required")

        health_check = FlextHealthCheck(
            component=component,
            status=status,
            timestamp=timestamp or _generate_utc_datetime(),
            message=message,
        )

        return self._health_service.check_health(health_check)

    def get_overall_health(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get overall health status using direct service call."""
        return self._health_service.get_overall_health()


__all__: FlextTypes.Core.StringList = [
    "FlextObservabilityService",
]
