"""Infrastructure layer for observability - external concerns.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_observability.infrastructure.adapters import (
    HttpHealthChecker,
    InMemoryEventBus,
    OpenTelemetryTraceExporter,
    PrometheusMetricsExporter,
    SlackAlertNotifier,
    StructlogLogAdapter,
)
from flext_observability.infrastructure.persistence.base import (
    AlertRepository,
    DashboardRepository,
    EventBus,
    HealthRepository,
    LogRepository,
    MetricsRepository,
    TraceRepository,
)
from flext_observability.infrastructure.persistence.repositories import (
    InMemoryAlertRepository,
    InMemoryDashboardRepository,
    InMemoryHealthRepository,
    InMemoryLogRepository,
    InMemoryMetricsRepository,
    InMemoryTraceRepository,
)

__all__ = [
    "AlertRepository",
    "DashboardRepository",
    "EventBus",
    "HealthRepository",
    "HttpHealthChecker",
    "InMemoryAlertRepository",
    "InMemoryDashboardRepository",
    "InMemoryEventBus",
    "InMemoryHealthRepository",
    "InMemoryLogRepository",
    "InMemoryMetricsRepository",
    "InMemoryTraceRepository",
    "LogRepository",
    "MetricsRepository",
    "OpenTelemetryTraceExporter",
    "PrometheusMetricsExporter",
    "SlackAlertNotifier",
    "StructlogLogAdapter",
    "TraceRepository",
]
