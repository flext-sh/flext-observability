"""Domain layer - Re-exports models for backwards compatibility.

This module maintains compatibility while redirecting to the new models module.
"""

from __future__ import annotations

# Re-export from models module
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_log_entry,
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
    "flext_log_entry",
    "flext_metric",
    "flext_trace",
]
