"""Observability domain models.

Core domain entities for metrics, traces, alerts, health checks, and logging.
Built on flext-core patterns with proper separation of concerns.

This module re-exports entities from entities.py to maintain compatibility
while following FLEXT architecture patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export entities from entities.py to maintain compatibility
from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)

__all__ = [
    "FlextAlert",
    "FlextHealthCheck",
    "FlextLogEntry",
    "FlextMetric",
    "FlextTrace",
    "flext_alert",
    "flext_health_check",
    "flext_metric",
    "flext_trace",
]
