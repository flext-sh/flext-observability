"""Compatibility wrapper: re-export observability entities from `entities`.

This file previously duplicated the full entity implementations. To remove
duplication and ensure a single source of truth, it now re-exports the models
implemented in `flext_observability.entities`.
"""

from __future__ import annotations

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
