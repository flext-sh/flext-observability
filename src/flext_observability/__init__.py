"""FLEXT Observability - Enterprise Observability Foundation Library.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Comprehensive observability foundation library providing metrics collection,
distributed tracing, health monitoring, alerting, and structured logging
capabilities for the FLEXT ecosystem. Built following Clean Architecture
and Domain-Driven Design principles with enterprise-grade reliability.

This package serves as the central observability layer for all FLEXT ecosystem
components, providing consistent monitoring patterns, telemetry collection,
and business intelligence across the entire distributed data integration platform.

Public API:
    - Domain Entities: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck,
      FlextLogEntry
    - Simple API: flext_create_metric(), flext_create_trace(), flext_create_alert()
    - Factory Patterns: FlextObservabilityMasterFactory for entity creation
    - Monitoring Automation: @flext_monitor_function decorator for automatic monitoring
    - Service Orchestration: FlextObservabilityMonitor for service coordination
    - Application Services: FlextMetricsService, FlextTracingService, FlextAlertService

Architecture:
    Clean Architecture implementation with clear layer separation:
    - Domain Layer: Entities with business logic and validation
    - Application Layer: Services coordinating business workflows
    - Interface Adapters: APIs, factories, and external integrations
    - Infrastructure Layer: External system integration and data persistence

Integration:
    - Built on flext-core foundation patterns (FlextEntity, FlextResult, FlextContainer)
    - Compatible with OpenTelemetry, Prometheus, Jaeger, and ELK stack
    - Supports all 33 FLEXT ecosystem projects with consistent patterns
    - Enterprise-grade scalability and performance for production deployments

Example:
    Quick start with simple API for immediate observability:

    from flext_observability import (
        flext_create_metric, flext_create_trace, flext_monitor_function
    )

    # Create business metrics
    metric_result = flext_create_metric("api_requests", 42, "count")

    # Distributed tracing
    trace_result = flext_create_trace("user_login", "auth-service")

    # Automatic function monitoring
    @flext_monitor_function("order_processing")
    def process_order(order_data):
        return {"status": "processed"}

Version: 0.9.0
Status: Production Ready
License: MIT

"""

from __future__ import annotations

__version__ = "0.9.0"

# Core entities and types
# Import get_logger from flext_core for convenience
from flext_core import get_logger

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,
    flext_health_check,
    flext_trace,
)

# Factory patterns
from flext_observability.factory import (
    FlextObservabilityMasterFactory,
    alert,
    create_simplified_observability_platform,
    get_global_factory,
    health_check,
    log,
    metric,
    reset_global_factory,
    trace,
)

# Monitor patterns
from flext_observability.flext_monitor import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Simple API
from flext_observability.flext_simple import (
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

# Platform
from flext_observability.obs_platform import FlextObservabilityPlatformV2

# Services
from flext_observability.services import (
    FlextAlertService,
    FlextHealthService,
    FlextLoggingService,
    FlextMetricsService,
    FlextTracingService,
)


# Health check function
def flext_health_status() -> dict[str, str]:
    """Get basic health status."""
    return {
        "status": "healthy",
        "service": "flext-observability",
        "version": "0.9.0",
    }


__all__ = [
    # Entities
    "FlextAlert",
    # Services
    "FlextAlertService",
    "FlextHealthCheck",
    "FlextHealthService",
    "FlextLogEntry",
    "FlextLoggingService",
    "FlextMetric",
    "FlextMetricsService",
    # Factory
    "FlextObservabilityMasterFactory",
    # Monitor
    "FlextObservabilityMonitor",
    # Platform
    "FlextObservabilityPlatformV2",
    "FlextTrace",
    "FlextTracingService",
    # Global functions
    "alert",
    "create_simplified_observability_platform",
    # Entity factory functions
    "flext_alert",
    # Simple API
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",
    # Utils
    "flext_health_status",
    "flext_monitor_function",
    "flext_trace",
    "get_global_factory",
    "get_logger",
    "health_check",
    "log",
    "metric",
    "reset_global_factory",
    "trace",
]
