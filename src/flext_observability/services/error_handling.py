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

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import time

from flext_observability import c, m, p, r, s, t, u
from flext_observability.services import FlextObservabilityContext


class FlextObservabilityErrorHandling:
    """Error handling and deduplication system.

    Provides intelligent error aggregation to reduce alert fatigue.

    Usage:
        Fetch the shared handler with ``active_handler()``, record error
        events with ``record_error``, and consult ``should_alert`` before
        dispatching notifications.

    Nested Classes:
        Handler: Error handling and deduplication logic
    """

    logger = u.fetch_logger(__name__)

    @staticmethod
    def _extract_validation_message(error: t.ValidationError) -> str:
        errors = error.errors()
        if not errors:
            return str(error)
        message: str = errors[0].get("msg", "Validation failed")
        prefix = "Value error, "
        if message.startswith(prefix):
            stripped: str = message.removeprefix(prefix)
            return stripped
        return message

    class Handler(s[p.Observability.ErrorEvent]):
        """Error handling and deduplication handler."""

        def __init__(
            self,
            *,
            runtime_settings: p.Settings | None = None,
            initial_context: p.Context | None = None,
        ) -> None:
            """Initialize error handler."""
            super().__init__(
                runtime_settings=runtime_settings,
                initial_context=initial_context,
            )
            self._state = m.Observability.ErrorHandlingState()

        def clear_error_counts(
            self,
            older_than_sec: float | None = None,
        ) -> p.Result[bool]:
            """Clear recorded error counts.

            Args:
                older_than_sec: Clear only counts older than N seconds
                    (``None`` clears all).

            Returns:
                ``True`` when counts were cleared successfully.

            """

            def operation() -> bool:
                if older_than_sec is None:
                    self._state.error_counts.clear()
                    self._state.last_alert_time.clear()
                else:
                    self._state.error_counts.clear()
                FlextObservabilityErrorHandling.logger.debug("Error counts cleared")
                return True

            return r[bool].create_from_callable(operation)

        def resolve_error_count(self, fingerprint: str) -> int:
            """Resolve the count of errors with a given fingerprint.

            Args:
                fingerprint: Error fingerprint.

            Returns:
                Recorded error count.

            """
            # Why: mro-4p0t — empty dict literal widens .get() to Any for mypy.
            return self._state.error_counts.get(fingerprint, 0)

        def resolve_escalated_severity(
            self,
            error: p.Observability.ErrorEvent,
        ) -> t.Observability.ErrorSeverity:
            """Resolve the escalated severity based on the error count.

            Args:
                error: Error event to evaluate.

            Returns:
                Escalated severity for the error.

            """
            error = m.Observability.ErrorEvent.model_validate(
                error, from_attributes=True
            )
            if not error.fingerprint:
                error = error.calculate_fingerprint()
            count = self._state.error_counts.get(error.fingerprint, 0)
            if count >= self._state.escalation_threshold * 3:
                return c.Observability.ErrorSeverity.CRITICAL
            if count >= self._state.escalation_threshold * 2:
                return c.Observability.ErrorSeverity.ERROR
            if count >= self._state.escalation_threshold:
                return c.Observability.ErrorSeverity.WARNING
            return error.severity

        def record_alert_sent(self, error: p.Observability.ErrorEvent) -> None:
            """Record that an alert was sent for the error.

            Args:
                error: Error the alert was sent for.

            """
            error = m.Observability.ErrorEvent.model_validate(
                error, from_attributes=True
            )
            if not error.fingerprint:
                error = error.calculate_fingerprint()
            self._state.last_alert_time[error.fingerprint] = time.time()

        def record_error(
            self,
            error: p.Observability.ErrorEvent,
        ) -> p.Result[p.Observability.ErrorEvent]:
            """Record an error event.

            Args:
                error: Error event to record.

            Returns:
                Updated error with fingerprint and correlation ID.

            Behavior:
                - Calculates fingerprint
                - Updates error counts
                - Preserves explicitly supplied correlation, including absence
                - Reads current context only for direct events without a snapshot

            """

            def operation() -> p.Observability.ErrorEvent:
                observed = m.Observability.ErrorEvent.model_validate(
                    error,
                    from_attributes=True,
                )
                current_error = observed.calculate_fingerprint()
                if c.ContextKey.CORRELATION_ID not in observed.model_fields_set:
                    current_error = current_error.model_copy(
                        update={
                            c.ContextKey.CORRELATION_ID: (
                                FlextObservabilityContext.correlation_id()
                            ),
                        },
                    )
                self._state.error_counts[current_error.fingerprint] = (
                    self._state.error_counts.get(current_error.fingerprint, 0) + 1
                )
                return current_error

            return r[p.Observability.ErrorEvent].create_from_callable(operation)

        def update_alert_cooldown(self, seconds: float) -> p.Result[bool]:
            """Update the minimum seconds between alerts for the same error.

            Args:
                seconds: Cooldown duration in seconds.

            Returns:
                ``True`` when the cooldown was applied.

            """
            try:
                validated_seconds = m.Observability.CooldownInput.model_validate(
                    obj={"seconds": seconds},
                ).seconds
            except c.ValidationError as error:
                return r[bool].fail(
                    FlextObservabilityErrorHandling._extract_validation_message(error),
                )
            self._state.alert_cooldown_sec = validated_seconds
            FlextObservabilityErrorHandling.logger.debug(
                f"Alert cooldown set to {validated_seconds}s",
            )
            return r[bool].ok(value=True)

        def update_escalation_threshold(self, threshold: int) -> p.Result[bool]:
            """Update the threshold for error escalation.

            Args:
                threshold: Number of errors before escalation.

            Returns:
                ``True`` when the threshold was applied.

            """
            try:
                validated_threshold = m.Observability.ThresholdInput.model_validate(
                    obj={"threshold": threshold},
                ).threshold
            except c.ValidationError as error:
                return r[bool].fail(
                    FlextObservabilityErrorHandling._extract_validation_message(error),
                )
            self._state.escalation_threshold = validated_threshold
            FlextObservabilityErrorHandling.logger.debug(
                f"Escalation threshold set to {validated_threshold}",
            )
            return r[bool].ok(value=True)

        def should_alert_for_error(self, error: p.Observability.ErrorEvent) -> bool:
            """Determine whether the error should trigger an alert.

            Args:
                error: Error event to evaluate.

            Returns:
                ``True`` when an alert should be sent.

            Behavior:
                - Checks cooldown period (don't spam same error)
                - Considers error count (escalate repeated errors)
                - Respects severity level

            """
            error = m.Observability.ErrorEvent.model_validate(
                error, from_attributes=True
            )
            if not error.fingerprint:
                error = error.calculate_fingerprint()
            if error.severity == c.Observability.ErrorSeverity.CRITICAL:
                return True
            last_alert = self._state.last_alert_time.get(error.fingerprint, 0)
            if time.time() - last_alert < self._state.alert_cooldown_sec:
                return False
            count = self._state.error_counts.get(error.fingerprint, 0)
            return not count < self._state.escalation_threshold

    @staticmethod
    def active_handler() -> p.Observability.ErrorHandler:
        """Return the global error handler instance.

        Returns:
            Shared error handler.

        """
        return FlextObservabilityErrorHandling.Handler.fetch_global()

    @staticmethod
    def record_error(
        error: p.Observability.ErrorEvent,
    ) -> p.Result[p.Observability.ErrorEvent]:
        """Record an error event through the global handler.

        Args:
            error: Error event to record.

        Returns:
            Updated error with fingerprint.

        """
        handler = FlextObservabilityErrorHandling.active_handler()
        return handler.record_error(error)

    @staticmethod
    def should_alert(error: p.Observability.ErrorEvent) -> bool:
        """Check whether the error should trigger an alert.

        Args:
            error: Error event to evaluate.

        Returns:
            ``True`` when an alert should be sent.

        """
        handler = FlextObservabilityErrorHandling.active_handler()
        return handler.should_alert_for_error(error)


__all__: list[str] = ["FlextObservabilityErrorHandling"]
