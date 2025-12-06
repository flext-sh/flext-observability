"""Async-safe context management for distributed tracing correlation.

Provides context variable management for correlation IDs, trace IDs, and span IDs
that are safe across async boundaries. Uses contextvars for proper async context
propagation throughout the FLEXT ecosystem.

FLEXT Pattern:
- Single FlextObservabilityContext class
- Nested subclasses for correlation and baggage management
- Async-safe using Python's contextvars module
- Integration with trace context propagation (W3C Trace Context)
"""

from __future__ import annotations

import json
from contextvars import ContextVar
from uuid import uuid4

from flext_core import FlextLogger, FlextResult


class FlextObservabilityContext:
    """Async-safe context management for distributed tracing.

    Manages context variables for correlation IDs, trace IDs, and span IDs
    that are properly propagated across async boundaries. Integrates with
    HTTP middleware for trace context propagation.

    Uses Python's contextvars module for async-safe context management:
    - Correlation IDs (application-level request tracking)
    - Trace IDs (OpenTelemetry distributed tracing)
    - Span IDs (individual span tracking)
    - Baggage (metadata propagation)

    Example:
        ```python
        from flext_observability.context import FlextObservabilityContext

        # Set correlation ID for request
        correlation_id = FlextObservabilityContext.set_correlation_id()

        # Get current correlation ID (available in nested async calls)
        current_id = FlextObservabilityContext.get_correlation_id()

        # Extract/set from HTTP headers
        FlextObservabilityContext.from_headers(dict(request.headers))

        # Get headers for outbound requests
        headers = FlextObservabilityContext.to_headers()
        ```

    """

    # ========================================================================
    # CONTEXT VARIABLES - Async-safe storage
    # ========================================================================

    _correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
    _trace_id: ContextVar[str] = ContextVar("trace_id", default="")
    _span_id: ContextVar[str] = ContextVar("span_id", default="")
    _baggage: ContextVar[dict[str, object] | None] = ContextVar("baggage", default=None)

    _logger = FlextLogger(__name__)

    # ========================================================================
    # CORRELATION ID MANAGEMENT
    # ========================================================================

    @staticmethod
    def set_correlation_id(correlation_id: str | None = None) -> str:
        """Set correlation ID for request tracking.

        Sets or generates correlation ID that will be propagated to all
        nested operations and across async boundaries.

        Args:
            correlation_id: Optional correlation ID. If None, generates UUID4.

        Returns:
            The correlation ID that was set.

        Example:
            ```python
            # Auto-generate correlation ID
            correlation_id = FlextObservabilityContext.set_correlation_id()

            # Set specific correlation ID
            FlextObservabilityContext.set_correlation_id("user-123-request-456")
            ```

        """
        if correlation_id is None:
            correlation_id = str(uuid4())

        FlextObservabilityContext._correlation_id.set(correlation_id)
        return correlation_id

    @staticmethod
    def get_correlation_id() -> str:
        """Get current correlation ID.

        Returns the correlation ID for current request/operation context.
        If no correlation ID is set, returns empty string.

        Returns:
            Current correlation ID or empty string if not set.

        Example:
            ```python
            correlation_id = FlextObservabilityContext.get_correlation_id()
            logger.info(f"Processing request {correlation_id}")
            ```

        """
        return FlextObservabilityContext._correlation_id.get("")

    @staticmethod
    def clear_correlation_id() -> None:
        """Clear correlation ID from context.

        Removes correlation ID from context variables. Use at end of
        request processing to prevent context leak.
        """
        FlextObservabilityContext._correlation_id.set("")

    # ========================================================================
    # TRACE ID MANAGEMENT
    # ========================================================================

    @staticmethod
    def set_trace_id(trace_id: str | None = None) -> str:
        """Set trace ID for distributed tracing.

        Sets OpenTelemetry trace ID for span correlation across services.
        If None, generates UUID4.

        Args:
            trace_id: Optional OpenTelemetry trace ID.

        Returns:
            The trace ID that was set.

        """
        if trace_id is None:
            trace_id = str(uuid4())

        FlextObservabilityContext._trace_id.set(trace_id)
        return trace_id

    @staticmethod
    def get_trace_id() -> str:
        """Get current trace ID."""
        return FlextObservabilityContext._trace_id.get("")

    @staticmethod
    def clear_trace_id() -> None:
        """Clear trace ID from context."""
        FlextObservabilityContext._trace_id.set("")

    # ========================================================================
    # SPAN ID MANAGEMENT
    # ========================================================================

    @staticmethod
    def set_span_id(span_id: str | None = None) -> str:
        """Set current span ID."""
        if span_id is None:
            span_id = str(uuid4())

        FlextObservabilityContext._span_id.set(span_id)
        return span_id

    @staticmethod
    def get_span_id() -> str:
        """Get current span ID."""
        return FlextObservabilityContext._span_id.get("")

    @staticmethod
    def clear_span_id() -> None:
        """Clear span ID from context."""
        FlextObservabilityContext._span_id.set("")

    # ========================================================================
    # BAGGAGE MANAGEMENT - Metadata propagation
    # ========================================================================

    @staticmethod
    def set_baggage(key: str, value: object) -> FlextResult[None]:
        """Set baggage value for metadata propagation.

        Baggage allows passing metadata across service boundaries
        without including it in every operation parameter.

        Args:
            key: Baggage key
            value: Baggage value (must be serializable)

        Returns:
            FlextResult[None] - Ok if successful, Fail if validation error

        Example:
            ```python
            # Set user context
            FlextObservabilityContext.set_baggage("user_id", "user-123")
            FlextObservabilityContext.set_baggage("tenant", "acme-corp")

            # Values automatically propagated to nested operations
            ```

        """
        try:
            if not isinstance(key, str) or not key:
                return FlextResult[None].fail("Baggage key must be non-empty string")

            # Validate value is serializable
            try:
                json.dumps(value)
            except (TypeError, ValueError):
                return FlextResult[None].fail(
                    f"Baggage value for '{key}' must be JSON serializable",
                )

            # Get current baggage and update
            current_baggage = FlextObservabilityContext._baggage.get({}) or {}
            updated_baggage = {**current_baggage, key: value}
            FlextObservabilityContext._baggage.set(updated_baggage)

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Baggage set failed: {e}")

    @staticmethod
    def get_baggage(key: str | None = None) -> object:
        """Get baggage value.

        Args:
            key: Optional specific baggage key. If None, returns all baggage.

        Returns:
            Baggage value, all baggage dict, or None if not found.

        Example:
            ```python
            # Get all baggage
            baggage = FlextObservabilityContext.get_baggage()

            # Get specific value
            user_id = FlextObservabilityContext.get_baggage("user_id")
            ```

        """
        baggage = FlextObservabilityContext._baggage.get({}) or {}

        if key is None:
            return baggage

        return baggage.get(key)

    @staticmethod
    def clear_baggage() -> None:
        """Clear all baggage from context."""
        FlextObservabilityContext._baggage.set({})

    # ========================================================================
    # HTTP HEADER MANAGEMENT - W3C Trace Context
    # ========================================================================

    @staticmethod
    def to_headers() -> dict[str, str]:
        """Get context as HTTP headers.

        Converts current context (correlation ID, trace ID, span ID) to
        HTTP headers for propagation to downstream services. Follows
        W3C Trace Context standard.

        Returns:
            Dict of headers for HTTP requests

        Standard Headers:
            - X-Correlation-ID: Application-level correlation (custom)
            - X-Trace-ID: OpenTelemetry trace ID (custom)
            - X-Span-ID: OpenTelemetry span ID (custom)
            - traceparent: W3C Trace Context format (todo: Phase 4)

        Example:
            ```python
            # Get headers for outbound request
            headers = FlextObservabilityContext.to_headers()
            response = httpx.get("http://api.example.com/users", headers=headers)

            # Headers automatically include current correlation/trace IDs
            ```

        """
        headers: dict[str, str] = {}

        correlation_id = FlextObservabilityContext.get_correlation_id()
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id

        trace_id = FlextObservabilityContext.get_trace_id()
        if trace_id:
            headers["X-Trace-ID"] = trace_id

        span_id = FlextObservabilityContext.get_span_id()
        if span_id:
            headers["X-Span-ID"] = span_id

        return headers

    @staticmethod
    def from_headers(headers: dict[str, str]) -> FlextResult[None]:
        """Set context from HTTP headers.

        Extracts correlation ID, trace ID, and span ID from incoming
        HTTP headers. Supports both lowercase and capitalized header names.

        Args:
            headers: HTTP request headers dict

        Returns:
            FlextResult[None] - Always Ok, generates IDs if not found

        Example:
            ```python
            # Extract context from incoming request
            from flext_observability.context import FlextObservabilityContext

            FlextObservabilityContext.from_headers(dict(request.headers))

            # Now context is available in nested calls
            correlation_id = FlextObservabilityContext.get_correlation_id()
            ```

        """
        try:
            # Normalize header names (case-insensitive)
            normalized_headers = {k.lower(): v for k, v in headers.items()}

            # Extract correlation ID (generate if not found)
            correlation_id = normalized_headers.get("x-correlation-id") or str(uuid4())
            FlextObservabilityContext.set_correlation_id(correlation_id)

            # Extract trace ID if present
            if trace_id := normalized_headers.get("x-trace-id"):
                FlextObservabilityContext.set_trace_id(trace_id)

            # Extract span ID if present
            if span_id := normalized_headers.get("x-span-id"):
                FlextObservabilityContext.set_span_id(span_id)

            return FlextResult[None].ok(None)
        except Exception as e:
            FlextObservabilityContext._logger.warning(
                f"Failed to extract context from headers: {e}",
            )
            # Still return ok - generate new IDs
            FlextObservabilityContext.set_correlation_id()
            return FlextResult[None].ok(None)

    # ========================================================================
    # COMPLETE CONTEXT RETRIEVAL
    # ========================================================================

    @staticmethod
    def get_context() -> dict[str, object]:
        """Get complete context snapshot.

        Returns all context variables as a dictionary. Useful for
        debugging and context propagation.

        Returns:
            Dict with all context variables

        Example:
            ```python
            context = FlextObservabilityContext.get_context()
            logger.debug(f"Current context: {context}")
            # Output: {
            #   "correlation_id": "abc-123",
            #   "trace_id": "def-456",
            #   "span_id": "ghi-789",
            #   "baggage": {"user_id": "user-123"}
            # }
            ```

        """
        return {
            "correlation_id": FlextObservabilityContext.get_correlation_id(),
            "trace_id": FlextObservabilityContext.get_trace_id(),
            "span_id": FlextObservabilityContext.get_span_id(),
            "baggage": FlextObservabilityContext.get_baggage(),
        }

    @staticmethod
    def clear_context() -> None:
        """Clear all context variables.

        Clears correlation ID, trace ID, span ID, and baggage.
        Use at end of request processing to prevent context leak.

        Example:
            ```python
            try:
                # Process request with context
                FlextObservabilityContext.set_correlation_id()
                process_request()
            finally:
                # Always clear at end to prevent leaks
                FlextObservabilityContext.clear_context()
            ```

        """
        FlextObservabilityContext.clear_correlation_id()
        FlextObservabilityContext.clear_trace_id()
        FlextObservabilityContext.clear_span_id()
        FlextObservabilityContext.clear_baggage()


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "FlextObservabilityContext",
]
