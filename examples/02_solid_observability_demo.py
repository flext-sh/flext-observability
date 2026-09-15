"""SOLID Observability Demo - Real functionality demonstration.

This example demonstrates the real functionality implemented in flext-observability
following SOLID principles with metrics, tracing, health monitoring,
and function monitoring capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time

from flext_cli import cli

from flext_observability import FlextObservability, c, t


class FlextObservabilitySolidDemo:
    """SOLID observability demo facade."""

    def __init__(self) -> None:
        """Initialize demo facade."""
        self._observability = FlextObservability

    def _emit(self, message: str) -> None:
        """Emit example output through the canonical CLI facade."""
        cli.print(message)

    def database_query(self, query: str) -> t.JsonMapping:
        """Simulate a database operation with monitoring."""
        time.sleep(0.05)
        return {"query": query, "rows": 42, "execution_time": 0.05}

    def process_api_request(self, endpoint: str) -> t.JsonMapping:
        """Simulate API request processing with monitoring."""
        time.sleep(0.1)
        return {"endpoint": endpoint, "status": "success", "response_time": 0.1}

    def demonstrate_solid_design(self) -> None:
        """Demonstrate SOLID design principles in action."""
        metric_result = self._observability.flext_metric("cpu_usage", 75.5, "percent")
        trace_result = self._observability.flext_trace("user_login")
        alert_result = self._observability.flext_alert(
            source="monitoring",
            title="High CPU usage",
            message="High CPU usage",
            severity=c.Observability.AlertLevel.WARNING,
        )
        health_result = self._observability.flext_health_check(
            "database", c.Observability.HealthStatus.HEALTHY
        )
        self._observability.flext_metric("custom_metric", 100.0, "units")
        results = [metric_result, trace_result, alert_result, health_result]
        for result in results:
            _ = hasattr(result, "success") and result.success

    def demonstrate_metrics_collection(self) -> None:
        """Demonstrate comprehensive metrics collection."""
        metrics = [
            ("api_requests_total", 1500.0, "count"),
            ("response_time_avg", 85.2, "milliseconds"),
            ("memory_usage", 68.5, "percent"),
            ("disk_usage", 45.8, "percent"),
            ("active_connections", 127.0, "count"),
        ]
        for name, value, unit in metrics:
            self._observability.flext_metric(name, value, unit)

    def demonstrate_distributed_tracing(self) -> None:
        """Demonstrate distributed tracing across services."""
        services = [
            ("api_gateway", "request_routing"),
            ("auth_service", "user_authentication"),
            ("user_service", "profile_retrieval"),
            ("database", "user_query"),
            ("cache", "result_caching"),
        ]
        for _service, operation in services:
            self._observability.flext_trace(operation)

    def demonstrate_health_monitoring(self) -> None:
        """Demonstrate comprehensive health monitoring."""
        services_health: t.SequenceOf[tuple[str, c.Observability.HealthStatus]] = [
            ("database", c.Observability.HealthStatus.HEALTHY),
            ("cache", c.Observability.HealthStatus.HEALTHY),
            ("message_queue", c.Observability.HealthStatus.DEGRADED),
            ("auth_service", c.Observability.HealthStatus.HEALTHY),
        ]
        for service, status in services_health:
            self._observability.flext_health_check(service, status)

    def demonstrate_alerting_system(self) -> None:
        """Demonstrate comprehensive alerting."""
        alerts: t.SequenceOf[tuple[c.Observability.AlertLevel, str, str]] = [
            (c.Observability.AlertLevel.INFO, "System maintenance scheduled", "system"),
            (
                c.Observability.AlertLevel.WARNING,
                "Database response time increased",
                "database",
            ),
            (c.Observability.AlertLevel.ERROR, "Failed to connect to cache", "cache"),
            (
                c.Observability.AlertLevel.CRITICAL,
                "API gateway not responding",
                "api_gateway",
            ),
        ]
        for level, message, service in alerts:
            result = self._observability.flext_alert(
                source=service, title=message, message=message, severity=level
            )
            if result.success:
                icons = {
                    "info": "[INFO]",
                    "warning": "[WARN]",
                    "error": "[ERROR]",
                    "critical": "[CRIT]",
                }
                icons[level]

    def demonstrate_function_monitoring(self) -> None:
        """Demonstrate automatic function monitoring."""
        self.database_query("SELECT * FROM users WHERE active = true")
        self.process_api_request("/api/v1/users")

    def demonstrate_factory_patterns(self) -> None:
        """Demonstrate factory pattern usage."""
        self._observability.flext_metric("global_metric", 42.0, "count")
        self._observability.flext_metric("custom_metric", 24.0, "count")

    def demonstrate_validation(self) -> None:
        """Demonstrate entity validation."""
        metric_res = self._observability.flext_metric("valid_metric", 100.0, "count")
        if metric_res.success:
            self._emit(f"Validation successful for {type(metric_res.value).__name__}")
        trace_res = self._observability.flext_trace("valid_operation")
        if trace_res.success:
            self._emit(f"Validation successful for {type(trace_res.value).__name__}")
        alert_res = self._observability.flext_alert(
            source="system",
            title="Valid alert",
            message="Valid alert",
            severity=c.Observability.AlertLevel.INFO,
        )
        if alert_res.success:
            self._emit(f"Validation successful for {type(alert_res.value).__name__}")
        health_res = self._observability.flext_health_check(
            "service", c.Observability.HealthStatus.HEALTHY
        )
        if health_res.success:
            self._emit(f"Validation successful for {type(health_res.value).__name__}")

    def run(self) -> None:
        """Run the comprehensive SOLID observability demo."""
        self.demonstrate_solid_design()
        self.demonstrate_metrics_collection()
        self.demonstrate_distributed_tracing()
        self.demonstrate_health_monitoring()
        self.demonstrate_alerting_system()
        self.demonstrate_function_monitoring()
        self.demonstrate_factory_patterns()
        self.demonstrate_validation()


def main() -> None:
    """Run the comprehensive SOLID observability demo."""
    FlextObservabilitySolidDemo().run()


if __name__ == "__main__":
    main()
