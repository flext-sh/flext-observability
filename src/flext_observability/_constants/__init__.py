# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._constants.base import FlextObservabilityConstantsBase
    from flext_observability._constants.domains import (
        FlextObservabilityConstantsDomains,
    )


__all__: tuple[str, ...] = (
    "FlextObservabilityConstantsBase",
    "FlextObservabilityConstantsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextObservabilityConstantsBase": ".base",
        "FlextObservabilityConstantsDomains": ".domains",
    },
    public_exports=__all__,
    deferred_members={
        "FlextObservabilityConstantsDomains": (
            "DEFAULT_SETTINGS_SERVICE_NAME",
            "DEFAULT_ENVIRONMENT",
            "DEFAULT_FLUSH_INTERVAL",
            "DEFAULT_METRICS_ENABLED",
            "DEFAULT_TRACES_ENABLED",
            "DEFAULT_ALERTS_ENABLED",
            "HTTP_ERROR_STATUS_THRESHOLD",
            "METRIC_VALID_UNITS",
            "MetricType",
            "AlertLevel",
            "TraceStatus",
            "HealthStatus",
            "AlertSeverity",
            "AlertStatus",
            "Storage",
            "Service",
            "SamplingDecision",
            "ErrorSeverity",
            "METRIC_UNIT_COUNT",
            "METRIC_UNIT_PERCENT",
            "METRIC_UNIT_BYTES",
            "METRIC_UNIT_SECONDS",
            "ALERT_LEVEL_INFO",
            "ALERT_LEVEL_WARNING",
            "ALERT_LEVEL_ERROR",
            "ALERT_LEVEL_CRITICAL",
            "TRACE_STATUS_STARTED",
            "TRACE_STATUS_RUNNING",
            "TRACE_STATUS_COMPLETED",
            "TRACE_STATUS_FAILED",
            "HEALTH_STATUS_HEALTHY",
            "HEALTH_STATUS_DEGRADED",
            "HEALTH_STATUS_UNHEALTHY",
            "LOG_LEVEL_DEBUG",
            "LOG_LEVEL_INFO",
            "LOG_LEVEL_WARNING",
            "LOG_LEVEL_ERROR",
            "LOG_LEVEL_CRITICAL",
            "MAX_METRIC_NAME_LENGTH",
            "MAX_TRACE_NAME_LENGTH",
            "MAX_ALERT_MESSAGE_LENGTH",
            "MAX_LOG_MESSAGE_LENGTH",
        ),
    },
)
