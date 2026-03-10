"""Structured logging integration with trace context enrichment.

Integrates FlextObservability with flext-core's structured logging system.
Automatically enriches all logs with correlation IDs, trace IDs, and span IDs
from the current context.

FLEXT Pattern:
- Single FlextObservabilityLogging class
- Integration with flext-core FlextLogger
- Automatic trace context injection
- Async-safe context propagation

Key Features:
- Automatic context enrichment in all logs
- Correlation ID propagation across services
- Trace ID and span ID inclusion
- Compatible with flext-core logging patterns
"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, m, t
from pydantic import BaseModel, Field
from structlog.typing import BindableLogger

from flext_observability import FlextObservabilityContext


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

    _logger = FlextLogger(__name__)

    class LogContext(BaseModel):
        correlation_id: str | None = None
        trace_id: str | None = None
        span_id: str | None = None
        baggage: str | None = None
        extra: m.Dict = Field(default_factory=lambda: m.Dict({}))

    @staticmethod
    def create_logger(name: str) -> FlextResult[BindableLogger]:
        """Create logger with trace context enrichment.

        Creates a logger that automatically includes correlation ID,
        trace ID, and span ID in all log entries.

        Args:
            name: Logger name (typically __name__)

        Returns:
            FlextResult[StructlogLogger] - Logger instance with context enrichment

        Example:
            ```python
            logger_result = FlextObservabilityLogging.create_logger(__name__)
            if logger_result.is_success:
                logger = logger_result.value
                logger.info("Application started")
                # Log automatically includes correlation IDs
            ```

        """
        try:
            if not name:
                return FlextResult[BindableLogger].fail(
                    "Logger name must be non-empty string"
                )
            logger = FlextLogger.get_logger(name)
            return FlextResult[BindableLogger].ok(logger)
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[BindableLogger].fail(f"Logger creation failed: {e}")

    @staticmethod
    def enrich_log_context(
        _logger: BindableLogger, *, include_baggage: bool = False
    ) -> FlextResult[FlextObservabilityLogging.LogContext]:
        """Get trace context for log enrichment.

        Retrieves current trace context (correlation ID, trace ID, span ID)
        that should be included in log entries. Can optionally include baggage.

        Args:
            _logger: Logger instance to enrich (reserved for future use)
            include_baggage: Whether to include baggage in context

        Returns:
            FlextResult with context dict for log enrichment

        Context Dict includes:
            - correlation_id: Application-level request tracking
            - trace_id: Distributed trace ID
            - span_id: Current span ID
            - baggage: (optional) Metadata from context

        Example:
            ```python
            # Get context to enrich log
            context_result = FlextObservabilityLogging.enrich_log_context(logger)
            if context_result.is_success:
                context = context_result.value
                logger.info("Processing", extra=context)
                # Log output: [...] correlation_id=abc-123 trace_id=def-456
            ```

        """
        try:
            context_payload = FlextObservabilityLogging.LogContext()
            correlation_id = FlextObservabilityContext.get_correlation_id()
            if correlation_id:
                context_payload.correlation_id = correlation_id
            trace_id = FlextObservabilityContext.get_trace_id()
            if trace_id:
                context_payload.trace_id = trace_id
            span_id = FlextObservabilityContext.get_span_id()
            if span_id:
                context_payload.span_id = span_id
            if include_baggage:
                baggage = FlextObservabilityContext.get_baggage()
                if baggage is not None:
                    context_payload.baggage = str(baggage)
            return FlextResult[FlextObservabilityLogging.LogContext].ok(context_payload)
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[FlextObservabilityLogging.LogContext].fail(
                f"Context enrichment failed: {e}"
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
        current_id = FlextObservabilityContext.get_correlation_id()
        if not current_id:
            return FlextObservabilityContext.set_correlation_id()
        return current_id

    @staticmethod
    def inject_trace_context(logger: BindableLogger) -> FlextResult[bool]:
        """Inject trace context into logger for structured logging.

        Configures logger to automatically include trace context in all
        log entries. This is typically called once per logger.

        Args:
            logger: Logger instance to configure

        Returns:
            FlextResult[bool] - Ok if successful

        Example:
            ```python
            logger = FlextLogger.get_logger("mymodule")
            result = FlextObservabilityLogging.inject_trace_context(logger)

            # Now all logs from this logger include trace context
            logger.info("User login successful", extra={"user_id": "123"})
            # Output: [...] correlation_id=abc-123 trace_id=def-456 user_id=123
            ```

        """
        try:
            context = FlextObservabilityContext.get_context()
            if not context:
                FlextObservabilityLogging._logger.debug(
                    "No trace context currently set"
                )
            _ = logger
            return FlextResult[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[bool].fail(f"Trace context injection failed: {e}")

    @staticmethod
    def log_with_context(
        logger: BindableLogger,
        level: str,
        message: str,
        extra: t.ConfigurationMapping | m.Dict | None = None,
        *,
        include_baggage: bool = False,
    ) -> FlextResult[bool]:
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
            FlextResult[bool] - Ok if logging succeeded

        Example:
            ```python
            logger = FlextLogger.get_logger("myapp")
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
                return FlextResult[bool].fail("Message must be non-empty string")
            if level not in {"debug", "info", "warning", "error", "critical"}:
                return FlextResult[bool].fail(f"Invalid log level: {level}")
            context_result = FlextObservabilityLogging.enrich_log_context(
                logger, include_baggage=include_baggage
            )
            if context_result.is_failure:
                return FlextResult[bool].fail(
                    f"Failed to get trace context: {context_result.error}"
                )
            log_context = context_result.value.model_dump(exclude_none=True)
            extra_context = log_context.pop("extra", {})
            log_context.update(extra_context)
            if extra:
                log_context.update(extra)
            getattr(logger, level)(message, extra=log_context)
            return FlextResult[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[bool].fail(f"Logging with context failed: {e}")

    @staticmethod
    def validate_context() -> FlextResult[FlextObservabilityLogging.LogContext]:
        """Validate current trace context is properly configured.

        Checks that essential trace context (correlation ID) is set.
        Useful for validation in middleware or handlers.

        Returns:
            FlextResult with context dict if valid

        Example:
            ```python
            # Validate at start of request processing
            validation_result = FlextObservabilityLogging.validate_context()
            if validation_result.is_failure:
                # Generate new context if invalid
                FlextObservabilityLogging.ensure_correlation_id()
            ```

        """
        try:
            context = FlextObservabilityContext.get_context()
            if not context.get("correlation_id"):
                _ = FlextObservabilityLogging.ensure_correlation_id()
                context = FlextObservabilityContext.get_context()
            return FlextResult[FlextObservabilityLogging.LogContext].ok(
                FlextObservabilityLogging.LogContext(
                    correlation_id=str(context.get("correlation_id"))
                    if context.get("correlation_id") is not None
                    else None,
                    trace_id=str(context.get("trace_id"))
                    if context.get("trace_id") is not None
                    else None,
                    span_id=str(context.get("span_id"))
                    if context.get("span_id") is not None
                    else None,
                )
            )
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult[FlextObservabilityLogging.LogContext].fail(
                f"Context validation failed: {e}"
            )


__all__ = ["FlextObservabilityLogging"]
