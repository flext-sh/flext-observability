"""Comprehensive functional examples for flext-observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This file demonstrates real-world usage patterns and functional scenarios
for the flext-observability module, showcasing 100% functional integration.
"""

from __future__ import annotations

import time

from flext_cli import cli

from flext_observability import FlextObservability, c, t


class FlextObservabilityFunctionalExamples:
    """Functional examples for flext-observability facade."""

    def __init__(self) -> None:
        """Initialize example facade."""
        self._observability = FlextObservability

    def _emit(self, message: str) -> None:
        """Emit example output through the canonical CLI facade."""
        cli.print(message)

    def demonstrate_simple_api(self) -> None:
        """Demonstrate the simple API for creating observability entities."""
        self._observability.flext_metric("api_requests", 150.0, "count")
        self._observability.flext_trace("user_registration")
        self._observability.flext_alert(
            source="monitoring",
            title="High CPU usage detected",
            message="High CPU usage detected",
            severity=c.Observability.AlertLevel.WARNING,
        )
        self._observability.flext_health_check(
            "database", c.Observability.HealthStatus.HEALTHY
        )
        self._observability.flext_log_entry(
            "User authentication successful",
            c.Observability.ErrorSeverity.INFO,
            "auth-service",
        )

    def demonstrate_factory_pattern(self) -> None:
        """Demonstrate direct facade usage for advanced flows."""
        self._observability.flext_metric("response_time", 45.2, "milliseconds")
        self._observability.flext_trace(
            "payment_processing", {"service": "payment-service"}
        )

    def monitored_function(self, data: str) -> str:
        """Demonstrate automatic monitoring."""
        time.sleep(0.1)
        return f"Processed: {data}"

    def demonstrate_monitoring(self) -> None:
        """Demonstrate automatic function monitoring."""
        self.monitored_function("sample data")

    def demonstrate_validation(self) -> None:
        """Demonstrate entity validation."""
        metric_result = self._observability.flext_metric("valid_metric", 100.0, "count")
        if metric_result.success:
            self._emit(f"Created metric: {metric_result.value}")
        invalid_metric_result = self._observability.flext_metric(
            "invalid_metric", -10.0, "count"
        )
        if invalid_metric_result.success:
            self._emit(f"Created invalid metric: {invalid_metric_result.value}")
        else:
            self._emit(f"Validation error (expected): {invalid_metric_result.error}")

    def demonstrate_health_monitoring(self) -> None:
        """Demonstrate health monitoring scenario."""
        services = ["database", "cache", "message-queue", "auth-service"]
        statuses: t.SequenceOf[c.Observability.HealthStatus] = [
            c.Observability.HealthStatus.HEALTHY,
            c.Observability.HealthStatus.HEALTHY,
            c.Observability.HealthStatus.DEGRADED,
            c.Observability.HealthStatus.HEALTHY,
        ]
        for service, status in zip(services, statuses, strict=False):
            self._observability.flext_health_check(service, status)

    def demonstrate_alerting_scenario(self) -> None:
        """Demonstrate alerting in different scenarios."""
        alert_scenarios: t.SequenceOf[tuple[c.Observability.AlertLevel, str, str]] = [
            (c.Observability.AlertLevel.INFO, "System started successfully", "system"),
            (
                c.Observability.AlertLevel.WARNING,
                "High memory usage: 85%",
                "monitoring",
            ),
            (
                c.Observability.AlertLevel.ERROR,
                "Database connection failed",
                "database",
            ),
            (
                c.Observability.AlertLevel.CRITICAL,
                "Payment service unavailable",
                "payment",
            ),
        ]
        for level, message, service in alert_scenarios:
            alert_result = self._observability.flext_alert(
                source=service, title=message, message=message, severity=level
            )
            if alert_result.success:
                icons = {
                    "info": "[INFO]",
                    "warning": "[WARN]",
                    "error": "[ERROR]",
                    "critical": "[CRIT]",
                }
                icons.get(level, "[UNKNOWN]")

    def demonstrate_global_factory(self) -> None:
        """Demonstrate repeated facade usage without factory indirection."""
        self._observability.flext_metric("global_metric", 42.0, "count")

    def run(self) -> None:
        """Run all functional examples."""
        self.demonstrate_simple_api()
        self.demonstrate_factory_pattern()
        self.demonstrate_monitoring()
        self.demonstrate_validation()
        self.demonstrate_health_monitoring()
        self.demonstrate_alerting_scenario()
        self.demonstrate_global_factory()


def main() -> None:
    """Entry point."""
    FlextObservabilityFunctionalExamples().run()


if __name__ == "__main__":
    main()
