"""Application Services - Use cases using flext-core DI.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Application Layer
Following SOLID, KISS, DRY principles using flext-core DI container.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import ServiceResult, get_container

if TYPE_CHECKING:
    from flext_observability.domain.entities import (
        Alert,
        HealthCheck,
        LogEntry,
        Metric,
        Trace,
    )


class MetricsService:
    """Application service for metrics - Single Responsibility with DI."""

    def __init__(self) -> None:
        """Initialize with DI container."""
        self.container = get_container()

    def record_metric(self, metric: Metric) -> ServiceResult[Metric]:
        """Record a metric - Use case."""
        # Domain validation through DI
        domain_service = self.container.get("metrics_domain_service")
        validation = domain_service.validate_metric(metric)

        if not validation.is_success:
            return ServiceResult.error(validation.error)

        # Repository through DI
        repository = self.container.get("metrics_repository")
        return repository.save(metric)

    def get_metric(self, metric_id: str) -> ServiceResult[Metric]:
        """Get metric by ID - Use case."""
        repository = self.container.get("metrics_repository")
        return repository.get_by_id(metric_id)


class LoggingService:
    """Application service for logging - Single Responsibility with DI."""

    def __init__(self) -> None:
        """Initialize with DI container."""
        self.container = get_container()

    def log_entry(self, entry: LogEntry) -> ServiceResult[LogEntry]:
        """Log an entry - Use case."""
        repository = self.container.get("logging_repository")
        return repository.save(entry)

    def get_logs(self, level: str | None = None) -> ServiceResult[list[LogEntry]]:
        """Get logs by level - Use case."""
        repository = self.container.get("logging_repository")
        return repository.find_by_level(level)


class TracingService:
    """Application service for tracing - Single Responsibility with DI."""

    def __init__(self) -> None:
        """Initialize with DI container."""
        self.container = get_container()

    def start_trace(self, trace: Trace) -> ServiceResult[Trace]:
        """Start a trace - Use case."""
        trace.status = "started"
        repository = self.container.get("tracing_repository")
        return repository.save(trace)

    def complete_trace(self, trace_id: str, duration_ms: int) -> ServiceResult[Trace]:
        """Complete a trace - Use case."""
        repository = self.container.get("tracing_repository")
        trace_result = repository.get_by_id(trace_id)

        if not trace_result.is_success:
            return trace_result

        trace = trace_result.data
        trace.duration_ms = duration_ms
        trace.status = "completed"

        return repository.save(trace)


class AlertService:
    """Application service for alerts - Single Responsibility with DI."""

    def __init__(self) -> None:
        """Initialize with DI container."""
        self.container = get_container()

    def create_alert(self, alert: Alert) -> ServiceResult[Alert]:
        """Create an alert - Use case."""
        # Domain logic through DI
        domain_service = self.container.get("alert_domain_service")
        should_escalate = domain_service.should_escalate(alert)

        if should_escalate.is_success and should_escalate.data:
            # Escalation logic here
            pass

        repository = self.container.get("alert_repository")
        return repository.save(alert)


class HealthService:
    """Application service for health checks - Single Responsibility with DI."""

    def __init__(self) -> None:
        """Initialize with DI container."""
        self.container = get_container()

    def check_health(self, component: str) -> ServiceResult[HealthCheck]:
        """Check component health - Use case."""
        repository = self.container.get("health_repository")
        return repository.get_by_component(component)

    def get_overall_health(self) -> ServiceResult[str]:
        """Get overall system health - Use case."""
        repository = self.container.get("health_repository")
        all_checks = repository.get_all()

        if not all_checks.is_success:
            return ServiceResult.error(all_checks.error)

        domain_service = self.container.get("health_domain_service")
        return domain_service.calculate_overall_health(all_checks.data)
