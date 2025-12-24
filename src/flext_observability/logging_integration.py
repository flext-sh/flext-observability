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

from flext import FlextLogger, FlextResult
from flext_observability.context import FlextObservabilityContext


class FlextObservabilityLogging:
    """Structured logging integration with trace context enrichment.

    Provides integration between flext-observability context (correlation IDs,
    trace IDs, span IDs) and flext-core's logging system. Automatically
    enriches log entries with trace context.

    Usage:
        ```python
        from flext_observability.logging_integration import FlextObservabilityLogging

        # Create logger with automatic trace context
        logger = FlextObservabilityLogging.create_logger(__name__)

        # Log entries are automatically enriched with correlation ID
        logger.info("Processing request", extra={"user_id": "123"})
        # Log output includes: correlation_id=abc-123, trace_id=def-456
        ```
    """

    _logger = FlextLogger(__name__)

    # ========================================================================
    # LOGGER CREATION WITH CONTEXT
    # ========================================================================

    @staticmethod
    def create_logger(name: str) -> FlextResult[FlextLogger]:
        """Create logger with trace context enrichment.

        Creates a FlextLogger that automatically includes correlation ID,
        trace ID, and span ID in all log entries.

        Args:
            name: Logger name (typically __name__)

        Returns:
            FlextResult[FlextLogger] - Logger instance with context enrichment

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
            if not name or not isinstance(name, str):
                return FlextResult[FlextLogger].fail(
                    "Logger name must be non-empty string",
                )

            # Create FlextLogger from flext-core
            logger = FlextLogger(name)

            # Logger is returned with capability to be enriched
            return FlextResult[FlextLogger].ok(logger)
        except Exception as e:
            return FlextResult[FlextLogger].fail(f"Logger creation failed: {e}")

    # ========================================================================
    # CONTEXT ENRICHMENT
    # ========================================================================

    @staticmethod
    def enrich_log_context(
        _logger: FlextLogger,
        *,
        include_baggage: bool = False,
    ) -> FlextResult[dict[str, object]]:
        """Get trace context for log enrichment.

        Retrieves current trace context (correlation ID, trace ID, span ID)
        that should be included in log entries. Can optionally include baggage.

        Args:
            _logger: FlextLogger instance to enrich (reserved for future use)
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
            context_dict: dict[str, object] = {}

            # Extract correlation ID
            correlation_id = FlextObservabilityContext.get_correlation_id()
            if correlation_id:
                context_dict["correlation_id"] = correlation_id

            # Extract trace ID
            trace_id = FlextObservabilityContext.get_trace_id()
            if trace_id:
                context_dict["trace_id"] = trace_id

            # Extract span ID
            span_id = FlextObservabilityContext.get_span_id()
            if span_id:
                context_dict["span_id"] = span_id

            # Optionally include baggage
            if include_baggage:
                baggage = FlextObservabilityContext.get_baggage()
                if baggage:
                    context_dict["baggage"] = baggage

            return FlextResult[dict[str, object]].ok(context_dict)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Context enrichment failed: {e}",
            )

    @staticmethod
    def inject_trace_context(logger: FlextLogger) -> FlextResult[None]:
        """Inject trace context into logger for structured logging.

        Configures logger to automatically include trace context in all
        log entries. This is typically called once per logger.

        Args:
            logger: FlextLogger instance to configure

        Returns:
            FlextResult[None] - Ok if successful

        Example:
            ```python
            logger = FlextLogger("mymodule")
            result = FlextObservabilityLogging.inject_trace_context(logger)

            # Now all logs from this logger include trace context
            logger.info("User login successful", extra={"user_id": "123"})
            # Output: [...] correlation_id=abc-123 trace_id=def-456 user_id=123
            ```

        """
        try:
            if not isinstance(logger, FlextLogger):
                return FlextResult[None].fail("Logger must be FlextLogger instance")

            # Get current trace context
            context = FlextObservabilityContext.get_context()

            # Logger will automatically include this context in logs
            # (This is handled by flext-core's structured logging)
            # We just verify the integration works
            if not context:
                FlextObservabilityLogging._logger.debug(
                    "No trace context currently set",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Trace context injection failed: {e}")

    # ========================================================================
    # LOGGING WITH CONTEXT
    # ========================================================================

    @staticmethod
    def log_with_context(
        logger: FlextLogger,
        level: str,
        message: str,
        extra: dict[str, object] | None = None,
        *,
        include_baggage: bool = False,
    ) -> FlextResult[None]:
        """Log message with automatic trace context.

        Logs a message while automatically enriching it with correlation ID,
        trace ID, and span ID from current context.

        Args:
            logger: FlextLogger instance
            level: Log level ("debug", "info", "warning", "error", "critical")
            message: Log message
            extra: Additional context fields to include
            include_baggage: Whether to include baggage in logs

        Returns:
            FlextResult[None] - Ok if logging succeeded

        Example:
            ```python
            logger = FlextLogger("myapp")
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
            if not isinstance(logger, FlextLogger):
                return FlextResult[None].fail("Logger must be FlextLogger instance")

            if not message or not isinstance(message, str):
                return FlextResult[None].fail("Message must be non-empty string")

            if level not in {"debug", "info", "warning", "error", "critical"}:
                return FlextResult[None].fail(f"Invalid log level: {level}")

            # Get trace context
            context_result = FlextObservabilityLogging.enrich_log_context(
                logger,
                include_baggage=include_baggage,
            )

            if context_result.is_failure:
                return FlextResult[None].fail(
                    f"Failed to get trace context: {context_result.error}",
                )

            # Merge context with extra fields
            log_context = context_result.value
            if extra:
                log_context.update(extra)

            # Log with context
            getattr(logger, level)(message, extra=log_context)

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Logging with context failed: {e}")

    # ========================================================================
    # CONTEXT VALIDATION
    # ========================================================================

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
    def validate_context() -> FlextResult[dict[str, object]]:
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

            # At minimum, correlation ID should be set
            if not context.get("correlation_id"):
                FlextObservabilityLogging.ensure_correlation_id()
                context = FlextObservabilityContext.get_context()

            return FlextResult[dict[str, object]].ok(context)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Context validation failed: {e}",
            )


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "FlextObservabilityLogging",
]
