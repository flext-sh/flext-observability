"""FLEXT Observability Utilities - Centralized domain utilities.

Unified utilities facade inheriting core FLEXT utilities.
Provides namespace classes for monitoring, performance, health,
sampling, HTTP instrumentation, logging, metrics, error handling, and context.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextUtilities, r
from flext_observability import t


class FlextObservabilityUtilities(FlextUtilities):
    """Centralized utilities for FLEXT Observability.

    Inherits core FLEXT utilities, providing additional namespace classes
    for observability domain operations.
    """

    class Observability:
        """Observability-specific project utilities."""

        class Monitoring:
            """Monitoring and observation helpers."""

            @staticmethod
            def create_monitor_config(
                service_name: str,
                interval_seconds: int = 60,
                *,
                enabled: bool = True,
            ) -> t.ConfigurationMapping:
                """Create a monitoring configuration dictionary."""
                return {
                    "service_name": service_name,
                    "interval_seconds": interval_seconds,
                    "enabled": enabled,
                }

        class Performance:
            """Performance tracking helpers."""

            @staticmethod
            def calculate_duration(start_ns: int, end_ns: int) -> r[float]:
                """Calculate duration in seconds from nanosecond timestamps."""
                if end_ns < start_ns:
                    return r[float].fail("end_ns must be >= start_ns")
                return r[float].ok((end_ns - start_ns) / 1000000000)

        class Health:
            """Health check helpers."""

            @staticmethod
            def create_health_status(
                service_name: str,
                *,
                is_healthy: bool = True,
                details: str = "",
            ) -> t.FeatureFlagMapping:
                """Create a health status dictionary."""
                return {
                    "service": service_name,
                    "healthy": is_healthy,
                    "details": details,
                }

        class Sampling:
            """Sampling strategy helpers."""

            @staticmethod
            def should_sample(rate: float, request_id: int) -> bool:
                """Determine if a request should be sampled based on rate."""
                if rate <= 0.0:
                    return False
                if rate >= 1.0:
                    return True
                return request_id % 100 < int(rate * 100)

        class HTTP:
            """HTTP instrumentation helpers."""

            @staticmethod
            def extract_route_pattern(path: str) -> str:
                """Extract a generic route pattern from a concrete URL path."""
                parts = path.strip("/").split("/")
                normalized: t.StrSequence = [
                    "{id}" if part.isdigit() else part for part in parts
                ]
                return "/" + "/".join(normalized) if normalized else "/"

        class Logging:
            """Logging integration helpers."""

            @staticmethod
            def build_log_context(
                service_name: str,
                correlation_id: str = "",
            ) -> t.StrMapping:
                """Build a structured logging context dictionary."""
                ctx: t.MutableStrMapping = {"service": service_name}
                if correlation_id:
                    ctx["correlation_id"] = correlation_id
                return ctx

        class Metrics:
            """Custom metrics helpers."""

            @staticmethod
            def create_metric_key(namespace: str, name: str, unit: str = "") -> str:
                """Create a standardized metric key."""
                base = f"{namespace}.{name}"
                if unit:
                    return f"{base}.{unit}"
                return base

        class ErrorHandling:
            """Error handling helpers."""

            @staticmethod
            def classify_error(error: Exception) -> str:
                """Classify an error into a standard category string."""
                error_type = type(error).__name__
                if "Timeout" in error_type:
                    return "timeout"
                if "Connection" in error_type:
                    return "connection"
                if "Permission" in error_type or "Auth" in error_type:
                    return "auth"
                return "unknown"

        class TraceContext:
            """Context management helpers."""

            @staticmethod
            def create_trace_context(
                trace_id: str,
                span_id: str,
                parent_span_id: str = "",
            ) -> t.StrMapping:
                """Create a trace context dictionary."""
                ctx: t.MutableStrMapping = {
                    "trace_id": trace_id,
                    "span_id": span_id,
                }
                if parent_span_id:
                    ctx["parent_span_id"] = parent_span_id
                return ctx


u = FlextObservabilityUtilities

__all__ = ["FlextObservabilityUtilities", "u"]
