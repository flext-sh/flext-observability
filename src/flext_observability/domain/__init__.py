"""Domain layer for observability - Clean Architecture domain.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Domain layer with entities and services using flext-core bases.
"""

from __future__ import annotations

# Domain entities using flext-core bases
from flext_observability.domain.entities import (
    # Backwards compatibility
    Alert,
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)

# Domain services
from flext_observability.domain.services import (
    # Backwards compatibility
    AlertDomainService,
    FlextAlertDomainService,
    FlextHealthDomainService,
    FlextMetricsDomainService,
    HealthDomainService,
    MetricsDomainService,
)

__all__ = [
    # Backwards compatibility entities
    "Alert",
    # Backwards compatibility services
    "AlertDomainService",
    # Modern entities
    "FlextAlert",
    # Modern domain services
    "FlextAlertDomainService",
    "FlextHealthCheck",
    "FlextHealthDomainService",
    "FlextLogEntry",
    "FlextMetric",
    "FlextMetricsDomainService",
    "FlextTrace",
    "HealthCheck",
    "HealthDomainService",
    "LogEntry",
    "Metric",
    "MetricsDomainService",
    "Trace",
]
