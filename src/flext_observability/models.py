"""Compatibility models module mapping to observability_models.

Re-exports domain models for tests that import flext_observability.models directly.
"""

from __future__ import annotations

from flext_observability.observability_models import (
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
