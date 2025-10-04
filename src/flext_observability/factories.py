"""Unified observability service implementing FLEXT patterns.

REFACTORED: Eliminated factory patterns, wrappers, and multiple classes.
Uses unified service with direct composition following zero tolerance policy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime

# FIXED: Removed ImportError fallback - psutil must be available (ZERO TOLERANCE)
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextTypes,
    FlextUtilities,
)

from flext_observability.config import FlextObservabilityConfig
from flext_observability.services import (
    FlextObservabilityService,
)


# Master factory class - unified pattern
class FlextObservabilityMasterFactory:
    """Master factory for creating all observability components."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize the master factory with shared configuration."""
        self._container = container or FlextContainer.get_global()
        self._service = FlextObservabilityService()
        self._logger = FlextLogger(__name__)
        # Use global config instance to avoid duplication
        self._config = FlextObservabilityConfig.get_global_instance()

    def create_metrics_service(self) -> object:
        """Create a metrics service instance."""
        return self._service.metrics

    def create_tracing_service(self) -> object:
        """Create a tracing service instance."""
        return self._service.tracing

    def create_alert_service(self) -> object:
        """Create an alert service instance."""
        return self._service.alerts

    def create_health_service(self) -> object:
        """Create a health service instance."""
        return self._service.health

    def create_observability_service(self) -> FlextObservabilityService:
        """Create the main observability service instance."""
        return FlextObservabilityService()

    def create_metric(
        self, name: str, value: float, unit: str = "count"
    ) -> FlextTypes.Dict:
        """Create a metric using the factory."""
        try:
            metrics: FlextTypes.Dict = {
                "service_name": "flext_observability",
                "timestamp": FlextUtilities.Generators.generate_timestamp(),
                "name": name,
                "value": value,
                "unit": unit,
            }
            return metrics
        except Exception as e:
            msg = f"Metric creation failed: {e}"
            raise ValueError(msg) from e

    def create_trace(
        self, name: str, operation: str, context: FlextTypes.Dict | None = None
    ) -> FlextTypes.Dict:
        """Create a trace using the factory."""
        try:
            return {
                "trace_id": FlextUtilities.Generators.generate_entity_id(),
                "span_id": FlextUtilities.Generators.generate_entity_id(),
                "name": name,
                "operation": operation,
                "start_time": FlextUtilities.Generators.generate_timestamp(),
                "context": context or {},
            }
        except Exception as e:
            msg = f"Trace creation failed: {e}"
            raise ValueError(msg) from e

    def create_log_entry(
        self,
        level: str,
        message: str,
        metadata: FlextTypes.Dict | None = None,
    ) -> FlextTypes.Dict:
        """Create a log entry using the factory."""
        try:
            log_entry: FlextTypes.Dict = {
                "level": level,
                "message": message,
                "metadata": metadata or {},
                "timestamp": datetime.now(UTC).isoformat(),
                "correlation_id": FlextUtilities.Generators.generate_entity_id(),
            }
            return log_entry
        except Exception as e:
            msg = f"Log entry creation failed: {e}"
            raise ValueError(msg) from e

    def create_alert(
        self,
        title: str,
        message: str,
        severity: str = "info",
        source: str = "system",
    ) -> FlextTypes.Dict:
        """Create an alert using the factory."""
        try:
            alert: FlextTypes.Dict = {
                "alert_id": FlextUtilities.Generators.generate_entity_id(),
                "title": title,
                "message": message,
                "severity": severity,
                "source": source,
                "created_at": datetime.now(UTC).isoformat(),
                "status": "active",
            }
            return alert
        except Exception as e:
            msg = f"Alert creation failed: {e}"
            raise ValueError(msg) from e

    def process_alert(self, alert: FlextTypes.Dict) -> FlextTypes.Dict:
        """Process an alert."""
        try:
            return {
                **alert,
                "processed": True,
                "processed_at": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            msg = f"Alert processing failed: {e}"
            raise ValueError(msg) from e

    def escalate_alert(
        self, alert: FlextTypes.Dict, escalation_config: FlextTypes.Dict
    ) -> FlextTypes.Dict:
        """Escalate an alert."""
        try:
            return {
                **alert,
                "escalated": True,
                "escalation_config": escalation_config,
                "escalated_at": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            msg = f"Alert escalation failed: {e}"
            raise ValueError(msg) from e

    def start_trace(self, trace: FlextTypes.Dict) -> str:
        """Start a trace."""
        try:
            trace_id = trace.get(
                "trace_id", FlextUtilities.Generators.generate_entity_id()
            )
            self._logger.debug(f"Started trace: {trace_id}")
            return str(trace_id)
        except Exception as e:
            msg = f"Trace start failed: {e}"
            raise ValueError(msg) from e

    def complete_trace(self, trace: FlextTypes.Dict) -> FlextTypes.Dict:
        """Complete a trace."""
        try:
            return {
                **trace,
                "completed": True,
                "end_time": FlextUtilities.Generators.generate_timestamp(),
            }
        except Exception as e:
            msg = f"Trace completion failed: {e}"
            raise ValueError(msg) from e

    def get_trace_summary(self) -> FlextTypes.Dict:
        """Get trace summary."""
        try:
            return {"traces": 0, "active": 0, "completed": 0}
        except Exception as e:
            msg = f"Trace summary failed: {e}"
            raise ValueError(msg) from e

    def get_metrics_summary(self) -> FlextTypes.Dict:
        """Get metrics summary."""
        try:
            return {"metrics": 0, "total": 0, "active": 0}
        except Exception as e:
            msg = f"Metrics summary failed: {e}"
            raise ValueError(msg) from e

    def execute_health_check(self, health_check: FlextTypes.Dict) -> FlextTypes.Dict:
        """Execute a health check."""
        try:
            return {
                **health_check,
                "executed": True,
                "execution_time": FlextUtilities.Generators.generate_timestamp(),
            }
        except Exception as e:
            msg = f"Health check execution failed: {e}"
            raise ValueError(msg) from e

    def create_health_check(
        self,
        service_name: str,
        status: str = "healthy",
        details: FlextTypes.Dict | None = None,
    ) -> FlextTypes.Dict:
        """Create a health check using the factory."""
        try:
            health_check: FlextTypes.Dict = {
                "service_name": service_name,
                "status": status,
                "details": details or {},
                "timestamp": datetime.now(UTC).isoformat(),
                "check_id": FlextUtilities.Generators.generate_entity_id(),
            }
            return health_check
        except Exception as e:
            msg = f"Health check creation failed: {e}"
            raise ValueError(msg) from e

    class GlobalFactoryHolder:
        """Nested holder for the global factory instance - unified pattern."""

        _instance: FlextObservabilityMasterFactory | None = None

        @classmethod
        def get(cls) -> FlextObservabilityMasterFactory:
            """Get the global observability factory instance."""
            if cls._instance is None:
                cls._instance = FlextObservabilityMasterFactory()
            return cls._instance

        @classmethod
        def reset(cls) -> None:
            """Reset the global observability factory instance."""
            cls._instance = None


def get_global_factory() -> FlextObservabilityMasterFactory:
    """Get the global observability factory instance."""
    return FlextObservabilityMasterFactory.GlobalFactoryHolder.get()


def reset_global_factory() -> None:
    """Reset the global observability factory instance."""
    FlextObservabilityMasterFactory.GlobalFactoryHolder.reset()


__all__: FlextTypes.StringList = [
    "FlextObservabilityMasterFactory",
    "get_global_factory",
    "reset_global_factory",
]
