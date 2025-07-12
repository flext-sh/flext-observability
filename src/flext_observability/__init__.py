"""FLEXT Observability - Enterprise monitoring with clean architecture.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Application layer exports
from flext_observability.application import AlertService
from flext_observability.application import HealthService
from flext_observability.application import LoggingService
from flext_observability.application import MetricsService
from flext_observability.application import TracingService

# Business metrics components
from flext_observability.business_metrics import BusinessMetric
from flext_observability.business_metrics import BusinessMetricType
from flext_observability.business_metrics import EnterpriseBusinessMetrics

# Configuration
from flext_observability.config import ObservabilitySettings
from flext_observability.config import configure_observability
from flext_observability.config import create_development_config
from flext_observability.config import create_production_config
from flext_observability.config import create_testing_config
from flext_observability.config import get_settings

# Domain layer exports
from flext_observability.domain import Alert
from flext_observability.domain import AlertSeverity
from flext_observability.domain import AlertTriggered
from flext_observability.domain import ComponentName
from flext_observability.domain import Duration
from flext_observability.domain import HealthCheck
from flext_observability.domain import LogEntry
from flext_observability.domain import LogLevel
from flext_observability.domain import Metric
from flext_observability.domain import MetricType
from flext_observability.domain import MetricValue
from flext_observability.domain import ThresholdValue
from flext_observability.domain import Trace
from flext_observability.domain import TraceId
from flext_observability.domain import TraceStatus

# Health monitoring components
from flext_observability.health import ComponentHealth
from flext_observability.health import HealthChecker
from flext_observability.health import HealthStatus

# Logging infrastructure - PRIMARY IMPLEMENTATION
from flext_observability.logging import bind_context
from flext_observability.logging import clear_context
from flext_observability.logging import get_logger
from flext_observability.logging import setup_logging
from flext_observability.logging import with_context

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
