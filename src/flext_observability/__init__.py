"""FLEXT Observability - Enterprise monitoring with clean architecture.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Application layer exports
from __future__ import annotations

from flext_observability.application import (
    AlertService,
    HealthService,
    LoggingService,
    MetricsService,
    TracingService,
)

# Business metrics components
from flext_observability.business_metrics import (
    BusinessMetric,
    BusinessMetricType,
    EnterpriseBusinessMetrics,
)

# Configuration
from flext_observability.config import (
    ObservabilitySettings,
    configure_observability,
    create_development_config,
    create_production_config,
    create_testing_config,
    get_settings,
)

# Domain layer exports
from flext_observability.domain import (
    Alert,
    AlertSeverity,
    AlertTriggered,
    ComponentName,
    Duration,
    HealthCheck,
    LogEntry,
    LogLevel,
    Metric,
    MetricType,
    MetricValue,
    ThresholdValue,
    Trace,
    TraceId,
    TraceStatus,
)

# Health monitoring components
from flext_observability.health import ComponentHealth, HealthChecker, HealthStatus

# Logging infrastructure - PRIMARY IMPLEMENTATION
from flext_observability.logging import (
    bind_context,
    clear_context,
    get_logger,
    setup_logging,
    with_context,
)

# Metrics collection
from flext_observability.metrics import MetricsCollector

# Simple API for easy adoption (TEMPORARILY DISABLED)
# from flext_observability.simple_api import check_health
# from flext_observability.simple_api import collect_metric
# from flext_observability.simple_api import create_alert
# from flext_observability.simple_api import get_system_overview
# from flext_observability.simple_api import log_message
# from flext_observability.simple_api import setup_observability
# from flext_observability.simple_api import start_trace

__version__ = "0.7.0"

__all__ = [
    # Domain entities and value objects
    "Alert",
    # Application services
    "AlertService",
    "AlertSeverity",
    "AlertTriggered",
    "BusinessMetric",
    "BusinessMetricType",
    "ComponentHealth",
    "ComponentName",
    "Duration",
    "EnterpriseBusinessMetrics",
    "HealthCheck",
    "HealthChecker",
    "HealthService",
    "HealthStatus",
    "LogEntry",
    "LogLevel",
    "LoggingService",
    "Metric",
    "MetricType",
    "MetricValue",
    "MetricsCollector",
    "MetricsService",
    # Configuration
    "ObservabilitySettings",
    "ThresholdValue",
    "Trace",
    "TraceId",
    "TraceStatus",
    "TracingService",
    # Logging infrastructure - PRIMARY IMPLEMENTATION (TEMPORARILY DISABLED)
    "bind_context",
    # "check_health",
    "clear_context",
    # Simple API (TEMPORARILY DISABLED)
    # "collect_metric",
    "configure_observability",
    # "create_alert",
    "create_development_config",
    "create_production_config",
    "create_testing_config",
    "get_logger",
    "get_settings",
    # "get_system_overview",
    # "log_message",
    "setup_logging",
    # "setup_observability",
    # "start_trace",
    "with_context",
]
