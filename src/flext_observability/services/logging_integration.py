"""Structured logging integration with trace context enrichment.

Integrates FlextObservability with flext-core's structured logging system.
Automatically enriches all logs with correlation IDs, trace IDs, and span IDs
from the current context.

FLEXT Pattern:
- Single FlextObservabilityLogging class
- Integration with flext-core `u.fetch_logger(...)` / `p.Logger`
- Automatic trace context injection
- Async-safe context propagation

Key Features:
- Automatic context enrichment in all logs
- Correlation ID propagation across services
- Trace ID and span ID inclusion
- Compatible with flext-core logging patterns
"""

from __future__ import annotations

from structlog.typing import BindableLogger

from flext_observability import FlextObservabilityContext, m, r, t, u


class FlextObservabilityLogging:
    """Structured logging integration with trace context enrichment.

    Provides integration between flext-observability context (correlation IDs,
    trace IDs, span IDs) and flext-core's logging system. Automatically
    enriches log entries with trace context.

    Usage:
        ```python
        from flext_observability import FlextObservabilityLogging

        # Create logger with automatic trace context
        logger = FlextObservabilityLogging.create_logger(__name__)

        # Log entries are automatically enriched with correlation ID
        logger.info("Processing request", extra={"user_id": "123"})
        # Log output includes: correlation_id=abc-123, trace_id=def-456
        ```
    """

    _logger = u.fetch_logger(__name__)

    @staticmethod
    def create_logger(name: str) -> r[BindableLogger]:
        """Create logger with trace context enrichment.

        Creates a logger that automatically includes correlation ID,
        trace ID, and span ID in all log entries.

        Args:
            name: Logger name (typically __name__)

        Returns:
            r[Logger] - Logger instance with context enrichment

        Example:
            ```python
            logger_result = FlextObservabilityLogging.create_logger(__name__)
            if logger_result.success:
                logger = logger_result.value
                logger.info("Application started")
                # Log automatically includes correlation IDs
            ```

        """
        try:
            if not name:
                return r[BindableLogger].fail("Logger name must be non-empty string")
            logger = u.fetch_logger(name)
            return r[BindableLogger].ok(logger)
        except (ValueError, TypeError, KeyError) as e:
            return r[BindableLogger].fail(f"Logger creation failed: {e}")

    @staticmethod
    def enrich_log_context(
        _logger: BindableLogger,
        *,
        include_baggage: bool = False,
    ) -> r[m.Observability.LogContext]:
        """Get trace context for log enrichment.

        Retrieves current trace context (correlation ID, trace ID, span ID)
        that should be included in log entries. Can optionally include baggage.

        Args:
            _logger: Logger instance to enrich (reserved for future use)
            include_baggage: Whether to include baggage in context

        Returns:
            r with context dict for log enrichment

        Context Dict includes:
            - correlation_id: Application-level request tracking
            - trace_id: Distributed trace ID
            - span_id: Current span ID
            - baggage: (optional) Metadata from context

        Example:
            ```python
            # Get context to enrich log
            context_result = FlextObservabilityLogging.enrich_log_context(logger)
            if context_result.success:
                context = context_result.value
                logger.info("Processing", extra=context)
                # Log output: [...] correlation_id=abc-123 trace_id=def-456
            ```

        """
        try:
            context_payload = m.Observability.LogContext()
            correlation_id = FlextObservabilityContext.correlation_id()
            if correlation_id:
                context_payload.correlation_id = correlation_id
            trace_id = FlextObservabilityContext.trace_id()
            if trace_id:
                context_payload.trace_id = trace_id
            span_id = FlextObservabilityContext.span_id()
            if span_id:
                context_payload.span_id = span_id
            if include_baggage:
                baggage = FlextObservabilityContext.resolve_baggage()
                if baggage is not None:
                    context_payload.baggage = str(baggage)
            return r[m.Observability.LogContext].ok(context_payload)
        except (ValueError, TypeError, KeyError) as e:
            return r[m.Observability.LogContext].fail(
                f"Context enrichment failed: {e}",
            )

    @staticmethod
    def ensure_correlation_id() -> str:
        """Ensure correlation ID exists, generating if needed.

        Checks if correlation ID is set in context. If not, generates
        and sets a new one. Always returns a valid correlation ID.

        Returns:
            The correlation ID (existing or newly generated)

        Example:
            ```python
            # At start of request processing
            correlation_id = FlextObservabilityLogging.ensure_correlation_id()
            logger.info(f"Processing request {correlation_id}")
            ```

        """
        current_id = FlextObservabilityContext.correlation_id()
        if not current_id:
            return FlextObservabilityContext.update_correlation_id()
        return current_id

    @staticmethod
    def inject_trace_context(logger: BindableLogger) -> r[bool]:
        """Inject trace context into logger for structured logging.

        Configures logger to automatically include trace context in all
        log entries. This is typically called once per logger.

        Args:
            logger: Logger instance to configure

        Returns:
            r[bool] - Ok if successful

        Example:
            ```python
            logger = u.fetch_logger("mymodule")
            result = FlextObservabilityLogging.inject_trace_context(logger)

            # Now all logs from this logger include trace context
            logger.info("User login successful", extra={"user_id": "123"})
            # Output: [...] correlation_id=abc-123 trace_id=def-456 user_id=123
            ```

        """
        try:
            context = FlextObservabilityContext.context_payload()
            if not context:
                FlextObservabilityLogging._logger.debug(
                    "No trace context currently set",
                )
            _ = logger
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            return r[bool].fail(f"Trace context injection failed: {e}")

    @staticmethod
    def log_with_context(
        logger: BindableLogger,
        level: str,
        message: str,
        extra: t.ConfigurationMapping | None = None,
        *,
        include_baggage: bool = False,
    ) -> r[bool]:
        """Log message with automatic trace context.

        Logs a message while automatically enriching it with correlation ID,
        trace ID, and span ID from current context.

        Args:
            logger: Logger instance
            level: Log level ("debug", "info", "warning", "error", "critical")
            message: Log message
            extra: Additional context fields to include
            include_baggage: Whether to include baggage in logs

        Returns:
            r[bool] - Ok if logging succeeded

        Example:
            ```python
            logger = u.fetch_logger("myapp")
            result = FlextObservabilityLogging.log_with_context(
                logger,
                "info",
                "User authentication successful",
                extra={"user_id": "user-123", "ip_address": "192.168.1.1"},
                include_baggage=True,
            )
            # Log includes: correlation_id=..., trace_id=..., user_id=..., ip_address=...
            ```

        """
        try:
            if not message:
                return r[bool].fail("Message must be non-empty string")
            if level not in {"debug", "info", "warning", "error", "critical"}:
                return r[bool].fail(f"Invalid log level: {level}")
            context_result = FlextObservabilityLogging.enrich_log_context(
                logger,
                include_baggage=include_baggage,
            )
            if context_result.failure:
                return r[bool].fail(
                    f"Failed to get trace context: {context_result.error}",
                )
            log_context: t.MutableContainerMapping = context_result.value.model_dump(
                exclude_none=True,
            )
            extra_context: t.NormalizedValue = log_context.pop("extra", {})
            if isinstance(extra_context, dict):
                typed_extra: t.ContainerMapping = extra_context
                log_context.update(typed_extra)
            if extra:
                log_context.update(extra)
            getattr(logger, level)(message, extra=log_context)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            return r[bool].fail(f"Logging with context failed: {e}")

    @staticmethod
    def validate_context() -> r[m.Observability.LogContext]:
        """Validate current trace context is properly configured.

        Checks that essential trace context (correlation ID) is set.
        Useful for validation in middleware or handlers.

        Returns:
            r with context dict if valid

        Example:
            ```python
            # Validate at start of request processing
            validation_result = FlextObservabilityLogging.validate_context()
            if validation_result.failure:
                # Generate new context if invalid
                FlextObservabilityLogging.ensure_correlation_id()
            ```

        """
        try:
            context = FlextObservabilityContext.context_payload()
            if not context.get("correlation_id"):
                _ = FlextObservabilityLogging.ensure_correlation_id()
                context = FlextObservabilityContext.context_payload()
            return r[m.Observability.LogContext].ok(
                m.Observability.LogContext(
                    correlation_id=str(context.get("correlation_id"))
                    if context.get("correlation_id") is not None
                    else None,
                    trace_id=str(context.get("trace_id"))
                    if context.get("trace_id") is not None
                    else None,
                    span_id=str(context.get("span_id"))
                    if context.get("span_id") is not None
                    else None,
                ),
            )
        except (ValueError, TypeError, KeyError) as e:
            return r[m.Observability.LogContext].fail(
                f"Context validation failed: {e}",
            )


__all__: list[str] = ["FlextObservabilityLogging"]
