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

import time
from collections.abc import Callable, MutableMapping

from pydantic import ValidationError

from flext_observability import FlextObservabilityContext, c, m, t, r, u


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
            severity=c.Observability.ErrorSeverity.ERROR,
        )

        # Check if error should be alerted
        should_alert = handler.should_alert_for_error(error)
        if should_alert:
            send_alert(error)
        ```

    Nested Classes:
        Handler: Error handling and deduplication logic
    """

    _logger = u.fetch_logger(__name__)
    _handler_instance: FlextObservabilityErrorHandling.Handler | None = None

    @staticmethod
    def _extract_validation_message(error: ValidationError) -> str:
        errors = error.errors()
        if not errors:
            return str(error)
        message = str(errors[0].get("msg", "Validation failed"))
        prefix = "Value error, "
        if message.startswith(prefix):
            return message.removeprefix(prefix)
        return message

    class Handler:
        """Error handling and deduplication handler."""

        def __init__(self) -> None:
            """Initialize error handler."""
            self._error_counts: t.MutableIntMapping = {}
            self._last_alert_time: MutableMapping[str, float] = {}
            self._alert_cooldown_sec = 60.0
            self._escalation_threshold = 5
            self._deduplication_window_sec = 300

        def clear_error_counts(self, older_than_sec: float | None = None) -> r[bool]:
            """Clear error counts.

            Args:
                older_than_sec: Clear only counts older than N seconds (None = clear all)

            Returns:
                r[bool] - Ok if successful

            """

            def operation() -> bool:
                if older_than_sec is None:
                    self._error_counts.clear()
                    self._last_alert_time.clear()
                else:
                    self._error_counts.clear()
                FlextObservabilityErrorHandling._logger.debug("Error counts cleared")
                return True

            return self._run_with_result(
                operation,
                error_prefix="Failed to clear error counts",
            )

        def get_error_count(self, fingerprint: str) -> int:
            """Get count of errors with given fingerprint.

            Args:
                fingerprint: Error fingerprint

            Returns:
                int - Error count

            """
            return self._error_counts.get(fingerprint, 0)

        def get_escalated_severity(
            self,
            error: m.Observability.ErrorEvent,
        ) -> c.Observability.ErrorSeverity:
            """Get escalated severity based on error count.

            Args:
                error: Error event

            Returns:
                c.Observability.ErrorSeverity - Escalated severity

            """
            if not error.fingerprint:
                error.calculate_fingerprint()
            count = self._error_counts.get(error.fingerprint, 0)
            if count >= self._escalation_threshold * 3:
                return c.Observability.ErrorSeverity.CRITICAL
            if count >= self._escalation_threshold * 2:
                return c.Observability.ErrorSeverity.ERROR
            if count >= self._escalation_threshold:
                return c.Observability.ErrorSeverity.WARNING
            return error.severity

        def record_alert_sent(self, error: m.Observability.ErrorEvent) -> None:
            """Record that alert was sent for error.

            Args:
                error: Error that was alerted

            """
            if not error.fingerprint:
                error.calculate_fingerprint()
            self._last_alert_time[error.fingerprint] = time.time()

        def record_error(
            self,
            error: m.Observability.ErrorEvent,
        ) -> r[m.Observability.ErrorEvent]:
            """Record an error event.

            Args:
                error: Error event to record

            Returns:
                r[ErrorEvent] - Updated error with fingerprint

            Behavior:
                - Calculates fingerprint
                - Updates error counts
                - Sets correlation ID if available

            """

            def operation() -> m.Observability.ErrorEvent:
                error.calculate_fingerprint()
                try:
                    error.correlation_id = (
                        FlextObservabilityContext.get_correlation_id()
                    )
                except (ValueError, TypeError, KeyError) as e:
                    FlextObservabilityErrorHandling._logger.warning(
                        f"Could not set correlation_id, falling back to empty: {e}",
                    )
                    error.correlation_id = ""
                self._error_counts[error.fingerprint] = (
                    self._error_counts.get(error.fingerprint, 0) + 1
                )
                FlextObservabilityErrorHandling._logger.debug(
                    f"Error recorded: {error.error_type} (fingerprint: {error.fingerprint[:8]})",
                )
                return error

            return self._run_with_result(
                operation,
                error_prefix="Failed to record error",
            )

        def set_alert_cooldown(self, seconds: float) -> r[bool]:
            """Set minimum seconds between alerts for same error.

            Args:
                seconds: Cooldown duration in seconds

            Returns:
                r[bool] - Ok if valid

            """
            try:
                validated_seconds = m.Observability.CooldownInput.model_validate(
                    obj={"seconds": seconds},
                ).seconds
            except ValidationError as error:
                return r[bool].fail(
                    FlextObservabilityErrorHandling._extract_validation_message(error),
                )
            self._alert_cooldown_sec = validated_seconds
            FlextObservabilityErrorHandling._logger.debug(
                f"Alert cooldown set to {validated_seconds}s",
            )
            return r[bool].ok(value=True)

        def set_escalation_threshold(self, threshold: int) -> r[bool]:
            """Set threshold for error escalation.

            Args:
                threshold: Number of errors before escalation

            Returns:
                r[bool] - Ok if valid

            """
            try:
                validated_threshold = m.Observability.ThresholdInput.model_validate(
                    obj={"threshold": threshold},
                ).threshold
            except ValidationError as error:
                return r[bool].fail(
                    FlextObservabilityErrorHandling._extract_validation_message(error),
                )
            self._escalation_threshold = validated_threshold
            FlextObservabilityErrorHandling._logger.debug(
                f"Escalation threshold set to {validated_threshold}",
            )
            return r[bool].ok(value=True)

        def should_alert_for_error(self, error: m.Observability.ErrorEvent) -> bool:
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
            if not error.fingerprint:
                error.calculate_fingerprint()
            if error.severity == c.Observability.ErrorSeverity.CRITICAL:
                return True
            last_alert = self._last_alert_time.get(error.fingerprint, 0)
            if time.time() - last_alert < self._alert_cooldown_sec:
                return False
            count = self._error_counts.get(error.fingerprint, 0)
            return not count < self._escalation_threshold

        def _run_with_result[TResult](
            self,
            operation: Callable[[], TResult],
            *,
            error_prefix: str,
        ) -> r[TResult]:
            try:
                return r[TResult].ok(operation())
            except (ValueError, TypeError, KeyError) as e:
                FlextObservabilityErrorHandling._logger.warning(f"{error_prefix}: {e}")
                return r[TResult].fail(f"{error_prefix}: {e}")

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
    def record_error(
        error: m.Observability.ErrorEvent,
    ) -> r[m.Observability.ErrorEvent]:
        """Convenience function: record an error.

        Args:
            error: Error event

        Returns:
            r[ErrorEvent] - Updated error with fingerprint

        """
        handler = FlextObservabilityErrorHandling.get_handler()
        return handler.record_error(error)

    @staticmethod
    def should_alert(error: m.Observability.ErrorEvent) -> bool:
        """Convenience function: check if error should alert.

        Args:
            error: Error event

        Returns:
            bool - True if should alert

        """
        handler = FlextObservabilityErrorHandling.get_handler()
        return handler.should_alert_for_error(error)


__all__ = ["FlextObservabilityErrorHandling"]
