"""Domain layer for observability - Clean Architecture domain.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Domain layer with entities and services using flext-core bases.
"""

from __future__ import annotations

# Domain entities using flext-core bases
from flext_observability.domain.entities import (
    Alert,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)

# Domain services
from flext_observability.domain.services import (
    AlertDomainService,
    HealthDomainService,
    MetricsDomainService,
)

__all__ = [
    # Entities
    "Alert",
    # Domain Services
    "AlertDomainService",
    "HealthCheck",
    "HealthDomainService",
    "LogEntry",
    "Metric",
    "MetricsDomainService",
    "Trace",
]
