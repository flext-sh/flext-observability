"""Performance optimization and monitoring for observability operations.

Provides tools for monitoring observability system performance, tracking
overhead, and optimizing for production environments.

FLEXT Pattern:
- Single FlextObservabilityPerformance class
- Metrics collection for observability operations
- Memory and CPU tracking
- Latency monitoring for instrumentation
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import psutil
from flext_core import FlextLogger, FlextResult
from flext_core.protocols import p


@dataclass
class PerformanceMetrics:
    """Performance metrics for observability operations."""

    operation: str
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    duration_ms: float = 0.0
    memory_used_mb: float = 0.0
    cpu_percent: float = 0.0
    success: bool = True
    error_message: str | None = None

    def calculate_duration(self) -> None:
        """Calculate operation duration."""
        if math.isclose(self.end_time, 0.0):
            self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000


class FlextObservabilityPerformance:
    """Performance monitoring for observability operations.

    Tracks observability overhead and provides metrics for optimization.

    Usage:
        ```python
        from flext_observability import FlextObservabilityPerformance

        # Start monitoring operation
        monitor = FlextObservabilityPerformance.start_monitoring("http_request_tracing")

        # Perform observability operation
        try:
            trace_handler.trace_request(...)
            monitor.mark_success()
        except Exception as e:
            monitor.mark_error(str(e))
        finally:
            metrics = monitor.finish()
            # metrics.duration_ms, metrics.memory_used_mb, etc.
        ```

    Nested Classes:
        Monitor: Performance monitoring for individual operations
    """

    _logger: p.Log.StructlogLogger = FlextLogger.get_logger(__name__)
    _process: psutil.Process = psutil.Process()

    class Monitor:
        """Individual operation performance monitor."""

        metrics: PerformanceMetrics
        _initial_memory: float
        _initial_cpu: float

        def __init__(self, operation: str) -> None:
            """Initialize monitor for operation.

            Args:
                operation: Operation name for tracking

            """
            self.metrics = PerformanceMetrics(operation=operation)
            self._initial_memory = self._get_memory_usage()
            self._initial_cpu = self._get_cpu_percent()

        def _get_memory_usage(self) -> float:
            """Get current memory usage in MB."""
            try:
                memory_info = FlextObservabilityPerformance._process.memory_info()
                rss_bytes: int = memory_info.rss
                return float(rss_bytes) / 1024 / 1024
            except Exception:
                return 0.0

        def _get_cpu_percent(self) -> float:
            """Get current CPU usage percent."""
            try:
                cpu: float = FlextObservabilityPerformance._process.cpu_percent(
                    interval=0.01,
                )
                return cpu
            except Exception:
                return 0.0

        def mark_success(self) -> None:
            """Mark operation as successful."""
            self.metrics.success = True

        def mark_error(self, error_message: str) -> None:
            """Mark operation as failed.

            Args:
                error_message: Error description

            """
            self.metrics.success = False
            self.metrics.error_message = error_message

        def finish(self) -> PerformanceMetrics:
            """Finish monitoring and return metrics.

            Returns:
                PerformanceMetrics - Operation performance data

            """
            self.metrics.end_time = time.time()
            self.metrics.calculate_duration()

            # Calculate resource usage
            final_memory = self._get_memory_usage()
            self.metrics.memory_used_mb = max(0, final_memory - self._initial_memory)
            self.metrics.cpu_percent = self._get_cpu_percent()

            return self.metrics

    @staticmethod
    def start_monitoring(operation: str) -> FlextObservabilityPerformance.Monitor:
        """Start monitoring an operation.

        Args:
            operation: Operation name

        Returns:
            Monitor - Performance monitor for the operation

        """
        return FlextObservabilityPerformance.Monitor(operation)

    @staticmethod
    def is_performance_acceptable(metrics: PerformanceMetrics) -> bool:
        """Check if operation performance is acceptable.

        Args:
            metrics: Performance metrics to check

        Returns:
            bool - True if performance is acceptable

        Behavior:
            - HTTP instrumentation: < 5ms overhead acceptable
            - Database instrumentation: < 10ms overhead acceptable
            - Context operations: < 1ms overhead acceptable

        """
        if not metrics.success:
            return False

        # Define acceptable latencies per operation type
        acceptable_latencies: dict[str, float] = {
            "http_": 50.0,  # HTTP operations: < 50ms
            "database_": 100.0,  # Database operations: < 100ms
            "context_": 10.0,  # Context operations: < 10ms
            "sampling_": 5.0,  # Sampling: < 5ms
            "default": 100.0,  # Default: < 100ms
        }

        # Find applicable latency threshold
        threshold = acceptable_latencies["default"]
        for prefix, latency in acceptable_latencies.items():
            if metrics.operation.lower().startswith(prefix):
                threshold = latency
                break

        return metrics.duration_ms < threshold

    @staticmethod
    def log_performance_metrics(metrics: PerformanceMetrics) -> FlextResult[bool]:
        """Log performance metrics for operation.

        Args:
            metrics: Performance metrics to log

        Returns:
            FlextResult[bool] - Ok always

        """
        try:
            status = "OK" if metrics.success else "ERROR"
            level = "debug" if metrics.success else "warning"

            message = (
                f"{status} {metrics.operation}: "
                f"duration={metrics.duration_ms:.2f}ms, "
                f"memory={metrics.memory_used_mb:.2f}MB, "
                f"cpu={metrics.cpu_percent:.1f}%"
            )

            if metrics.error_message:
                message += f", error={metrics.error_message}"

            if level == "debug":
                FlextObservabilityPerformance._logger.debug(message)
            else:
                FlextObservabilityPerformance._logger.warning(message)

            return FlextResult[bool].ok(value=True)

        except Exception as e:
            return FlextResult[bool].fail(f"Failed to log metrics: {e}")

    @staticmethod
    def get_system_resources() -> dict[str, float]:
        """Get current system resource usage.

        Returns:
            dict - Resource usage metrics
                - memory_mb: Current memory usage
                - memory_percent: Memory usage percentage
                - cpu_percent: CPU usage percentage

        """
        try:
            memory_info = FlextObservabilityPerformance._process.memory_info()
            rss_bytes: int = memory_info.rss
            memory_mb: float = float(rss_bytes) / 1024 / 1024

            return {
                "memory_mb": memory_mb,
                "memory_percent": FlextObservabilityPerformance._process.memory_percent(),
                "cpu_percent": FlextObservabilityPerformance._process.cpu_percent(),
            }
        except Exception:
            return {"memory_mb": 0.0, "memory_percent": 0.0, "cpu_percent": 0.0}


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "FlextObservabilityPerformance",
    "PerformanceMetrics",
]
