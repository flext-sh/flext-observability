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

from contextvars import ContextVar
from uuid import uuid4

from flext_core import u

from flext_observability import c, m, p, r, t


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
        from flext_observability import FlextObservabilityContext

        # Set correlation ID for request
        correlation_id = FlextObservabilityContext.update_correlation_id()

        # Get current correlation ID (available in nested async calls)
        current_id = FlextObservabilityContext.correlation_id()

        # Extract/set from HTTP headers
        FlextObservabilityContext.from_headers(dict(request.headers))

        # Get headers for outbound requests
        headers = FlextObservabilityContext.to_headers()
        ```

    """

    _correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
    _trace_id: ContextVar[str] = ContextVar("trace_id", default="")
    _span_id: ContextVar[str] = ContextVar("span_id", default="")
    _baggage: ContextVar[m.Dict | None] = ContextVar("baggage", default=None)
    _logger = u.fetch_logger(__name__)

    @staticmethod
    def clear_baggage() -> None:
        """Clear all baggage from context."""
        FlextObservabilityContext._baggage.set(m.Dict({}))

    @staticmethod
    def clear_context() -> None:
        """Clear all context variables.

        Clears correlation ID, trace ID, span ID, and baggage.
        Use at end of request processing to prevent context leak.

        Example:
            ```python
            try:
                # Process request with context
                FlextObservabilityContext.update_correlation_id()
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

    @staticmethod
    def clear_correlation_id() -> None:
        """Clear correlation ID from context.

        Removes correlation ID from context variables. Use at end of
        request processing to prevent context leak.
        """
        FlextObservabilityContext._correlation_id.set("")

    @staticmethod
    def clear_span_id() -> None:
        """Clear span ID from context."""
        FlextObservabilityContext._span_id.set("")

    @staticmethod
    def clear_trace_id() -> None:
        """Clear trace ID from context."""
        FlextObservabilityContext._trace_id.set("")

    @staticmethod
    def from_headers(headers: m.Dict | t.ScalarMapping) -> p.Result[bool]:
        """Set context from HTTP headers.

        Extracts correlation ID, trace ID, and span ID from incoming
        HTTP headers. Supports both lowercase and capitalized header names.

        Args:
            headers: HTTP request headers dict

        Returns:
            r[bool] - Always Ok, generates IDs if not found

        Example:
            ```python
            # Extract context from incoming request
            from flext_observability import FlextObservabilityContext

            FlextObservabilityContext.from_headers(dict(request.headers))

            # Now context is available in nested calls
            correlation_id = FlextObservabilityContext.correlation_id()
            ```

        """
        try:
            normalized_headers = {
                header_key.lower(): str(header_value)
                for header_key, header_value in headers.items()
            }
            correlation_id = normalized_headers.get("x-correlation-id") or str(uuid4())
            FlextObservabilityContext.update_correlation_id(correlation_id)
            if trace_id := normalized_headers.get("x-trace-id"):
                FlextObservabilityContext.update_trace_id(trace_id)
            if span_id := normalized_headers.get("x-span-id"):
                FlextObservabilityContext.update_span_id(span_id)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            FlextObservabilityContext._logger.warning(
                f"Failed to extract context from headers: {e}",
            )
            FlextObservabilityContext.update_correlation_id()
            return r[bool].ok(value=True)

    @staticmethod
    def resolve_baggage(
        key: str | None = None,
    ) -> m.BaseModel | t.JsonValue | m.Dict | None:
        """Resolve baggage value.

        Args:
            key: Optional specific baggage key. If None, returns all baggage.

        Returns:
            Baggage value, all baggage dict, or None if not found.

        Example:
            ```python
            # Get all baggage
            baggage = FlextObservabilityContext.resolve_baggage()

            # Get specific value
            user_id = FlextObservabilityContext.resolve_baggage("user_id")
            ```

        """
        baggage = FlextObservabilityContext._baggage.get() or {}
        if key is None:
            return baggage
        return baggage.get(key)

    @staticmethod
    def context_payload() -> m.Dict:
        """Return complete context snapshot.

        Returns all context variables as a dictionary. Useful for
        debugging and context propagation.

        Returns:
            Dict with all context variables

        Example:
            ```python
            context = FlextObservabilityContext.context_payload()
            logger.debug(f"Current context: {context}")
            # Output: {
            #   "correlation_id": "abc-123",
            #   "trace_id": "def-456",
            #   "span_id": "ghi-789",
            #   "baggage": {"user_id": "user-123"}
            # }
            ```

        """
        return m.Dict({
            "correlation_id": FlextObservabilityContext.correlation_id(),
            "trace_id": FlextObservabilityContext.trace_id(),
            "span_id": FlextObservabilityContext.span_id(),
            "baggage": FlextObservabilityContext.resolve_baggage(),
        })

    @staticmethod
    def correlation_id() -> str:
        """Return current correlation ID.

        Returns the correlation ID for current request/operation context.
        If no correlation ID is set, returns empty string.

        Returns:
            Current correlation ID or empty string if not set.

        Example:
            ```python
            correlation_id = FlextObservabilityContext.correlation_id()
            logger.info(f"Processing request {correlation_id}")
            ```

        """
        return FlextObservabilityContext._correlation_id.get("")

    @staticmethod
    def span_id() -> str:
        """Return current span ID."""
        return FlextObservabilityContext._span_id.get("")

    @staticmethod
    def trace_id() -> str:
        """Return current trace ID."""
        return FlextObservabilityContext._trace_id.get("")

    @staticmethod
    def update_baggage(key: str, value: t.JsonValue) -> p.Result[bool]:
        """Update baggage value for metadata propagation.

        Baggage allows passing metadata across service boundaries
        without including it in every operation parameter.

        Args:
            key: Baggage key
            value: Baggage value (must be serializable)

        Returns:
            r[bool] - Ok if successful, Fail if validation error

        Example:
            ```python
            # Set user context
            FlextObservabilityContext.update_baggage("user_id", "user-123")
            FlextObservabilityContext.update_baggage("tenant", "acme-corp")

            # Values automatically propagated to nested operations
            ```

        """
        try:
            try:
                m.Observability.BaggageKeyModel.model_validate(obj={"key": key})
            except c.ValidationError:
                return r[bool].fail("Baggage key must be non-empty string")
            current_baggage = FlextObservabilityContext._baggage.get() or {}
            updated_baggage = m.Dict({
                **dict(current_baggage.items()),
                key: value,
            })
            FlextObservabilityContext._baggage.set(updated_baggage)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError) as e:
            return r[bool].fail(f"Baggage set failed: {e}")

    @staticmethod
    def update_correlation_id(correlation_id: str | None = None) -> str:
        """Update correlation ID for request tracking.

        Sets or generates correlation ID that will be propagated to all
        nested operations and across async boundaries.

        Args:
            correlation_id: Optional correlation ID. If None, generates UUID4.

        Returns:
            The correlation ID that was set.

        Example:
            ```python
            # Auto-generate correlation ID
            correlation_id = FlextObservabilityContext.update_correlation_id()

            # Set specific correlation ID
            FlextObservabilityContext.update_correlation_id("user-123-request-456")
            ```

        """
        if correlation_id is None:
            correlation_id = str(uuid4())
        FlextObservabilityContext._correlation_id.set(correlation_id)
        return correlation_id

    @staticmethod
    def update_span_id(span_id: str | None = None) -> str:
        """Update current span ID."""
        if span_id is None:
            span_id = str(uuid4())
        FlextObservabilityContext._span_id.set(span_id)
        return span_id

    @staticmethod
    def update_trace_id(trace_id: str | None = None) -> str:
        """Update trace ID for distributed tracing.

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
    def to_headers() -> m.Dict:
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
        headers = {}
        correlation_id = FlextObservabilityContext.correlation_id()
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id
        trace_id = FlextObservabilityContext.trace_id()
        if trace_id:
            headers["X-Trace-ID"] = trace_id
        span_id = FlextObservabilityContext.span_id()
        if span_id:
            headers["X-Span-ID"] = span_id
        return m.Dict(headers)


__all__: list[str] = ["FlextObservabilityContext"]
