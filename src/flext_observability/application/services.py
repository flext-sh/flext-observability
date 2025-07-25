"""Application Services - Use cases using flext-core DI.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Clean Architecture - Application Layer
Following SOLID, KISS, DRY principles using flext-core DI container.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, FlextDomainService, FlextResult

if TYPE_CHECKING:
    from flext_observability.domain.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )


class FlextMetricsService(FlextDomainService):
    """Application service for metrics - Single Responsibility with DI."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize with DI container."""
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def record_metric(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Record a metric - Use case."""
        # Domain validation through DI
        domain_service_result = self.container.get("metrics_domain_service")
        if domain_service_result.is_success and domain_service_result.data:
            validation = domain_service_result.data.validate_metric(metric)
            if not validation.is_success:
                return FlextResult.fail(validation.error)

        # Repository through DI
        repository_result = self.container.get("metrics_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.save(metric)

        return FlextResult.fail("Metrics repository not configured")

    def get_metric(self, metric_id: str) -> FlextResult[FlextMetric]:
        """Get metric by ID - Use case."""
        repository_result = self.container.get("metrics_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.get_by_id(metric_id)

        return FlextResult.fail("Metrics repository not configured")


class FlextLoggingService(FlextDomainService):
    """Application service for logging - Single Responsibility with DI."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize with DI container."""
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def log_entry(self, entry: FlextLogEntry) -> FlextResult[FlextLogEntry]:
        """Log an entry - Use case."""
        repository_result = self.container.get("logging_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.save(entry)

        return FlextResult.fail("Logging repository not configured")

    def get_logs(self, level: str | None = None) -> FlextResult[list[FlextLogEntry]]:
        """Get logs by level - Use case."""
        repository_result = self.container.get("logging_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.find_by_level(level)

        return FlextResult.fail("Logging repository not configured")


class FlextTracingService(FlextDomainService):
    """Application service for tracing - Single Responsibility with DI."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize with DI container."""
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def start_trace(self, trace: FlextTrace) -> FlextResult[FlextTrace]:
        """Start a trace - Use case."""
        trace.status = "started"
        repository_result = self.container.get("tracing_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.save(trace)

        return FlextResult.fail("Tracing repository not configured")

    def complete_trace(
        self,
        trace_id: str,
        duration_ms: int,
    ) -> FlextResult[FlextTrace]:
        """Complete a trace - Use case."""
        repository_result = self.container.get("tracing_repository")
        if not repository_result.is_success or not repository_result.data:
            return FlextResult.fail("Tracing repository not configured")

        trace_result = repository_result.data.get_by_id(trace_id)

        if not trace_result.is_success:
            return trace_result

        trace = trace_result.data
        trace.duration_ms = duration_ms
        trace.status = "completed"

        return repository_result.data.save(trace)


class FlextAlertService(FlextDomainService):
    """Application service for alerts - Single Responsibility with DI."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize with DI container."""
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def create_alert(self, alert: FlextAlert) -> FlextResult[FlextAlert]:
        """Create an alert - Use case."""
        # Domain logic through DI
        domain_service_result = self.container.get("alert_domain_service")
        if domain_service_result.is_success and domain_service_result.data:
            should_escalate = domain_service_result.data.should_escalate(alert)
            if should_escalate.is_success and should_escalate.data:
                # Escalation logic here
                pass

        repository_result = self.container.get("alert_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.save(alert)

        return FlextResult.fail("Alert repository not configured")


class FlextHealthService(FlextDomainService):
    """Application service for health checks - Single Responsibility with DI."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize with DI container."""
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def check_health(self, component: str) -> FlextResult[FlextHealthCheck]:
        """Check component health - Use case."""
        repository_result = self.container.get("health_repository")
        if repository_result.is_success and repository_result.data:
            return repository_result.data.get_by_component(component)

        return FlextResult.fail("Health repository not configured")

    def get_overall_health(self) -> FlextResult[str]:
        """Get overall system health - Use case."""
        repository_result = self.container.get("health_repository")
        if not repository_result.is_success or not repository_result.data:
            return FlextResult.fail("Health repository not configured")

        all_checks = repository_result.data.get_all()

        if not all_checks.is_success:
            return FlextResult.fail(all_checks.error)

        domain_service_result = self.container.get("health_domain_service")
        if domain_service_result.is_success and domain_service_result.data:
            return domain_service_result.data.calculate_overall_health(all_checks.data)

        return FlextResult.ok("unknown")


# Backwards compatibility aliases
MetricsService = FlextMetricsService
LoggingService = FlextLoggingService
TracingService = FlextTracingService
AlertService = FlextAlertService
HealthService = FlextHealthService
