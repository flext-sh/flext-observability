"""Domain ports for FLEXT-OBSERVABILITY.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from flext_core.domain import ServiceResult
    from flext_observability.domain.entities import Alert
    from flext_observability.domain.entities import Dashboard
    from flext_observability.domain.entities import HealthCheck
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace


class LogService(ABC):
    """Abstract log service port."""

    @abstractmethod
    async def write_log(self, log_entry: LogEntry) -> ServiceResult[None]:
        """Write a log entry."""
        ...

    @abstractmethod
    async def configure_logging(self, config: dict[str, Any]) -> ServiceResult[None]:
        """Configure logging settings."""
        ...

    @abstractmethod
    async def get_log_level(self) -> ServiceResult[str]:
        """Get current log level."""
        ...

    @abstractmethod
    async def set_log_level(self, level: str) -> ServiceResult[None]:
        """Set log level."""
        ...


class MetricsService(ABC):
    """Abstract metrics service port."""

    @abstractmethod
    async def record_metric(self, metric: Metric) -> ServiceResult[None]:
        """Record a metric."""
        ...

    @abstractmethod
    async def get_current_metrics(self) -> ServiceResult[dict[str, Any]]:
        """Get current metrics."""
        ...

    @abstractmethod
    async def reset_metrics(self) -> ServiceResult[None]:
        """Reset all metrics."""
        ...

    @abstractmethod
    async def export_metrics(self, format: str) -> ServiceResult[str]:
        """Export metrics in specified format."""
        ...


class TracingService(ABC):
    """Abstract tracing service port."""

    @abstractmethod
    async def start_trace(self, trace: Trace) -> ServiceResult[None]:
        """Start a trace."""
        ...

    @abstractmethod
    async def finish_trace(self, trace: Trace) -> ServiceResult[None]:
        """Finish a trace."""
        ...

    @abstractmethod
    async def add_span(
        self,
        trace: Trace,
        span_data: dict[str, Any],
    ) -> ServiceResult[None]:
        """Add span to trace."""
        ...

    @abstractmethod
    async def export_traces(self, format: str) -> ServiceResult[str]:
        """Export traces in specified format."""
        ...


class AlertService(ABC):
    """Abstract alert service port."""

    @abstractmethod
    async def trigger_alert(self, alert: Alert) -> ServiceResult[None]:
        """Trigger an alert."""
        ...

    @abstractmethod
    async def acknowledge_alert(self, alert_id: str) -> ServiceResult[None]:
        """Acknowledge an alert."""
        ...

    @abstractmethod
    async def resolve_alert(self, alert_id: str) -> ServiceResult[None]:
        """Resolve an alert."""
        ...

    @abstractmethod
    async def get_active_alerts(self) -> ServiceResult[list[Alert]]:
        """Get all active alerts."""
        ...


class HealthService(ABC):
    """Abstract health service port."""

    @abstractmethod
    async def perform_health_check(self, check: HealthCheck) -> ServiceResult[None]:
        """Perform a health check."""
        ...

    @abstractmethod
    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health."""
        ...

    @abstractmethod
    async def register_health_check(self, check: HealthCheck) -> ServiceResult[None]:
        """Register a health check."""
        ...


class DashboardService(ABC):
    """Abstract dashboard service port."""

    @abstractmethod
    async def create_dashboard(self, dashboard: Dashboard) -> ServiceResult[None]:
        """Create a dashboard."""
        ...

    @abstractmethod
    async def update_dashboard(self, dashboard: Dashboard) -> ServiceResult[None]:
        """Update a dashboard."""
        ...

    @abstractmethod
    async def get_dashboard(self, dashboard_id: str) -> ServiceResult[Dashboard]:
        """Get a dashboard by ID."""
        ...

    @abstractmethod
    async def list_dashboards(self) -> ServiceResult[list[Dashboard]]:
        """List all dashboards."""
        ...


__all__ = [
    "AlertService",
    "DashboardService",
    "HealthService",
    "LogService",
    "MetricsService",
    "TracingService",
]
