#!/usr/bin/env python3
"""Comprehensive functional examples for flext-observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This file demonstrates real-world usage patterns and functional scenarios
for the flext-observability module, showcasing 100% functional integration.
"""

from __future__ import annotations

import time
from datetime import datetime

from flext_core import FlextContainer

from flext_observability import (
    FlextObservabilityMasterFactory,
    flext_create_metric,
    flext_create_trace,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_monitor_function,
    get_global_factory,
    reset_global_factory,
)


def demonstrate_simple_api() -> None:
    """Demonstrate the simple API for creating observability entities."""
    print("🔍 Demonstrating Simple API")
    
    # Create metrics
    metric_result = flext_create_metric("api_requests", 150.0, "count")
    if metric_result.success:
        print(f"✅ Created metric: {metric_result.data.name} = {metric_result.data.value}")
    
    # Create traces
    trace_result = flext_create_trace("user_registration", "auth-service")
    if trace_result.success:
        print(f"✅ Created trace: {trace_result.data.operation_name} on {trace_result.data.service_name}")
    
    # Create alerts
    alert_result = flext_create_alert("High CPU usage detected", "monitoring", "warning")
    if alert_result.success:
        print(f"✅ Created alert: {alert_result.data.message} (level: {alert_result.data.level})")
    
    # Create health checks
    health_result = flext_create_health_check("database", "healthy")
    if health_result.success:
        print(f"✅ Created health check: {health_result.data.service_name} is {health_result.data.status}")
    
    # Create log entries
    log_result = flext_create_log_entry("User authentication successful", "auth-service", "INFO")
    if log_result.success:
        print(f"✅ Created log entry: {log_result.data.message}")


def demonstrate_factory_pattern() -> None:
    """Demonstrate the factory pattern for advanced usage."""
    print("\n🏭 Demonstrating Factory Pattern")
    
    # Create factory with container
    container = FlextContainer()
    factory = FlextObservabilityMasterFactory(container)
    
    # Create entities via factory
    metric_result = factory.create_metric("response_time", 45.2, "milliseconds")
    if metric_result.success:
        print(f"✅ Factory created metric: {metric_result.data.name}")
    
    trace_result = factory.create_trace("payment_processing", "payment-service")
    if trace_result.success:
        print(f"✅ Factory created trace: {trace_result.data.operation_name}")


@flext_monitor_function(metric_name="example_processing")
def monitored_function(data: str) -> str:
    """Example function with automatic monitoring."""
    time.sleep(0.1)  # Simulate processing
    return f"Processed: {data}"


def demonstrate_monitoring() -> None:
    """Demonstrate automatic function monitoring."""
    print("\n📊 Demonstrating Function Monitoring")
    
    result = monitored_function("sample data")
    print(f"✅ Monitored function result: {result}")


def demonstrate_validation() -> None:
    """Demonstrate entity validation."""
    print("\n✅ Demonstrating Entity Validation")
    
    # Valid metric
    metric_result = flext_create_metric("valid_metric", 100.0, "count")
    if metric_result.success:
        validation = metric_result.data.validate_business_rules()
        print(f"✅ Metric validation: {'passed' if validation.success else 'failed'}")
    
    # Invalid metric (negative value should be caught by pydantic or business rules)
    try:
        invalid_metric_result = flext_create_metric("invalid_metric", -10.0, "count")
        if invalid_metric_result.success:
            validation = invalid_metric_result.data.validate_business_rules()
            print(f"❌ Invalid metric validation: {'passed' if validation.success else 'failed'}")
    except Exception as e:
        print(f"✅ Caught validation error as expected: {type(e).__name__}")


def demonstrate_health_monitoring() -> None:
    """Demonstrate health monitoring scenario."""
    print("\n💚 Demonstrating Health Monitoring")
    
    services = ["database", "cache", "message-queue", "auth-service"]
    statuses = ["healthy", "healthy", "degraded", "healthy"]
    
    for service, status in zip(services, statuses):
        health_result = flext_create_health_check(service, status)
        if health_result.success:
            icon = "✅" if status == "healthy" else "⚠️" if status == "degraded" else "❌"
            print(f"{icon} {health_result.data.service_name}: {health_result.data.status}")


def demonstrate_alerting_scenario() -> None:
    """Demonstrate alerting in different scenarios."""
    print("\n🚨 Demonstrating Alerting Scenarios")
    
    alert_scenarios = [
        ("info", "System started successfully", "system"),
        ("warning", "High memory usage: 85%", "monitoring"),
        ("error", "Database connection failed", "database"),
        ("critical", "Payment service unavailable", "payment"),
    ]
    
    for level, message, service in alert_scenarios:
        alert_result = flext_create_alert(message, service, level)
        if alert_result.success:
            icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "critical": "🔥"}
            icon = icons.get(level, "❓")
            print(f"{icon} [{level.upper()}] {alert_result.data.message}")


def demonstrate_global_factory() -> None:
    """Demonstrate global factory usage."""
    print("\n🌍 Demonstrating Global Factory")
    
    # Reset to ensure clean state
    reset_global_factory()
    
    # Get global factory
    factory = get_global_factory()
    
    # Use global factory
    metric_result = factory.create_metric("global_metric", 42.0, "count")
    if metric_result.success:
        print(f"✅ Global factory created: {metric_result.data.name}")


def main() -> None:
    """Run all functional examples."""
    print("🚀 FLEXT Observability - Functional Examples")
    print("=" * 50)
    
    try:
        demonstrate_simple_api()
        demonstrate_factory_pattern()
        demonstrate_monitoring()
        demonstrate_validation()
        demonstrate_health_monitoring()
        demonstrate_alerting_scenario()
        demonstrate_global_factory()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        raise


if __name__ == "__main__":
    main()