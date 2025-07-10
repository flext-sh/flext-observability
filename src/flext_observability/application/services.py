"""Application services for observability - orchestrate use cases."""

from __future__ import annotations

from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from uuid import uuid4

from flext_core.config import injectable
from flext_core.domain.types import ServiceResult
from flext_core.domain.types import TraceStatus
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.entities import LogEntry
from flext_observability.domain.entities import Metric
from flext_observability.domain.entities import Trace
from flext_observability.domain.events import AlertTriggered
from flext_observability.domain.events import HealthCheckCompleted
from flext_observability.domain.events import LogEntryCreated
from flext_observability.domain.events import MetricCollected
from flext_observability.domain.events import TraceCompleted
from flext_observability.domain.events import TraceStarted
from flext_observability.domain.specifications import ActiveAlertSpec
from flext_observability.domain.specifications import MetricValidationSpec
from flext_observability.domain.value_objects import ComponentName
from flext_observability.domain.value_objects import Duration
from flext_observability.domain.value_objects import MetricValue
from flext_observability.domain.value_objects import TraceId

if TYPE_CHECKING:
    from flext_core.domain.types import AlertSeverity
    from flext_core.domain.types import LogLevel
    from flext_core.domain.types import MetricType
    from flext_observability.domain.entities import Alert
    from flext_observability.domain.services import AlertingService
    from flext_observability.domain.services import HealthAnalysisService
    from flext_observability.domain.services import LogAnalysisService
    from flext_observability.domain.services import MetricsAnalysisService
    from flext_observability.domain.services import TraceAnalysisService
    from flext_observability.infrastructure.persistence.base import AlertRepository
    from flext_observability.infrastructure.persistence.base import EventBus
    from flext_observability.infrastructure.persistence.base import HealthRepository
    from flext_observability.infrastructure.persistence.base import LogRepository
    from flext_observability.infrastructure.persistence.base import MetricsRepository
    from flext_observability.infrastructure.persistence.base import TraceRepository


@injectable()
class MetricsService:
    """Application service for metrics collection and analysis."""

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_analysis_service: MetricsAnalysisService,
        event_bus: EventBus,
    ) -> None:
        self.metrics_repository = metrics_repository
        self.metrics_analysis_service = metrics_analysis_service
        self.event_bus = event_bus

    async def collect_metric(
        self,
        name: str,
        value: float,
        unit: str,
        metric_type: MetricType,
        component_name: str,
        component_namespace: str = "default",
        tags: dict[str, str] | None = None,
    ) -> ServiceResult[Metric]:
        """Collect a metric value."""
        try:
            # Create domain objects
            metric_value = MetricValue(value=value, unit=unit)
            component = ComponentName(name=component_name, namespace=component_namespace)

            # Create metric entity
            metric = Metric(
                name=name,
                metric_type=metric_type,
                value=metric_value,
                component=component,
                tags=tags or {},
            )

            # Validate metric
            validation_spec = MetricValidationSpec()
            if not validation_spec.is_satisfied_by(metric):
                return ServiceResult.fail("Invalid metric data")

            # Store metric
            stored_metric = await self.metrics_repository.save(metric)

            # Analyze trends
            self.metrics_analysis_service.analyze_trend(stored_metric)

            # Publish event
            event = MetricCollected(metric=stored_metric)
            await self.event_bus.publish(event)

            return ServiceResult.ok(stored_metric)

        except Exception as e:
            return ServiceResult.fail(f"Failed to collect metric: {e}")

    async def get_metrics(
        self,
        component_name: str | None = None,
        metric_type: MetricType | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[Metric]]:
        """Get metrics with optional filtering."""
        try:
            metrics = await self.metrics_repository.find_by_criteria(
                component_name=component_name,
                metric_type=metric_type,
                start_time=start_time,
                end_time=end_time,
                limit=limit,
            )

            return ServiceResult.ok(metrics)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get metrics: {e}")

    async def get_metric_trends(self, metric_name: str) -> ServiceResult[dict[str, Any]]:
        """Get trend analysis for a metric."""
        try:
            # Get recent metrics
            metrics = await self.metrics_repository.find_by_name(metric_name, limit=100)

            if not metrics:
                return ServiceResult.ok({"trend": "no_data", "points": 0})

            # Analyze trends using the latest metric
            latest_metric = metrics[0]
            return self.metrics_analysis_service.analyze_trend(latest_metric)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get metric trends: {e}")


@injectable()
class AlertService:
    """Application service for alert management."""

    def __init__(
        self,
        alert_repository: AlertRepository,
        alerting_service: AlertingService,
        event_bus: EventBus,
    ) -> None:
        self.alert_repository = alert_repository
        self.alerting_service = alerting_service
        self.event_bus = event_bus

    async def evaluate_metric_for_alerts(self, metric: Metric) -> ServiceResult[Alert | None]:
        """Evaluate a metric against alert rules."""
        try:
            # Use domain service to evaluate
            alert_result = self.alerting_service.evaluate_metric(metric)

            if not alert_result.success:
                return alert_result

            alert = alert_result.data
            if alert is None:
                return ServiceResult.ok(None)

            # Store alert
            stored_alert = await self.alert_repository.save(alert)

            # Publish event
            event = AlertTriggered(alert=stored_alert)
            await self.event_bus.publish(event)

            return ServiceResult.ok(stored_alert)

        except Exception as e:
            return ServiceResult.fail(f"Failed to evaluate metric for alerts: {e}")

    async def acknowledge_alert(self, alert_id: str, user: str) -> ServiceResult[Alert]:
        """Acknowledge an alert."""
        try:
            # Get alert
            alert = await self.alert_repository.get_by_id(alert_id)
            if not alert:
                return ServiceResult.fail("Alert not found")

            # Acknowledge alert
            alert.acknowledge(user)

            # Save changes
            updated_alert = await self.alert_repository.save(alert)

            return ServiceResult.ok(updated_alert)

        except Exception as e:
            return ServiceResult.fail(f"Failed to acknowledge alert: {e}")

    async def resolve_alert(self, alert_id: str) -> ServiceResult[Alert]:
        """Resolve an alert."""
        try:
            # Get alert
            alert = await self.alert_repository.get_by_id(alert_id)
            if not alert:
                return ServiceResult.fail("Alert not found")

            # Resolve alert
            alert.resolve()

            # Save changes
            updated_alert = await self.alert_repository.save(alert)

            return ServiceResult.ok(updated_alert)

        except Exception as e:
            return ServiceResult.fail(f"Failed to resolve alert: {e}")

    async def get_active_alerts(
        self,
        severity: AlertSeverity | None = None,
        component_name: str | None = None,
        limit: int = 50,
    ) -> ServiceResult[list[Alert]]:
        """Get active alerts."""
        try:
            alerts = await self.alert_repository.find_active(
                severity=severity,
                component_name=component_name,
                limit=limit,
            )

            # Filter using specification
            active_spec = ActiveAlertSpec()
            active_alerts = [alert for alert in alerts if active_spec.is_satisfied_by(alert)]

            return ServiceResult.ok(active_alerts)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get active alerts: {e}")


@injectable()
class HealthMonitoringService:
    """Application service for health monitoring."""

    def __init__(
        self,
        health_repository: HealthRepository,
        health_analysis_service: HealthAnalysisService,
        event_bus: EventBus,
    ) -> None:
        self.health_repository = health_repository
        self.health_analysis_service = health_analysis_service
        self.event_bus = event_bus

    async def perform_health_check(
        self,
        component_name: str,
        component_namespace: str = "default",
        endpoint: str | None = None,
        timeout_ms: int = 5000,
    ) -> ServiceResult[HealthCheck]:
        """Perform a health check for a component."""
        try:
            start_time = datetime.now(UTC)

            # Create component name
            ComponentName(name=component_name, namespace=component_namespace)

            # Perform actual health check (simplified)
            # In a real implementation, this would call the actual health endpoint
            error = None

            # Calculate duration
            end_time = datetime.now(UTC)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            Duration(milliseconds=duration_ms)

            # Create health check entity
            health_check = HealthCheck(
                name=component_name,
                check_type="api",
                endpoint=endpoint,
                error_message=error,
            )

            # Store health check
            stored_health_check = await self.health_repository.save(health_check)

            # Update component health status
            status_changed_result = self.health_analysis_service.update_component_health(
                stored_health_check,
            )

            # Publish event
            event = HealthCheckCompleted(health_check=stored_health_check)
            await self.event_bus.publish(event)

            # Publish status change event if needed
            if status_changed_result.success and status_changed_result.data:
                # Would publish ComponentHealthChanged event
                pass

            return ServiceResult.ok(stored_health_check)

        except Exception as e:
            return ServiceResult.fail(f"Failed to perform health check: {e}")

    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health."""
        try:
            # Get latest health checks for all components
            health_checks = await self.health_repository.get_latest_by_component()

            # Update health analysis service with latest data
            for health_check in health_checks:
                self.health_analysis_service.update_component_health(health_check)

            # Get system health
            return self.health_analysis_service.get_system_health()

        except Exception as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")

    async def get_component_health(
        self,
        component_name: str,
        component_namespace: str = "default",
    ) -> ServiceResult[HealthCheck | None]:
        """Get health status for a specific component."""
        try:
            component = ComponentName(name=component_name, namespace=component_namespace)
            health_check = await self.health_repository.get_latest_by_component(component)

            return ServiceResult.ok(health_check)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get component health: {e}")


@injectable()
class LoggingService:
    """Application service for structured logging."""

    def __init__(
        self,
        log_repository: LogRepository,
        log_analysis_service: LogAnalysisService,
        event_bus: EventBus,
    ) -> None:
        self.log_repository = log_repository
        self.log_analysis_service = log_analysis_service
        self.event_bus = event_bus

    async def create_log_entry(
        self,
        level: LogLevel,
        message: str,
        component_name: str,
        component_namespace: str = "default",
        correlation_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        fields: dict[str, Any] | None = None,
        exception: str | None = None,
    ) -> ServiceResult[LogEntry]:
        """Create a structured log entry."""
        try:
            # Create component name
            ComponentName(name=component_name, namespace=component_namespace)

            # Create log entry entity
            log_entry = LogEntry(
                level=level,
                message=message,
                logger_name=component_name,
                correlation_id=correlation_id,
                extra=fields or {},
            )

            # Store log entry
            stored_log_entry = await self.log_repository.save(log_entry)

            # Analyze log entry
            self.log_analysis_service.analyze_log_entry(stored_log_entry)

            # Publish event
            event = LogEntryCreated(log_entry=stored_log_entry)
            await self.event_bus.publish(event)

            return ServiceResult.ok(stored_log_entry)

        except Exception as e:
            return ServiceResult.fail(f"Failed to create log entry: {e}")

    async def get_logs(
        self,
        level: LogLevel | None = None,
        component_name: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        search: str | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[LogEntry]]:
        """Get log entries with optional filtering."""
        try:
            logs = await self.log_repository.find_by_criteria(
                level=level,
                component_name=component_name,
                start_time=start_time,
                end_time=end_time,
                search=search,
                limit=limit,
            )

            return ServiceResult.ok(logs)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get logs: {e}")

    async def get_error_patterns(self) -> ServiceResult[dict[str, int]]:
        """Get detected error patterns."""
        try:
            return self.log_analysis_service.get_error_patterns()

        except Exception as e:
            return ServiceResult.fail(f"Failed to get error patterns: {e}")


@injectable()
class TracingService:
    """Application service for distributed tracing."""

    def __init__(
        self,
        trace_repository: TraceRepository,
        trace_analysis_service: TraceAnalysisService,
        event_bus: EventBus,
    ) -> None:
        self.trace_repository = trace_repository
        self.trace_analysis_service = trace_analysis_service
        self.event_bus = event_bus

    async def start_trace(
        self,
        operation_name: str,
        component_name: str,
        component_namespace: str = "default",
        trace_id: str | None = None,
        span_id: str | None = None,
        parent_span_id: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> ServiceResult[Trace]:
        """Start a new trace."""
        try:
            # Create component name
            ComponentName(name=component_name, namespace=component_namespace)

            # Create trace identifier
            trace_identifier = TraceId(
                trace_id=trace_id or str(uuid4()).replace("-", ""),
                span_id=span_id or str(uuid4()).replace("-", "")[:16],
            )

            # Create trace entity
            trace = Trace(
                trace_id=trace_identifier,
                span_id=str(uuid4()),
                operation_name=operation_name,
                service_name=component_name,
                trace_status=TraceStatus.STARTED,
                parent_span_id=parent_span_id,
                trace_tags=tags or {},
            )

            # Start the trace
            trace.start()

            # Store trace
            stored_trace = await self.trace_repository.save(trace)

            # Publish event
            event = TraceStarted(trace=stored_trace)
            await self.event_bus.publish(event)

            return ServiceResult.ok(stored_trace)

        except Exception as e:
            return ServiceResult.fail(f"Failed to start trace: {e}")

    async def complete_trace(
        self,
        trace_id: str,
        success: bool = True,
        error: str | None = None,
    ) -> ServiceResult[Trace]:
        """Complete a trace."""
        try:
            # Get trace
            trace = await self.trace_repository.get_by_trace_id(trace_id)
            if not trace:
                return ServiceResult.fail("Trace not found")

            # Complete or fail the trace
            if success:
                trace.complete()
            else:
                trace.fail(error or "Unknown error")

            # Store updated trace
            updated_trace = await self.trace_repository.save(trace)

            # Analyze trace
            self.trace_analysis_service.analyze_trace(updated_trace)

            # Publish event
            event = TraceCompleted(trace=updated_trace)
            await self.event_bus.publish(event)

            return ServiceResult.ok(updated_trace)

        except Exception as e:
            return ServiceResult.fail(f"Failed to complete trace: {e}")

    async def get_traces(
        self,
        operation_name: str | None = None,
        component_name: str | None = None,
        status: TraceStatus | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[Trace]]:
        """Get traces with optional filtering."""
        try:
            traces = await self.trace_repository.find_by_criteria(
                operation_name=operation_name,
                component_name=component_name,
                status=status,
                start_time=start_time,
                end_time=end_time,
                limit=limit,
            )

            return ServiceResult.ok(traces)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get traces: {e}")

    async def get_operation_stats(self, operation_name: str) -> ServiceResult[dict[str, Any]]:
        """Get statistics for an operation."""
        try:
            return self.trace_analysis_service.get_operation_stats(operation_name)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get operation stats: {e}")
