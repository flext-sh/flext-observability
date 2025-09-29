#!/usr/bin/env python3  # pragma: no cover
"""Comprehensive functional examples for flext-observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This file demonstrates real-world usage patterns and functional scenarios
for the flext-observability module, showcasing 100% functional integration.
"""

from __future__ import annotations

import time

from flext_core import FlextContainer
from flext_observability import (
    FlextObservabilityMasterFactory,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
    get_global_factory,
    reset_global_factory,
)


def demonstrate_simple_api() -> None:
    """Demonstrate the simple API for creating observability entities."""
    # Create metrics
    metric_result = flext_create_metric("api_requests", 150.0, "count")
    if metric_result.is_success:
        pass

    # Create traces
    trace_result = flext_create_trace("user_registration", "auth-service")
    if trace_result.is_success:
        pass

    # Create alerts
    alert_result = flext_create_alert(
        "High CPU usage detected",
        "monitoring",
        "warning",
    )
    if alert_result.is_success:
        pass

    # Create health checks
    health_result = flext_create_health_check("database", "healthy")
    if health_result.is_success:
        pass

    # Create log entries
    log_result = flext_create_log_entry(
        "User authentication successful",
        "auth-service",
        "INFO",
    )
    if log_result.is_success:
        pass


def demonstrate_factory_pattern() -> None:
    """Demonstrate the factory pattern for advanced usage."""
    # Create factory with container
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)

    # Create entities via factory
    metric_result = factory.create_metric("response_time", 45.2, "milliseconds")
    if metric_result.is_success:
        pass

    trace_result = factory.create_trace("payment_processing", "payment-service")
    if trace_result.is_success:
        pass


def monitored_function(data: str) -> str:
    """Example function with automatic monitoring."""
    time.sleep(0.1)  # Simulate processing
    return f"Processed: {data}"


def demonstrate_monitoring() -> None:
    """Demonstrate automatic function monitoring."""
    monitored_function("sample data")


def demonstrate_validation() -> None:
    """Demonstrate entity validation."""
    # Valid metric
    metric_result = flext_create_metric("valid_metric", 100.0, "count")
    if metric_result.is_success:
        metric_result.unwrap().validate_business_rules()

    # Invalid metric (negative value should be caught by pydantic or business rules)
    try:
        invalid_metric_result = flext_create_metric("invalid_metric", -10.0, "count")
        if invalid_metric_result.is_success:
            invalid_metric_result.unwrap().validate_business_rules()
    except Exception as e:
        print(f"Validation error (expected): {e}")


def demonstrate_health_monitoring() -> None:
    """Demonstrate health monitoring scenario."""
    services = ["database", "cache", "message-queue", "auth-service"]
    statuses = ["healthy", "healthy", "degraded", "healthy"]

    for service, status in zip(services, statuses, strict=False):
        health_result = flext_create_health_check(service, status)
        if health_result.is_success:
            pass


def demonstrate_alerting_scenario() -> None:
    """Demonstrate alerting in different scenarios."""
    alert_scenarios = [
        ("info", "System started successfully", "system"),
        ("warning", "High memory usage: 85%", "monitoring"),
        ("error", "Database connection failed", "database"),
        ("critical", "Payment service unavailable", "payment"),
    ]

    for level, message, service in alert_scenarios:
        alert_result = flext_create_alert(message, service, level)
        if alert_result.is_success:
            icons = {
                "info": "[INFO]",
                "warning": "[WARN]",
                "error": "[ERROR]",
                "critical": "[CRIT]",
            }
            icons.get(level, "[UNKNOWN]")


def demonstrate_global_factory() -> None:
    """Demonstrate global factory usage."""
    # Reset to ensure clean state
    reset_global_factory()

    # Get global factory
    factory = get_global_factory()

    # Use global factory
    metric_result = factory.create_metric("global_metric", 42.0, "count")
    if metric_result.is_success:
        pass


def main() -> None:
    """Run all functional examples."""
    demonstrate_simple_api()
    demonstrate_factory_pattern()
    demonstrate_monitoring()
    demonstrate_validation()
    demonstrate_health_monitoring()
    demonstrate_alerting_scenario()
    demonstrate_global_factory()


if __name__ == "__main__":
    main()
