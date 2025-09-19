"""Unified observability service implementing FLEXT patterns.

REFACTORED: Eliminated factory patterns, wrappers, and multiple classes.
Uses unified service with direct composition following zero tolerance policy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import cast

# FIXED: Removed ImportError fallback - psutil must be available (ZERO TOLERANCE)
import psutil

from flext_core import (
    FlextContainer,
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextTypes,
)


def _generate_utc_datetime() -> datetime:
    """Generate UTC datetime using flext-core pattern."""
    return datetime.now(tz=UTC)


class FlextObservabilityService(FlextDomainService[FlextTypes.Core.Dict]):
    """Observability service providing metrics, tracing, and logging capabilities.

    Unified class implementing observability patterns with flext-core foundation.
    """

    def __init__(self, **_data: object) -> None:
        """Initialize observability service with flext-core foundation."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        self._metrics_enabled = True
        self._tracing_enabled = True

    class _MetricsHelper:
        """Nested helper for metrics collection."""

        @staticmethod
        def collect_system_metrics() -> FlextResult[dict[str, float]]:
            """Collect system performance metrics."""
            # FIXED: Removed psutil availability check - psutil must be available (ZERO TOLERANCE)
            metrics = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "load_average": psutil.getloadavg()[0]
                if hasattr(psutil, "getloadavg")
                else 0.0,
            }

            return FlextResult[dict[str, float]].ok(metrics)

        @staticmethod
        def format_metrics(metrics: dict[str, float]) -> FlextResult[dict[str, str]]:
            """Format metrics for display."""
            try:
                formatted = {}
                for key, value in metrics.items():
                    # All values are guaranteed to be float by type hint
                    formatted[key] = f"{value:.2f}%"

                return FlextResult[dict[str, str]].ok(formatted)

            except Exception as e:
                return FlextResult[dict[str, str]].fail(
                    f"Metrics formatting error: {e!s}",
                )

    class _TracingHelper:
        """Nested helper for distributed tracing."""

        @staticmethod
        def create_trace_context() -> FlextResult[dict[str, str]]:
            """Create distributed tracing context."""
            try:
                trace_context = {
                    "trace_id": str(uuid.uuid4()),
                    "span_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(UTC).isoformat(),
                    "service": "flext-observability",
                }

                return FlextResult[dict[str, str]].ok(trace_context)

            except Exception as e:
                return FlextResult[dict[str, str]].fail(
                    f"Trace context creation error: {e!s}",
                )

        @staticmethod
        def log_trace_event(context: dict[str, str], event: str) -> FlextResult[None]:
            """Log trace event with context."""
            try:
                logger = FlextLogger(__name__)
                logger.info(f"TRACE[{context.get('trace_id', 'unknown')}]: {event}")

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Trace logging error: {e!s}")

    def health_check(self) -> FlextResult[str]:
        """Check observability service health."""
        self._logger.debug("Performing observability health check")

        # Test metrics collection
        metrics_result = self._MetricsHelper.collect_system_metrics()
        if metrics_result.is_failure:
            return FlextResult[str].fail(
                f"Metrics collection failed: {metrics_result.error}",
            )

        # Test tracing
        trace_result = self._TracingHelper.create_trace_context()
        if trace_result.is_failure:
            return FlextResult[str].fail(f"Tracing failed: {trace_result.error}")

        return FlextResult[str].ok("Observability service healthy")

    def collect_observability_data(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Collect comprehensive observability data."""
        self._logger.info("Collecting observability data")

        observability_data = {}

        # Collect metrics if enabled
        if self._metrics_enabled:
            metrics_result = self._MetricsHelper.collect_system_metrics()
            if metrics_result.is_success:
                format_result = self._MetricsHelper.format_metrics(
                    metrics_result.unwrap(),
                )
                if format_result.is_success:
                    observability_data["metrics"] = format_result.unwrap()

        # Create trace context if enabled
        if self._tracing_enabled:
            trace_result = self._TracingHelper.create_trace_context()
            if trace_result.is_success:
                observability_data["trace_context"] = trace_result.unwrap()

        # Add service metadata
        observability_data["service_info"] = {
            "name": "flext-observability",
            "version": "1.0.0",
            "metrics_enabled": str(self._metrics_enabled),
            "tracing_enabled": str(self._tracing_enabled),
        }

        return FlextResult[FlextTypes.Core.Dict].ok(
            cast("FlextTypes.Core.Dict", observability_data),
        )

    def execute(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Execute observability service operation."""
        self._logger.info("Executing observability service")

        # Health check first
        health_result = self.health_check()
        if health_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Health check failed: {health_result.error}",
            )

        # Collect observability data
        data_result = self.collect_observability_data()
        if data_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Data collection failed: {data_result.error}",
            )

        return data_result


__all__: FlextTypes.Core.StringList = [
    "FlextObservabilityService",
]
