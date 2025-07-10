"""Infrastructure layer for observability - external concerns."""

from flext_observability.infrastructure.adapters import HttpHealthChecker
from flext_observability.infrastructure.adapters import InMemoryEventBus
from flext_observability.infrastructure.adapters import OpenTelemetryTraceExporter
from flext_observability.infrastructure.adapters import PrometheusMetricsExporter
from flext_observability.infrastructure.adapters import SlackAlertNotifier
from flext_observability.infrastructure.adapters import StructlogLogAdapter
from flext_observability.infrastructure.persistence.base import AlertRepository
from flext_observability.infrastructure.persistence.base import DashboardRepository
from flext_observability.infrastructure.persistence.base import EventBus
from flext_observability.infrastructure.persistence.base import HealthRepository
from flext_observability.infrastructure.persistence.base import LogRepository
from flext_observability.infrastructure.persistence.base import MetricsRepository
from flext_observability.infrastructure.persistence.base import TraceRepository
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryAlertRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryDashboardRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryHealthRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryLogRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryMetricsRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryTraceRepository,
)

__all__ = [
    "AlertNotifier",
    # Ports
    "AlertRepository",
    "EventBus",
    "HealthChecker",
    "HealthRepository",
    "HttpHealthChecker",
    # Repositories
    "InMemoryAlertRepository",
    "InMemoryDashboardRepository",
    "InMemoryEventBus",
    "InMemoryHealthRepository",
    "InMemoryLogRepository",
    "InMemoryMetricsRepository",
    "InMemoryTraceRepository",
    "LogRepository",
    "MetricsExporter",
    "MetricsRepository",
    "OpenTelemetryTraceExporter",
    # Adapters
    "PrometheusMetricsExporter",
    "SlackAlertNotifier",
    "StructlogLogAdapter",
    "TraceRepository",
]
