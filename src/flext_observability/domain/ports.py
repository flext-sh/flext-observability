"""Domain ports for FLEXT-OBSERVABILITY.

Using flext-core port patterns - NO duplication.
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
        """Write log entry to storage."""

    @abstractmethod
    async def configure_logging(self, config: dict[str, Any]) -> ServiceResult[None]:
        """Configure logging system."""

    @abstractmethod
    async def get_log_level(self) -> ServiceResult[str]:
        """Get current log level."""

    @abstractmethod
    async def set_log_level(self, level: str) -> ServiceResult[None]:
        """Set log level."""


class MetricsService(ABC):
    """Abstract metrics service port."""

    @abstractmethod
    async def record_metric(self, metric: Metric) -> ServiceResult[None]:
        """Record metric."""

    @abstractmethod
    async def get_current_metrics(self) -> ServiceResult[dict[str, Any]]:
        """Get current metrics."""

    @abstractmethod
    async def reset_metrics(self) -> ServiceResult[None]:
        """Reset all metrics."""

    @abstractmethod
    async def export_metrics(self, format: str) -> ServiceResult[str]:
        """Export metrics in specified format."""


class TracingService(ABC):
    """Abstract tracing service port."""

    @abstractmethod
    async def start_trace(self, trace: Trace) -> ServiceResult[None]:
        """Start a trace."""

    @abstractmethod
    async def finish_trace(self, trace: Trace) -> ServiceResult[None]:
        """Finish a trace."""

    @abstractmethod
    async def add_span(self, trace: Trace, span_data: dict[str, Any]) -> ServiceResult[None]:
        """Add span to trace."""

    @abstractmethod
    async def export_traces(self, format: str) -> ServiceResult[str]:
        """Export traces in specified format."""


class AlertService(ABC):
    """Abstract alert service port."""

    @abstractmethod
    async def send_alert(self, alert: Alert) -> ServiceResult[None]:
        """Send alert notification."""

    @abstractmethod
    async def resolve_alert(self, alert: Alert) -> ServiceResult[None]:
        """Resolve alert notification."""

    @abstractmethod
    async def configure_channels(self, channels: dict[str, Any]) -> ServiceResult[None]:
        """Configure alert channels."""

    @abstractmethod
    async def test_alert(self, channel: str) -> ServiceResult[None]:
        """Test alert channel."""


class HealthService(ABC):
    """Abstract health service port."""

    @abstractmethod
    async def run_check(self, health_check: HealthCheck) -> ServiceResult[dict[str, Any]]:
        """Run health check."""

    @abstractmethod
    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health."""

    @abstractmethod
    async def register_check(self, health_check: HealthCheck) -> ServiceResult[None]:
        """Register health check."""

    @abstractmethod
    async def unregister_check(self, check_name: str) -> ServiceResult[None]:
        """Unregister health check."""


class DashboardService(ABC):
    """Abstract dashboard service port."""

    @abstractmethod
    async def render_dashboard(self, dashboard: Dashboard) -> ServiceResult[dict[str, Any]]:
        """Render dashboard with current data."""

    @abstractmethod
    async def export_dashboard(self, dashboard: Dashboard, format: str) -> ServiceResult[str]:
        """Export dashboard configuration."""

    @abstractmethod
    async def import_dashboard(self, config: str, format: str) -> ServiceResult[Dashboard]:
        """Import dashboard configuration."""

    @abstractmethod
    async def get_widget_data(self, widget_config: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Get data for dashboard widget."""
