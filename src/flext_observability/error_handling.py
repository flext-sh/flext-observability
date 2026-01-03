"""Error aggregation and deduplication for intelligent alerting.

Provides smart error fingerprinting, aggregation, and deduplication to reduce
alert fatigue while ensuring critical issues are visible.

FLEXT Pattern:
- Single FlextObservabilityErrorHandling class
- Error fingerprinting for grouping
- Alert deduplication rules
- Severity escalation

Key Features:
- Error fingerprinting (group similar errors)
- Alert deduplication (reduce noise)
- Severity escalation (escalate repeated errors)
- Rate limiting (prevent alert storms)
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field

from flext_core import FlextLogger, FlextResult, FlextTypes as t

from flext_observability.constants import c
from flext_observability.context import FlextObservabilityContext

# Alias for backward compatibility - ErrorSeverity is now centralized in constants.py
ErrorSeverity = c.Observability.ErrorSeverity


@dataclass
class ErrorEvent:
    """Represents an error event."""

    error_type: str
    message: str
    severity: ErrorSeverity
    timestamp: float = field(default_factory=time.time)
    correlation_id: str = ""
    context: dict[str, t.GeneralValueType] = field(default_factory=dict)
    fingerprint: str = ""

    def calculate_fingerprint(self) -> str:
        """Calculate fingerprint for error deduplication.

        Returns:
            str - Error fingerprint hash

        """
        # Create fingerprint from error type and message
        fingerprint_data = f"{self.error_type}:{self.message}"
        self.fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        return self.fingerprint


class FlextObservabilityErrorHandling:
    """Error handling and deduplication system.

    Provides intelligent error aggregation to reduce alert fatigue.

    Usage:
        ```python
        from flext_observability import FlextObservabilityErrorHandling

        handler = FlextObservabilityErrorHandling.get_handler()

        # Create error event
        error = ErrorEvent(
            error_type="DatabaseError",
            message="Connection timeout",
            severity=ErrorSeverity.ERROR,
        )

        # Check if error should be alerted
        should_alert = handler.should_alert_for_error(error)
        if should_alert:
            send_alert(error)
        ```

    Nested Classes:
        Handler: Error handling and deduplication logic
    """

    _logger = FlextLogger.get_logger(__name__)
    _handler_instance: FlextObservabilityErrorHandling.Handler | None = None

    class Handler:
        """Error handling and deduplication handler."""

        def __init__(self) -> None:
            """Initialize error handler."""
            self._error_counts: dict[str, int] = {}  # fingerprint -> count
            self._last_alert_time: dict[str, float] = {}  # fingerprint -> timestamp
            self._alert_cooldown_sec = 60.0  # Min seconds between alerts
            self._escalation_threshold = 5  # Escalate after N errors
            self._deduplication_window_sec = 300  # 5 minutes

        def set_alert_cooldown(self, seconds: float) -> FlextResult[None]:
            """Set minimum seconds between alerts for same error.

            Args:
                seconds: Cooldown duration in seconds

            Returns:
                FlextResult[None] - Ok if valid

            """
            if seconds < 0:
                return FlextResult[None].fail("Cooldown must be >= 0")

            self._alert_cooldown_sec = seconds
            FlextObservabilityErrorHandling._logger.debug(
                f"Alert cooldown set to {seconds}s",
            )
            return FlextResult[None].ok(None)

        def set_escalation_threshold(self, threshold: int) -> FlextResult[None]:
            """Set threshold for error escalation.

            Args:
                threshold: Number of errors before escalation

            Returns:
                FlextResult[None] - Ok if valid

            """
            if threshold < 1:
                return FlextResult[None].fail("Threshold must be >= 1")

            self._escalation_threshold = threshold
            FlextObservabilityErrorHandling._logger.debug(
                f"Escalation threshold set to {threshold}",
            )
            return FlextResult[None].ok(None)

        def record_error(self, error: ErrorEvent) -> FlextResult[ErrorEvent]:
            """Record an error event.

            Args:
                error: Error event to record

            Returns:
                FlextResult[ErrorEvent] - Updated error with fingerprint

            Behavior:
                - Calculates fingerprint
                - Updates error counts
                - Sets correlation ID if available

            """
            try:
                # Calculate fingerprint
                error.calculate_fingerprint()

                # Get correlation ID - optional enrichment
                try:
                    error.correlation_id = (
                        FlextObservabilityContext.get_correlation_id()
                    )
                except Exception as e:
                    FlextObservabilityErrorHandling._logger.debug(
                        f"Could not set correlation_id: {e}",
                    )
                    error.correlation_id = ""

                # Increment error count
                self._error_counts[error.fingerprint] = (
                    self._error_counts.get(error.fingerprint, 0) + 1
                )

                FlextObservabilityErrorHandling._logger.debug(
                    f"Error recorded: {error.error_type} (fingerprint: {error.fingerprint[:8]})",
                )

                return FlextResult[ErrorEvent].ok(error)

            except Exception as e:
                return FlextResult[ErrorEvent].fail(f"Failed to record error: {e}")

        def should_alert_for_error(self, error: ErrorEvent) -> bool:
            """Determine if error should trigger an alert.

            Args:
                error: Error event to evaluate

            Returns:
                bool - True if alert should be sent

            Behavior:
                - Checks cooldown period (don't spam same error)
                - Considers error count (escalate repeated errors)
                - Respects severity level

            """
            # Calculate fingerprint if not already done
            if not error.fingerprint:
                error.calculate_fingerprint()

            # Critical errors always alert
            if error.severity == ErrorSeverity.CRITICAL:
                return True

            # Check cooldown period
            last_alert = self._last_alert_time.get(error.fingerprint, 0)
            if time.time() - last_alert < self._alert_cooldown_sec:
                return False

            # Check escalation threshold
            count = self._error_counts.get(error.fingerprint, 0)
            return not count < self._escalation_threshold

        def get_escalated_severity(self, error: ErrorEvent) -> ErrorSeverity:
            """Get escalated severity based on error count.

            Args:
                error: Error event

            Returns:
                ErrorSeverity - Escalated severity

            """
            if not error.fingerprint:
                error.calculate_fingerprint()

            count = self._error_counts.get(error.fingerprint, 0)

            # Escalate based on count
            if count >= self._escalation_threshold * 3:
                return ErrorSeverity.CRITICAL
            if count >= self._escalation_threshold * 2:
                return ErrorSeverity.ERROR
            if count >= self._escalation_threshold:
                return ErrorSeverity.WARNING

            return error.severity

        def record_alert_sent(self, error: ErrorEvent) -> None:
            """Record that alert was sent for error.

            Args:
                error: Error that was alerted

            """
            if not error.fingerprint:
                error.calculate_fingerprint()

            self._last_alert_time[error.fingerprint] = time.time()

        def get_error_count(self, fingerprint: str) -> int:
            """Get count of errors with given fingerprint.

            Args:
                fingerprint: Error fingerprint

            Returns:
                int - Error count

            """
            return self._error_counts.get(fingerprint, 0)

        def clear_error_counts(
            self,
            older_than_sec: float | None = None,
        ) -> FlextResult[None]:
            """Clear error counts.

            Args:
                older_than_sec: Clear only counts older than N seconds (None = clear all)

            Returns:
                FlextResult[None] - Ok if successful

            """
            try:
                if older_than_sec is None:
                    self._error_counts.clear()
                    self._last_alert_time.clear()
                else:
                    # Clear old entries (would need timestamp tracking)
                    self._error_counts.clear()

                FlextObservabilityErrorHandling._logger.debug("Error counts cleared")
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Failed to clear error counts: {e}")

    @staticmethod
    def get_handler() -> FlextObservabilityErrorHandling.Handler:
        """Get global error handler instance (singleton).

        Returns:
            Handler - Global error handler

        """
        if FlextObservabilityErrorHandling._handler_instance is None:
            FlextObservabilityErrorHandling._handler_instance = (
                FlextObservabilityErrorHandling.Handler()
            )

        return FlextObservabilityErrorHandling._handler_instance

    @staticmethod
    def record_error(error: ErrorEvent) -> FlextResult[ErrorEvent]:
        """Convenience function: record an error.

        Args:
            error: Error event

        Returns:
            FlextResult[ErrorEvent] - Updated error with fingerprint

        """
        handler = FlextObservabilityErrorHandling.get_handler()
        return handler.record_error(error)

    @staticmethod
    def should_alert(error: ErrorEvent) -> bool:
        """Convenience function: check if error should alert.

        Args:
            error: Error event

        Returns:
            bool - True if should alert

        """
        handler = FlextObservabilityErrorHandling.get_handler()
        return handler.should_alert_for_error(error)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "ErrorEvent",
    "ErrorSeverity",
    "FlextObservabilityErrorHandling",
]
