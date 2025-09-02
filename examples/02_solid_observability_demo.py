#!/usr/bin/env python3
"""SOLID Observability Demo - Real functionality demonstration.

This example demonstrates the real functionality implemented in flext-observability
following SOLID principles with metrics, tracing, health monitoring,
and function monitoring capabilities.
"""

import time

from flext_core import FlextContainer, FlextResult

from flext_observability import (
    FlextObservabilityMasterFactory,
    flext_create_alert,
    flext_create_health_check,
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    get_global_factory,
)
from flext_observability.models import (
    FlextAlert,
    FlextHealthCheck,
    FlextMetric,
    FlextTrace,
)


@flext_monitor_function(metric_name="database_operation")
def database_query(query: str) -> dict[str, object]:
    """Simulate a database operation with monitoring."""
    time.sleep(0.05)  # Simulate database latency
    return {"query": query, "rows": 42, "execution_time": 0.05}


@flext_monitor_function(metric_name="api_request")
def process_api_request(endpoint: str) -> dict[str, object]:
    """Simulate API request processing with monitoring."""
    time.sleep(0.1)  # Simulate processing time
    return {"endpoint": endpoint, "status": "success", "response_time": 0.1}


def demonstrate_solid_design() -> None:
    """Demonstrate SOLID design principles in action."""
    # Single Responsibility: Each entity has one clear purpose
    metric_result = flext_create_metric("cpu_usage", 75.5, "percent")
    trace_result = flext_create_trace("user_login", "auth-service")
    alert_result = flext_create_alert("High CPU usage", "monitoring", "warning")
    health_result = flext_create_health_check("database", "healthy")

    # Open/Closed: Extensible without modification
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)
    factory.create_metric("custom_metric", 100.0, "units")

    # Liskov Substitution: All entities implement the same base interface
    results: list[FlextResult[object]] = [
        metric_result,
        trace_result,
        alert_result,
        health_result,
    ]
    entities: list[FlextMetric | FlextTrace | FlextAlert | FlextHealthCheck] = [
        result.data for result in results if result.success and result.data
    ]
    for entity in entities:
        if hasattr(entity, "validate_business_rules"):
            entity.validate_business_rules()

    # Interface Segregation: Clean interfaces for different concerns

    # Dependency Inversion: High-level modules depend on abstractions


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
        result = flext_create_metric(name, value, unit)
        if result.success:
            pass


def demonstrate_distributed_tracing() -> None:
    """Demonstrate distributed tracing across services."""
    # Simulate a distributed request flow
    services = [
        ("api_gateway", "request_routing"),
        ("auth_service", "user_authentication"),
        ("user_service", "profile_retrieval"),
        ("database", "user_query"),
        ("cache", "result_caching"),
    ]

    for service, operation in services:
        result = flext_create_trace(operation, service)
        if result.success:
            pass


def demonstrate_health_monitoring() -> None:
    """Demonstrate comprehensive health monitoring."""
    services_health = [
        ("api_gateway", "healthy"),
        ("auth_service", "healthy"),
        ("user_service", "healthy"),
        ("database", "degraded"),
        ("cache", "healthy"),
        ("message_queue", "healthy"),
    ]

    for service, status in services_health:
        result = flext_create_health_check(service, status)
        if result.success:
            pass


def demonstrate_alerting_system() -> None:
    """Demonstrate comprehensive alerting."""
    alerts = [
        ("info", "System maintenance scheduled", "system"),
        ("warning", "Database response time increased", "database"),
        ("error", "Failed to connect to cache", "cache"),
        ("critical", "API gateway not responding", "api_gateway"),
    ]

    for level, message, service in alerts:
        result = flext_create_alert(message, service, level)
        if result.success:
            icons = {
                "info": "[INFO]",
                "warning": "[WARN]",
                "error": "[ERROR]",
                "critical": "[CRIT]",
            }
            icons[level]


def demonstrate_function_monitoring() -> None:
    """Demonstrate automatic function monitoring."""
    # Execute monitored functions
    database_query("SELECT * FROM users WHERE active = true")

    process_api_request("/api/v1/users")


def demonstrate_factory_patterns() -> None:
    """Demonstrate factory pattern usage."""
    # Global factory
    global_factory = get_global_factory()
    global_factory.create_metric("global_metric", 42.0, "count")

    # Custom factory with DI container
    container = FlextContainer()
    custom_factory = FlextObservabilityMasterFactory(container)
    custom_factory.create_metric("custom_metric", 24.0, "count")


def demonstrate_validation() -> None:
    """Demonstrate entity validation."""
    # Create various entities and validate them
    entities_to_validate: list[
        FlextResult[FlextMetric]
        | FlextResult[FlextTrace]
        | FlextResult[FlextAlert]
        | FlextResult[FlextHealthCheck]
    ] = [
        flext_create_metric("valid_metric", 100.0, "count"),
        flext_create_trace("valid_operation", "valid_service"),
        flext_create_alert("Valid alert", "system", "info"),
        flext_create_health_check("service", "healthy"),
    ]

    for result in entities_to_validate:
        if result.success and result.data:
            result.data.validate_business_rules()
            type(result.data).__name__


def main() -> None:
    """Run the comprehensive SOLID observability demo."""
    try:
        demonstrate_solid_design()
        demonstrate_metrics_collection()
        demonstrate_distributed_tracing()
        demonstrate_health_monitoring()
        demonstrate_alerting_system()
        demonstrate_function_monitoring()
        demonstrate_factory_patterns()
        demonstrate_validation()

    except Exception:
        raise


if __name__ == "__main__":
    main()
