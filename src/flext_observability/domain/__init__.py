"""Domain layer for observability - pure business logic.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core.domain.shared_types import AlertSeverity
from flext_core.domain.types import LogLevel, MetricType, TraceStatus

from flext_observability.domain.entities import (
    Alert,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)
from flext_observability.domain.events import (
    AlertTriggered,
    HealthCheckCompleted,
    MetricCollected,
    TraceCompleted,
    TraceStarted,
)
from flext_observability.domain.services import (
    AlertingService,
    HealthAnalysisService,
    MetricsAnalysisService,
)
from flext_observability.domain.specifications import (
    AlertThresholdSpec,
    HealthyComponentSpec,
    MetricValueRangeSpec,
)
from flext_observability.domain.value_objects import (
    ComponentName,
    Duration,
    MetricValue,
    ThresholdValue,
    TraceId,
)

__all__ = [
    # Entities
    "Alert",
    # Value Objects
    "AlertSeverity",
    # Specifications
    "AlertThresholdSpec",
    # Events
    "AlertTriggered",
    # Services
    "AlertingService",
    "ComponentName",
    "Duration",
    "HealthAnalysisService",
    "HealthCheck",
    "HealthCheckCompleted",
    "HealthyComponentSpec",
    "LogEntry",
    "LogLevel",
    "Metric",
    "MetricCollected",
    "MetricType",
    "MetricValue",
    "MetricValueRangeSpec",
    "MetricsAnalysisService",
    "ThresholdValue",
    "Trace",
    "TraceCompleted",
    "TraceId",
    "TraceStarted",
    "TraceStatus",
]
