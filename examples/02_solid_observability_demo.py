"""SOLID Observability Demo - Real functionality demonstration.

This example demonstrates the real functionality implemented in flext-observability
following SOLID principles with metrics, tracing, health monitoring,
and function monitoring capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from collections.abc import Sequence

from flext_core import FlextContainer
from flext_observability import (
    FlextObservability,
    FlextObservabilityMasterFactory,
    c,
    t,
)

AlertLevel = c.Observability.AlertLevel
HealthStatus = c.Observability.HealthStatus

flext_alert = FlextObservability.flext_alert
flext_health_check = FlextObservability.flext_health_check
flext_metric = FlextObservability.flext_metric
flext_trace = FlextObservability.flext_trace


def database_query(query: str) -> t.ContainerMapping:
    """Simulate a database operation with monitoring."""
    time.sleep(0.05)
    return {"query": query, "rows": 42, "execution_time": 0.05}


def process_api_request(endpoint: str) -> t.ContainerMapping:
    """Simulate API request processing with monitoring."""
    time.sleep(0.1)
    return {"endpoint": endpoint, "status": "success", "response_time": 0.1}


def demonstrate_solid_design() -> None:
    """Demonstrate SOLID design principles in action."""
    metric_result = flext_metric("cpu_usage", 75.5, "percent")
    trace_result = flext_trace("user_login")
    alert_result = flext_alert("monitoring", "High CPU usage", AlertLevel.WARNING)
    health_result = flext_health_check("database", HealthStatus.HEALTHY)
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)
    factory.create_metric("custom_metric", 100.0, "units")
    results = [metric_result, trace_result, alert_result, health_result]
    for result in results:
        _ = hasattr(result, "is_success") and result.is_success


def demonstrate_metrics_collection() -> None:
    """Demonstrate comprehensive metrics collection."""
    metrics = [
        ("api_requests_total", 1500.0, "count"),
        ("response_time_avg", 85.2, "milliseconds"),
        ("memory_usage", 68.5, "percent"),
        ("disk_usage", 45.8, "percent"),
        ("active_connections", 127.0, "count"),
    ]
    for name, value, unit in metrics:
        flext_metric(name, value, unit)


def demonstrate_distributed_tracing() -> None:
    """Demonstrate distributed tracing across services."""
    services = [
        ("api_gateway", "request_routing"),
        ("auth_service", "user_authentication"),
        ("user_service", "profile_retrieval"),
        ("database", "user_query"),
        ("cache", "result_caching"),
    ]
    for _service, operation in services:
        flext_trace(operation)


def demonstrate_health_monitoring() -> None:
    """Demonstrate comprehensive health monitoring."""
    services_health: Sequence[tuple[str, HealthStatus]] = [
        ("database", HealthStatus.HEALTHY),
        ("cache", HealthStatus.HEALTHY),
        ("message_queue", HealthStatus.DEGRADED),
        ("auth_service", HealthStatus.HEALTHY),
    ]
    for service, status in services_health:
        flext_health_check(service, status)


def demonstrate_alerting_system() -> None:
    """Demonstrate comprehensive alerting."""
    alerts: Sequence[tuple[AlertLevel, str, str]] = [
        (AlertLevel.INFO, "System maintenance scheduled", "system"),
        (AlertLevel.WARNING, "Database response time increased", "database"),
        (AlertLevel.ERROR, "Failed to connect to cache", "cache"),
        (AlertLevel.CRITICAL, "API gateway not responding", "api_gateway"),
    ]
    for level, message, service in alerts:
        result = flext_alert(service, message, level)
        if result.is_success:
            icons = {
                "info": "[INFO]",
                "warning": "[WARN]",
                "error": "[ERROR]",
                "critical": "[CRIT]",
            }
            icons[level]


def demonstrate_function_monitoring() -> None:
    """Demonstrate automatic function monitoring."""
    database_query("SELECT * FROM users WHERE active = true")
    process_api_request("/api/v1/users")


def demonstrate_factory_patterns() -> None:
    """Demonstrate factory pattern usage."""
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)
    factory.create_metric("global_metric", 42.0, "count")
    custom_factory = FlextObservabilityMasterFactory(container)
    custom_factory.create_metric("custom_metric", 24.0, "count")


def demonstrate_validation() -> None:
    """Demonstrate entity validation."""
    metric_res = flext_metric("valid_metric", 100.0, "count")
    if metric_res.is_success:
        print(f"Validation successful for {type(metric_res.value).__name__}")
    trace_res = flext_trace("valid_operation")
    if trace_res.is_success:
        print(f"Validation successful for {type(trace_res.value).__name__}")
    alert_res = flext_alert("system", "Valid alert", AlertLevel.INFO)
    if alert_res.is_success:
        print(f"Validation successful for {type(alert_res.value).__name__}")
    health_res = flext_health_check("service", HealthStatus.HEALTHY)
    if health_res.is_success:
        print(f"Validation successful for {type(health_res.value).__name__}")


def main() -> None:
    """Run the comprehensive SOLID observability demo."""
    demonstrate_solid_design()
    demonstrate_metrics_collection()
    demonstrate_distributed_tracing()
    demonstrate_health_monitoring()
    demonstrate_alerting_system()
    demonstrate_function_monitoring()
    demonstrate_factory_patterns()
    demonstrate_validation()


if __name__ == "__main__":
    main()
