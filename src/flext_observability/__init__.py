"""FLEXT Observability - Enterprise Observability Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Modern observability platform following Clean Architecture and Domain-Driven Design.
Built on Python 3.13 with enterprise-grade monitoring, logging, metrics, and tracing.
"""

from __future__ import annotations

import importlib.metadata

# Import from flext-core for foundational patterns
from flext_core import FlextContainer, FlextResult

try:
    __version__ = importlib.metadata.version("flext-observability")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.8.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Core structured logging
# Application services
from flext_observability.application.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)

# Domain entities
from flext_observability.domain.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)

# Platform
from flext_observability.platform import FlextObservabilityPlatform

# Simple API
from flext_observability.simple_api import (
    create_flext_alert,
    create_flext_health_check,
    create_flext_log_entry,
    create_flext_metric,
    create_flext_trace,
)
from flext_observability.structured_logging import (
    LoggingConfig,
    get_logger,
    setup_logging,
)

# Main FlextObservability aliases
FlextObservability = FlextObservabilityPlatform
FlextObservabilityResult = FlextResult

# Prefixed helper functions
flext_observability_create_metric = create_flext_metric
flext_observability_create_log_entry = create_flext_log_entry
flext_observability_create_trace = create_flext_trace
flext_observability_create_alert = create_flext_alert
flext_observability_create_health_check = create_flext_health_check


def create_flext_observability_platform(
    config: dict[str, object] | None = None,
) -> FlextObservabilityPlatform:
    """Create unified FLEXT Observability platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextObservabilityPlatform instance

    """
    return FlextObservabilityPlatform(config or {})


flext_observability_create_platform = create_flext_observability_platform

__all__ = [
    "FlextAlert",
    "FlextAlertService",
    "FlextContainer",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    "FlextObservability",
    "FlextObservabilityPlatform",
    "FlextObservabilityResult",
    "FlextResult",
    "FlextTrace",
    "FlextTracingService",
    "LoggingConfig",
    "__version__",
    "__version_info__",
    "create_flext_alert",
    "create_flext_health_check",
    "create_flext_log_entry",
    "create_flext_metric",
    "create_flext_observability_platform",
    "create_flext_trace",
    "flext_observability_create_alert",
    "flext_observability_create_health_check",
    "flext_observability_create_log_entry",
    "flext_observability_create_metric",
    "flext_observability_create_platform",
    "flext_observability_create_trace",
    "get_logger",
    "setup_logging",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"
