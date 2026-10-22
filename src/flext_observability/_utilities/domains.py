"""Observability-specific project utilities owned by the private utilities family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import r, u

from flext_observability import c, m, p


class FlextObservabilityUtilitiesDomains:
    """Observability-specific project utilities."""

    class ContextStage:
        """Read injected live context at Core's native processor boundary."""

        def __init__(self, context: p.Observability.LoggingContext) -> None:
            """Retain the actual context provider, never a context snapshot."""
            self._context = context

        def __call__(
            self,
            logger: p.OutputLogger,
            method_name: str,
            event_dict: p.LoggingEvent,
        ) -> p.LoggingEvent:
            """Supply only existing operation identifiers before sanitization.

            Returns:
                The event updated with the provider's current identifiers.

            """
            _ = logger, method_name
            for key, value in (
                ("correlation_id", self._context.correlation_id()),
                ("trace_id", self._context.trace_id()),
                ("span_id", self._context.span_id()),
            ):
                if value:
                    event_dict[key] = value
                else:
                    event_dict.pop(key, None)
            return event_dict

    class ErrorObserver:
        """Adapt sanitized Core records to an injected domain recording service."""

        def __init__(self, recorder: p.Observability.ErrorRecorder) -> None:
            """Retain the actual recording port, not a second error engine."""
            self._recorder = recorder

        def __call__(self, event: p.LoggingRecord) -> None:
            """Record actual exceptions; use Core's canonical failure terminal."""
            if event.exception is None:
                return
            error = m.Observability.ErrorEvent(
                error_type=type(event.exception).__name__,
                message=u.str_adapter().validate_python(
                    event.context["exception_message"],
                ),
                severity=c.Observability.ErrorSeverity(event.level),
                correlation_id=u.str_adapter().validate_python(
                    event.context.get("correlation_id", ""),
                ),
            )
            self._recorder.record_error(error).unwrap()

    @staticmethod
    def compose_logging(
        options: p.StructlogOptions,
        *,
        context_stage: p.LoggingStage,
        capture: p.LoggingObserver,
        errors: p.LoggingObserver,
        enabled: bool = True,
    ) -> p.StructlogOptions:
        """Compose supplied providers without configuring the process runtime.

        The caller owns provider identities and configuration lifecycle. Removing
        this binding preserves all unrelated stages, observers and destinations.

        Returns:
            Copied options with the supplied providers attached or removed.

        Raises:
            TypeError: A supplied stage or observer violates its protocol.

        """
        stages = tuple(
            stage for stage in options.processing_stages if stage is not context_stage
        )
        observers = tuple(
            observer
            for observer in options.observers
            if observer is not capture and observer is not errors
        )
        if enabled:
            stages += (context_stage,)
            observers += (capture,)
            if errors is not capture:
                observers += (errors,)
        return m.StructlogOptions(
            log_level=options.log_level,
            console_renderer=options.console_renderer,
            processing_stages=stages,
            observers=observers,
            handlers=options.handlers,
            redacted_keys=options.redacted_keys,
            redacted_values=options.redacted_values,
            wrapper_class_factory=options.wrapper_class_factory,
            logger_factory=options.logger_factory,
            cache_logger_on_first_use=options.cache_logger_on_first_use,
            async_logging=options.async_logging,
        )

    class Performance:
        """Performance tracking helpers."""

        @staticmethod
        def calculate_duration(start_ns: int, end_ns: int) -> p.Result[float]:
            """Calculate duration in seconds from nanosecond timestamps.

            Returns:
                The resulting ``p.Result[float]``.

            """
            if end_ns < start_ns:
                return r[float].fail("end_ns must be >= start_ns")
            return r[float].ok((end_ns - start_ns) / 1000000000)

    class Sampling:
        """Sampling strategy helpers."""

        @staticmethod
        def should_sample(rate: float, request_id: int) -> bool:
            """Determine if a request should be sampled based on rate.

            Returns:
                The resulting ``bool``.

            """
            if rate <= 0.0:
                return False
            if rate >= 1.0:
                return True
            return request_id % 100 < int(rate * 100)


__all__: list[str] = ["FlextObservabilityUtilitiesDomains"]
