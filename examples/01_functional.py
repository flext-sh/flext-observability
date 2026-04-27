"""Comprehensive functional examples for flext-observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This file demonstrates real-world usage patterns and functional scenarios
for the flext-observability module, showcasing 100% functional integration.
"""

from __future__ import annotations

import time
from collections.abc import (
    Sequence,
)

from flext_observability import (
    FlextObservability,
    c,
)

flext_alert = FlextObservability.flext_alert
flext_health_check = FlextObservability.flext_health_check
flext_log_entry = FlextObservability.flext_log_entry
flext_metric = FlextObservability.flext_metric
flext_trace = FlextObservability.flext_trace


def demonstrate_simple_api() -> None:
    """Demonstrate the simple API for creating observability entities."""
    flext_metric("api_requests", 150.0, "count")
    flext_trace("user_registration")
    flext_alert(
        source="monitoring",
        title="High CPU usage detected",
        message="High CPU usage detected",
        severity=c.Observability.AlertLevel.WARNING,
    )
    flext_health_check("database", c.Observability.HealthStatus.HEALTHY)
    flext_log_entry(
        "User authentication successful",
        c.Observability.ErrorSeverity.INFO,
        "auth-service",
    )


def demonstrate_factory_pattern() -> None:
    """Demonstrate direct facade usage for advanced flows."""
    flext_metric("response_time", 45.2, "milliseconds")
    flext_trace("payment_processing", {"service": "payment-service"})


def monitored_function(data: str) -> str:
    """Example function with automatic monitoring."""
    time.sleep(0.1)
    return f"Processed: {data}"


def demonstrate_monitoring() -> None:
    """Demonstrate automatic function monitoring."""
    monitored_function("sample data")


def demonstrate_validation() -> None:
    """Demonstrate entity validation."""
    metric_result = flext_metric("valid_metric", 100.0, "count")
    if metric_result.success:
        print(f"Created metric: {metric_result.value}")
    try:
        invalid_metric_result = flext_metric("invalid_metric", -10.0, "count")
        if invalid_metric_result.success:
            print(f"Created invalid metric: {invalid_metric_result.value}")
    except Exception as e:
        print(f"Validation error (expected): {e}")


def demonstrate_health_monitoring() -> None:
    """Demonstrate health monitoring scenario."""
    services = ["database", "cache", "message-queue", "auth-service"]
    statuses: Sequence[c.Observability.HealthStatus] = [
        c.Observability.HealthStatus.HEALTHY,
        c.Observability.HealthStatus.HEALTHY,
        c.Observability.HealthStatus.DEGRADED,
        c.Observability.HealthStatus.HEALTHY,
    ]
    for service, status in zip(services, statuses, strict=False):
        flext_health_check(service, status)


def demonstrate_alerting_scenario() -> None:
    """Demonstrate alerting in different scenarios."""
    alert_scenarios: Sequence[tuple[c.Observability.AlertLevel, str, str]] = [
        (c.Observability.AlertLevel.INFO, "System started successfully", "system"),
        (c.Observability.AlertLevel.WARNING, "High memory usage: 85%", "monitoring"),
        (c.Observability.AlertLevel.ERROR, "Database connection failed", "database"),
        (c.Observability.AlertLevel.CRITICAL, "Payment service unavailable", "payment"),
    ]
    for level, message, service in alert_scenarios:
        alert_result = flext_alert(
            source=service,
            title=message,
            message=message,
            severity=level,
        )
        if alert_result.success:
            icons = {
                "info": "[INFO]",
                "warning": "[WARN]",
                "error": "[ERROR]",
                "critical": "[CRIT]",
            }
            icons.get(level, "[UNKNOWN]")


def demonstrate_global_factory() -> None:
    """Demonstrate repeated facade usage without factory indirection."""
    flext_metric("global_metric", 42.0, "count")


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
