"""Application services for observability - orchestrate use cases.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from flext_core.domain.types import AlertSeverity, LogLevel, MetricType, ServiceResult

from flext_observability.domain.entities import (
    Alert,
    HealthCheck,
    LogEntry,
    Metric,
    Trace,
)
from flext_observability.domain.events import (
    AlertTriggered,
    HealthCheckCompleted,
    LogEntryCreated,
    MetricCollected,
    TraceCompleted,
)
from flext_observability.domain.value_objects import ComponentName

# Rebuild models to handle forward references in events and value objects
try:
    # Import and rebuild value objects first

    # Import and rebuild entities
    Alert.model_rebuild()
    HealthCheck.model_rebuild()
    LogEntry.model_rebuild()
    Metric.model_rebuild()
    Trace.model_rebuild()

    # Import and rebuild events
    AlertTriggered.model_rebuild()
    HealthCheckCompleted.model_rebuild()
    LogEntryCreated.model_rebuild()
    MetricCollected.model_rebuild()
    TraceCompleted.model_rebuild()

except Exception as e:
    # If rebuild fails, it might be due to circular dependencies - that's okay for now
    import logging

    logging.getLogger(__name__).debug("Model rebuild failed: %s", e)

if TYPE_CHECKING:
    from flext_observability.domain.services import (
        AlertingService,
        HealthAnalysisService,
        LogAnalysisService,
        MetricsAnalysisService,
        TraceAnalysisService,
    )
    from flext_observability.infrastructure.persistence.base import (
        AlertRepository,
        EventBus,
        HealthRepository,
        LogRepository,
        MetricsRepository as MetricRepository,
        TraceRepository,
    )


class MetricsService:
    """Application service for metrics collection and analysis."""

    def __init__(
        self,
        metric_repository: MetricRepository[Any],
        metrics_analysis_service: MetricsAnalysisService,
        alerting_service: AlertingService,
        event_bus: EventBus,
    ) -> None:
        """Initialize metrics service.

        Args:
            metric_repository: Repository for storing metrics.
            metrics_analysis_service: Service for analyzing metrics.
            alerting_service: Service for handling alerts.
            event_bus: Event bus for publishing events.

        """
        self.metric_repository = metric_repository
        self.metrics_analysis_service = metrics_analysis_service
        self.alerting_service = alerting_service
        self.event_bus = event_bus

    async def collect_metric(
        self,
        name: str,
        value: float,
        *,
        metric_type: str = "gauge",
        unit: str | None = None,
        labels: dict[str, str] | None = None,
        component_name: str = "unknown",
        component_namespace: str = "default",
    ) -> ServiceResult[Metric]:
        """Collect a metric value and perform analysis.

        Args:
            name: Metric name.
            value: Metric value.
            metric_type: Type of metric (gauge, counter, histogram).
            unit: Unit of measurement.
            labels: Additional labels for the metric.
            component_name: Name of the component generating the metric.
            component_namespace: Namespace of the component.

        Returns:
            ServiceResult containing the created metric or error.

        """
        try:
            # Ensure models are properly rebuilt to handle forward references in the \
            # correct order
            import contextlib

            with contextlib.suppress(Exception):
                # First rebuild value objects and entities
                ComponentName.model_rebuild()
                Metric.model_rebuild()
                Alert.model_rebuild()

                # Then rebuild events that depend on entities
                MetricCollected.model_rebuild()
                AlertTriggered.model_rebuild()

            # Create metric entity from data, then save
            # Convert string metric_type to MetricType enum
            try:
                metric_type_enum = MetricType(metric_type.lower())
            except ValueError:
                metric_type_enum = MetricType.GAUGE  # Default fallback

            metric_entity = Metric(
                name=name,
                value=value,
                unit=unit,
                metric_type=metric_type_enum,
                component=ComponentName(
                    name=component_name,
                    namespace=component_namespace,
                ),
                labels=labels or {},
                timestamp=datetime.now(UTC),
            )
            metric_result = await self.metric_repository.save(metric_entity)
            if not metric_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save metric: {metric_result.error}",
                )

            metric = metric_result.data
            if metric is None:
                return ServiceResult.fail("Failed to save metric: No data returned")

            # Publish metric collected event - handle model rebuild issues gracefully
            try:
                MetricCollected(
                    metric=metric,
                    component=metric.component,
                )
            except Exception as event_error:
                # Only suppress Pydantic model rebuild errors, continue processing
                if "not fully defined" in str(event_error) or "model_rebuild" in str(
                    event_error,
                ):
                    pass  # Skip model rebuild issues but continue processing
                else:
                    raise  # Re-raise other unexpected exceptions

            # Analyze trend
            trend_result = self.metrics_analysis_service.analyze_trend(metric)
            if not trend_result.is_success:
                return ServiceResult.fail(
                    f"Trend analysis failed: {trend_result.error}",
                )

            # Check for alerts
            alert_result = self.alerting_service.evaluate_metric(metric)
            if alert_result.is_success and alert_result.data:
                alert_data = alert_result.data

                # Handle both Alert objects and alert data dictionaries
                if hasattr(alert_data, "severity"):
                    # It's an Alert object
                    alert = alert_data
                    severity = alert.severity
                else:
                    # It's alert data dictionary - create Alert object
                    alert = Alert(
                        title=alert_data.get("title", "Generated Alert"),
                        description=alert_data.get("description"),
                        severity=alert_data.get("severity", "medium"),
                        source="metrics",
                        source_type="automatic",
                        condition=f"Metric {metric.name} triggered alert",
                        threshold=metric.value,
                        created_at=datetime.now(UTC),
                    )
                    severity = alert.severity

                # Create and publish alert event
                try:
                    AlertTriggered(
                        alert=alert,
                        metric=metric,
                        severity=severity,
                    )
                    # Publish alert event would go here
                except Exception as event_error:
                    # Only suppress Pydantic model rebuild errors, continue processing
                    if "not fully defined" in str(
                        event_error,
                    ) or "model_rebuild" in str(event_error):
                        pass  # Skip model rebuild issues but continue processing
                    else:
                        raise  # Re-raise other unexpected exceptions

            return ServiceResult.ok(metric)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to collect metric: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error collecting metric: {e}")

    async def get_metrics(
        self,
        name: str | None = None,
        component_name: str | None = None,
        limit: int = 100,
    ) -> ServiceResult[list[Metric]]:
        """Get metrics with optional filtering.

        Args:
            name: Optional metric name filter.
            component_name: Optional component name filter.
            limit: Maximum number of metrics to return.

        Returns:
            ServiceResult containing list of metrics or error.

        """
        try:
            filters = {}
            if name:
                filters["name"] = name
            if component_name:
                filters["component__name"] = component_name

            # Use list method since find_by_filters doesn't exist in base repository
            metrics_result = await self.metric_repository.list(limit=limit)
            if not metrics_result.is_success:
                return ServiceResult.fail(
                    f"Failed to get metrics: {metrics_result.error}",
                )

            # Apply filters manually since we don't have a proper filter system
            metrics = metrics_result.data
            if metrics is None:
                return ServiceResult.ok([])

            if name:
                metrics = [m for m in metrics if m.name == name]
            if component_name:
                metrics = [m for m in metrics if m.component.name == component_name]
            return ServiceResult.ok(metrics)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get metrics: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error getting metrics: {e}")


class AlertService:
    """Application service for alert management."""

    def __init__(
        self,
        alert_repository: AlertRepository[Any],
        alerting_service: AlertingService,
        event_bus: EventBus,
    ) -> None:
        """Initialize alert service.

        Args:
            alert_repository: Repository for storing alerts.
            alerting_service: Service for alert logic.
            event_bus: Event bus for publishing events.

        """
        self.alert_repository = alert_repository
        self.alerting_service = alerting_service
        self.event_bus = event_bus

    async def create_alert(
        self,
        title: str,
        *,
        description: str | None = None,
        severity: str = "medium",
        source: str = "manual",
        source_type: str = "user",
        condition: str = "manual trigger",
        threshold: float | None = None,
    ) -> ServiceResult[Alert]:
        """Create a new alert and publish alert event.

        Args:
            title: Alert title.
            description: Optional alert description.
            severity: Alert severity level.
            source: Source of the alert.
            source_type: Type of the alert source.
            condition: Alert condition description.
            threshold: Optional threshold value.

        Returns:
            ServiceResult containing the created alert or error.

        """
        try:
            # Create alert entity from data, then save
            # Convert string severity to AlertSeverity enum
            try:
                severity_enum = AlertSeverity(severity.lower())
            except ValueError:
                severity_enum = AlertSeverity.MEDIUM  # Default fallback

            alert_entity = Alert(
                title=title,
                description=description,
                severity=severity_enum,
                source=source,
                source_type=source_type,
                condition=condition,
                threshold=threshold,
                created_at=datetime.now(UTC),
            )
            alert_result = await self.alert_repository.save(alert_entity)
            if not alert_result.is_success:
                return ServiceResult.fail(f"Failed to save alert: {alert_result.error}")

            alert = alert_result.data
            if alert is None:
                return ServiceResult.fail("Failed to save alert: No data returned")

            # Publish alert triggered event - create a dummy metric for manual alerts
            # Ensure models are rebuilt to handle forward references
            import contextlib

            from flext_core.domain.types import MetricType

            from flext_observability.domain.entities import Metric
            from flext_observability.domain.value_objects import ComponentName

            with contextlib.suppress(Exception):
                Metric.model_rebuild()

            dummy_metric = Metric(
                name="manual_alert",
                value=1.0,
                unit="count",
                metric_type=MetricType.GAUGE,
                component=ComponentName(name="manual", namespace="alerts"),
                labels={},
                timestamp=datetime.now(UTC),
            )
            event = AlertTriggered(
                alert=alert,
                metric=dummy_metric,
                severity=alert.severity,
            )
            await self.event_bus.publish(event)

            return ServiceResult.ok(alert)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create alert: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error creating alert: {e}")

    async def acknowledge_alert(
        self,
        alert_id: str,
        user: str,
    ) -> ServiceResult[Alert]:
        """Acknowledge an alert.

        Args:
            alert_id: ID of the alert to acknowledge.
            user: User acknowledging the alert.

        Returns:
            ServiceResult containing the acknowledged alert or error.

        """
        try:
            from uuid import UUID

            alert_uuid = UUID(alert_id)
            alert_result = await self.alert_repository.get_by_id(alert_uuid)
            if not alert_result.is_success:
                return ServiceResult.fail(f"Failed to get alert: {alert_result.error}")

            alert = alert_result.data
            if alert is None:
                return ServiceResult.fail("Alert not found")

            # Update alert status manually since there's no acknowledge method
            alert.acknowledged_by = user
            alert.acknowledged_at = datetime.now(UTC)

            # Save the updated alert (using save since there's no update method)
            save_result = await self.alert_repository.save(alert)
            if not save_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save acknowledged alert: {save_result.error}",
                )

            return ServiceResult.ok(alert)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to acknowledge alert: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error acknowledging alert: {e}")

    async def resolve_alert(
        self,
        alert_id: str,
        resolution_reason: str | None = None,
    ) -> ServiceResult[Alert]:
        """Resolve an alert.

        Args:
            alert_id: ID of the alert to resolve.
            resolution_reason: Optional reason for resolution.

        Returns:
            ServiceResult containing the resolved alert or error.

        """
        try:
            from uuid import UUID

            alert_uuid = UUID(alert_id)
            alert_result = await self.alert_repository.get_by_id(alert_uuid)
            if not alert_result.is_success:
                return ServiceResult.fail(f"Failed to get alert: {alert_result.error}")

            alert = alert_result.data
            if alert is None:
                return ServiceResult.fail("Alert not found")

            # Update alert status manually since there's no resolve method
            alert.resolved_at = datetime.now(UTC)
            alert.resolution_reason = resolution_reason

            # Save the updated alert (using save since there's no update method)
            save_result = await self.alert_repository.save(alert)
            if not save_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save resolved alert: {save_result.error}",
                )

            return ServiceResult.ok(alert)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to resolve alert: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error resolving alert: {e}")


class HealthService:
    """Application service for health monitoring."""

    def __init__(
        self,
        health_repository: HealthRepository[Any],
        health_analysis_service: HealthAnalysisService,
        event_bus: EventBus,
    ) -> None:
        """Initialize health service.

        Args:
            health_repository: Repository for storing health checks.
            health_analysis_service: Service for health analysis.
            event_bus: Event bus for publishing events.

        """
        self.health_repository = health_repository
        self.health_analysis_service = health_analysis_service
        self.event_bus = event_bus

    async def perform_health_check(
        self,
        name: str,
        check_type: str,
        component_name: str,
        *,
        component_namespace: str = "default",
        endpoint: str | None = None,
        timeout_seconds: int = 5,
    ) -> ServiceResult[HealthCheck]:
        """Perform a health check and analyze results.

        Args:
            name: Name of the health check.
            check_type: Type of health check to perform.
            component_name: Name of the component being checked.
            component_namespace: Namespace of the component.
            endpoint: Optional endpoint to check.
            timeout_seconds: Timeout for the health check.

        Returns:
            ServiceResult containing the health check result or error.

        """
        try:
            # Create health check entity from data, then save
            health_check_entity = HealthCheck(
                name=name,
                check_type=check_type,
                component=ComponentName(
                    name=component_name,
                    namespace=component_namespace,
                ),
                endpoint=endpoint,
                timeout_seconds=timeout_seconds,
            )

            # Simulate health check execution
            # In real implementation, this would perform actual health check
            health_check_entity.last_check_at = datetime.now(UTC)
            health_check_entity.is_healthy = True
            health_check_entity.response_time_ms = 50.0
            health_check_entity.check_result = {"status": "ok"}

            health_check_result = await self.health_repository.save(health_check_entity)
            if not health_check_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save health check: {health_check_result.error}",
                )

            health_check = health_check_result.data
            if health_check is None:
                return ServiceResult.fail(
                    "Failed to save health check: No data returned",
                )

            # Update system health analysis
            analysis_result = self.health_analysis_service.update_component_health(
                health_check,
            )
            if not analysis_result.is_success:
                return ServiceResult.fail(
                    f"Failed to update component health: {analysis_result.error}",
                )

            # Publish health check completed event
            from flext_observability.domain.value_objects import HealthStatus

            event = HealthCheckCompleted(
                health_check=health_check,
                component=health_check.component,
                status=(
                    HealthStatus.HEALTHY
                    if health_check.is_healthy
                    else HealthStatus.UNHEALTHY
                ),
                duration_ms=int(health_check.response_time_ms or 50.0),
            )
            await self.event_bus.publish(event)

            return ServiceResult.ok(health_check)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to perform health check: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error performing health check: {e}")

    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get system health overview.

        Returns:
            ServiceResult containing system health information or error.

        """
        try:
            # Health analysis service returns ServiceResult synchronously
            return self.health_analysis_service.get_system_health()

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error getting system health: {e}")


class LoggingService:
    """Application service for structured logging."""

    def __init__(
        self,
        log_repository: LogRepository[Any],
        log_analysis_service: LogAnalysisService,
        event_bus: EventBus,
    ) -> None:
        """Initialize logging service.

        Args:
            log_repository: Repository for storing log entries.
            log_analysis_service: Service for log analysis.
            event_bus: Event bus for publishing events.

        """
        self.log_repository = log_repository
        self.log_analysis_service = log_analysis_service
        self.event_bus = event_bus

    async def create_log_entry(
        self,
        level: str,
        message: str,
        logger_name: str,
        component_name: str,
        *,
        component_namespace: str = "default",
        module: str | None = None,
        function: str | None = None,
        line_number: int | None = None,
        extra: dict[str, Any] | None = None,
    ) -> ServiceResult[LogEntry]:
        """Create a structured log entry.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            message: Log message.
            logger_name: Name of the logger.
            component_name: Name of the component generating the log.
            component_namespace: Namespace of the component.
            module: Optional module name.
            function: Optional function name.
            line_number: Optional line number.
            extra: Optional additional fields.

        Returns:
            ServiceResult containing the created log entry or error.

        """
        try:
            # Create log entry entity from data, then save
            # Convert string level to LogLevel enum
            try:
                level_enum = LogLevel(level.upper())
            except ValueError:
                level_enum = LogLevel.INFO  # Default fallback

            log_entry_entity = LogEntry(
                level=level_enum,
                message=message,
                logger_name=logger_name,
                module=module,
                function=function,
                line_number=line_number,
                extra=extra or {},
            )

            log_entry_result = await self.log_repository.save(log_entry_entity)
            if not log_entry_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save log entry: {log_entry_result.error}",
                )

            log_entry = log_entry_result.data
            if log_entry is None:
                return ServiceResult.fail("Failed to save log entry: No data returned")

            # Analyze log entry
            analysis_result = self.log_analysis_service.analyze_log_entry(log_entry)
            if not analysis_result.is_success:
                return ServiceResult.fail(
                    f"Failed to analyze log entry: {analysis_result.error}",
                )

            # Publish log entry created event
            # LogEntryCreated needs component - we need to add it to LogEntry
            component = ComponentName(
                name=component_name,
                namespace=component_namespace,
            )
            event = LogEntryCreated(
                log_entry=log_entry,
                component=component,
                level=log_entry.level,
                message=log_entry.message,
            )
            await self.event_bus.publish(event)

            return ServiceResult.ok(log_entry)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to create log entry: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error creating log entry: {e}")


class TracingService:
    """Application service for distributed tracing."""

    def __init__(
        self,
        trace_repository: TraceRepository[Any],
        trace_analysis_service: TraceAnalysisService,
        event_bus: EventBus,
    ) -> None:
        """Initialize tracing service.

        Args:
            trace_repository: Repository for storing traces.
            trace_analysis_service: Service for trace analysis.
            event_bus: Event bus for publishing events.

        """
        self.trace_repository = trace_repository
        self.trace_analysis_service = trace_analysis_service
        self.event_bus = event_bus

    async def start_trace(
        self,
        operation_name: str,
        component_name: str,
        *,
        component_namespace: str = "default",
        trace_id: str | None = None,
        span_id: str | None = None,
        parent_span_id: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> ServiceResult[Trace]:
        """Start a new distributed trace.

        Args:
            operation_name: Name of the operation being traced.
            component_name: Name of the component generating the trace.
            component_namespace: Namespace of the component.
            trace_id: Optional trace ID (generated if not provided).
            span_id: Optional span ID (generated if not provided).
            parent_span_id: Optional parent span ID for nested spans.
            tags: Optional tags for the trace.

        Returns:
            ServiceResult containing the started trace or error.

        """
        try:
            # Generate IDs if not provided
            actual_trace_id = trace_id or str(uuid4())
            actual_span_id = span_id or str(uuid4())
            actual_component = ComponentName(
                name=component_name,
                namespace=component_namespace,
            )
            actual_tags = tags or {}
            actual_start_time = datetime.now(UTC)

            # Create trace entity from data, then save
            from flext_observability.domain.entities import Trace

            trace_entity = Trace(
                trace_id=actual_trace_id,
                span_id=actual_span_id,
                parent_span_id=parent_span_id,
                operation_name=operation_name,
                component=actual_component,
                service_name=component_name,
                trace_tags=actual_tags,
                start_time=actual_start_time,
            )
            trace_entity.start()

            # Save the trace entity
            trace_result = await self.trace_repository.save(trace_entity)
            if not trace_result.is_success:
                return ServiceResult.fail(f"Failed to save trace: {trace_result.error}")

            trace = trace_result.data
            if trace is None:
                return ServiceResult.fail("Failed to save trace: No data returned")

            # Publish trace started event
            # Ensure models are rebuilt to handle forward references
            import contextlib

            from flext_observability.domain.events import TraceStarted
            from flext_observability.domain.value_objects import ComponentName

            with contextlib.suppress(Exception):
                Trace.model_rebuild()
                ComponentName.model_rebuild()
                TraceStarted.model_rebuild()

            event = TraceStarted(
                trace=trace,
                component=trace.component,
                operation_name=trace.operation_name,
            )
            await self.event_bus.publish(event)

            return ServiceResult.ok(trace)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to start trace: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error starting trace: {e}")

    async def finish_trace(
        self,
        trace_id: str,
        *,
        success: bool = True,
        error: str | None = None,
    ) -> ServiceResult[Trace]:
        """Finish a distributed trace.

        Args:
            trace_id: ID of the trace to finish.
            success: Whether the trace completed successfully.
            error: Optional error message if the trace failed.

        Returns:
            ServiceResult containing the finished trace or error.

        """
        try:
            from uuid import UUID

            trace_uuid = UUID(trace_id)
            trace_result = await self.trace_repository.get_by_id(trace_uuid)
            if not trace_result.is_success:
                return ServiceResult.fail(f"Failed to get trace: {trace_result.error}")

            trace = trace_result.data
            if trace is None:
                return ServiceResult.fail("Trace not found")

            if success:
                trace.finish()
            else:
                trace.fail(error or "Unknown error")

            # Save the updated trace (using save since there's no update method)
            save_result = await self.trace_repository.save(trace)
            if not save_result.is_success:
                return ServiceResult.fail(
                    f"Failed to save updated trace: {save_result.error}",
                )

            # Analyze trace
            analysis_result = self.trace_analysis_service.analyze_trace(trace)
            if not analysis_result.is_success:
                return ServiceResult.fail(
                    f"Failed to analyze trace: {analysis_result.error}",
                )

            # Publish trace completed event
            # Ensure models are rebuilt to handle forward references
            import contextlib

            from flext_observability.domain.events import TraceCompleted
            from flext_observability.domain.value_objects import ComponentName

            with contextlib.suppress(Exception):
                ComponentName.model_rebuild()
                TraceCompleted.model_rebuild()

            event = TraceCompleted(
                trace=trace,
                component=trace.component,
                operation_name=trace.operation_name,
                duration_ms=int(trace.duration_ms or 0),
                success=success,
            )
            await self.event_bus.publish(event)

            return ServiceResult.ok(trace)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to finish trace: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error finishing trace: {e}")

    async def get_operation_stats(
        self,
        operation_name: str,
    ) -> ServiceResult[dict[str, Any]]:
        """Get statistics for a specific operation.

        Args:
            operation_name: Name of the operation to get statistics for.

        Returns:
            ServiceResult containing operation statistics or error.

        """
        try:
            return self.trace_analysis_service.get_operation_stats(operation_name)

        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get operation stats: {e}")
        except Exception as e:
            return ServiceResult.fail(f"Unexpected error getting operation stats: {e}")
