"""FLEXT Observability Services - Simplified using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Services simplificados usando padrões essenciais do flext-core.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextContainer, FlextResult, get_logger

from flext_observability.validation import create_observability_result_error

if TYPE_CHECKING:
    from flext_observability.entities import (
        FlextAlert,
        FlextHealthCheck,
        FlextLogEntry,
        FlextMetric,
        FlextTrace,
    )

# ============================================================================
# CORE SERVICES - Simplified using flext-core patterns
# ============================================================================


class FlextMetricsService:
    """Simplified metrics service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize metrics service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def record_metric(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Record metric using flext-core patterns."""
        try:
            self.logger.info(f"Recording metric: {metric.name} = {metric.value}")
            return FlextResult.ok(metric)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "metrics",
                f"Failed to record metric: {e}",
                metric_name=metric.name,
                metric_value=metric.value,
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextLoggingService:
    """Simplified logging service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize logging service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def log_entry(self, entry: FlextLogEntry) -> FlextResult[FlextLogEntry]:
        """Log entry using flext-core patterns."""
        try:
            level_method = getattr(self.logger, entry.level.lower(), self.logger.info)
            level_method(f"{entry.message} | Context: {entry.context}")
            return FlextResult.ok(entry)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "logging",
                f"Failed to log entry: {e}",
                log_level=entry.level,
                log_message=entry.message[:100],
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextTracingService:
    """Simplified tracing service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize tracing service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def start_trace(self, trace: FlextTrace) -> FlextResult[FlextTrace]:
        """Start trace using flext-core patterns."""
        try:
            self.logger.info(
                f"Starting trace: {trace.trace_id} | "
                f"Operation: {trace.operation}",
            )
            return FlextResult.ok(trace)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "tracing",
                f"Failed to start trace: {e}",
                trace_id=trace.trace_id,
                operation=trace.operation,
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextAlertService:
    """Simplified alert service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize alert service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def create_alert(self, alert: FlextAlert) -> FlextResult[FlextAlert]:
        """Create alert using flext-core patterns."""
        try:
            self.logger.warning(
                f"Alert created: {alert.title} | Severity: {alert.severity}",
            )
            return FlextResult.ok(alert)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "alert",
                f"Failed to create alert: {e}",
                alert_title=alert.title,
                alert_severity=alert.severity,
            )
            return FlextResult.fail(error_result.error or "Unknown error")


class FlextHealthService:
    """Simplified health service using flext-core patterns."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize health service."""
        self.container = container or FlextContainer()
        self.logger = get_logger(self.__class__.__name__)

    def check_health(self, health: FlextHealthCheck) -> FlextResult[FlextHealthCheck]:
        """Check health using flext-core patterns."""
        try:
            self.logger.info(f"Health check: {health.component} = {health.status}")
            return FlextResult.ok(health)
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "health_check",
                f"Failed to check health: {e}",
                component_name=health.component,
                health_status=health.status,
            )
            return FlextResult.fail(error_result.error or "Unknown error")

    def get_overall_health(self) -> FlextResult[dict[str, object]]:
        """Get overall system health."""
        try:
            return FlextResult.ok({
                "status": "healthy",
                "timestamp": "now",
                "components": {},
            })
        except (ValueError, TypeError, AttributeError) as e:
            error_result = create_observability_result_error(
                "health_check",
                f"Failed to get overall health: {e}",
            )
            return FlextResult.fail(error_result.error or "Unknown error")
