"""Advanced context management for rich metadata propagation.

Extends Phase 3 context with advanced features for request-local storage,
baggage propagation, and metadata management.

FLEXT Pattern:
- Single FlextObservabilityAdvancedContext class
- Request-local context storage
- Baggage API integration
- Metadata snapshot/restore

Key Features:
- Request-local storage (separate from async context)
- Rich metadata propagation
- Context snapshots for debugging
- Automatic cleanup
"""

from __future__ import annotations

from flext_observability import m, r, t, u


class FlextObservabilityAdvancedContext:
    """Advanced context management for rich metadata propagation.

    Extends basic context with request-local storage and baggage support.

    Usage:
        ```python
        from flext_observability import (
            FlextObservabilityAdvancedContext,
        )

        ctx = FlextObservabilityAdvancedContext.active_context()

        # Store request-local data
        ctx.update_metadata("user_id", "user-123")
        ctx.update_metadata("api_key", "secret-key")

        # Get context snapshot
        snapshot = ctx.snapshot()

        # Restore context
        ctx.restore(snapshot)
        ```

    Nested Classes:
        Context: Request-local context management
    """

    _logger = u.fetch_logger(__name__)
    _context_instance: FlextObservabilityAdvancedContext.Context | None = None

    class Context:
        """Request-local context for storing metadata."""

        def __init__(self) -> None:
            """Initialize advanced context."""
            self._metadata: t.MutableScalarMapping = {}
            self._baggage: t.MutableStrMapping = {}
            self._request_id: str = ""
            self._parent_context: m.Observability.ContextSnapshot | None = None

        def clear(self) -> r[bool]:
            """Clear all request-local context.

            Returns:
                r[bool] - Ok always

            """
            try:
                self._metadata.clear()
                self._baggage.clear()
                self._request_id = ""
                FlextObservabilityAdvancedContext._logger.debug("Context cleared")
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to clear context: {e}")

        @property
        def baggage(self) -> t.StrMapping:
            """Return all baggage items.

            Returns:
                dict - All baggage

            """
            return dict(self._baggage)

        @property
        def metadata(self) -> t.ConfigurationMapping:
            """Return all request-local metadata.

            Returns:
                dict - All metadata

            """
            return dict(self._metadata)

        def resolve_baggage(self, key: str) -> str | None:
            """Resolve a baggage item.

            Args:
                key: Baggage key

            Returns:
                str - Baggage value or None

            """
            return self._baggage.get(key)

        def resolve_metadata(self, key: str) -> t.Scalar | None:
            """Resolve request-local metadata.

            Args:
                key: Metadata key

            Returns:
                JSONValue - Metadata value or None

            """
            return self._metadata.get(key)

        def merge(self, other: FlextObservabilityAdvancedContext.Context) -> r[bool]:
            """Merge another context into this one.

            Args:
                other: Other context to merge

            Returns:
                r[bool] - Ok if successful

            """
            try:
                self._metadata.update(other.metadata)
                self._baggage.update(other.baggage)
                FlextObservabilityAdvancedContext._logger.debug("Context merged")
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to merge context: {e}")

        def restore(self, snapshot: m.Observability.ContextSnapshot) -> r[bool]:
            """Restore context from snapshot.

            Args:
                snapshot: Context snapshot to restore

            Returns:
                r[bool] - Ok if successful

            Behavior:
                - Restores all metadata and baggage
                - Useful for async callbacks, background tasks

            """
            try:
                self._metadata = dict(snapshot.metadata)
                self._baggage = dict(snapshot.baggage)
                FlextObservabilityAdvancedContext._logger.debug(
                    "Context restored from snapshot",
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to restore context: {e}")

        def update_baggage(self, key: str, value: str) -> r[bool]:
            """Update a baggage item (W3C Baggage API).

            Args:
                key: Baggage key
                value: Baggage value (string)

            Returns:
                r[bool] - Ok if successful

            """
            try:
                self._baggage[key] = value
                FlextObservabilityAdvancedContext._logger.debug(f"Baggage set: {key}")
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to set baggage: {e}")

        def update_metadata(self, key: str, value: t.Scalar) -> r[bool]:
            """Update request-local metadata.

            Args:
                key: Metadata key
                value: Metadata value (must be JSON serializable)

            Returns:
                r[bool] - Ok if successful

            Behavior:
                - Stores in request-local storage
                - Value must be JSON serializable
                - Useful for user IDs, request IDs, etc.

            """
            try:
                t.SCALAR_ADAPTER.validate_python(value)
                self._metadata[key] = value
                FlextObservabilityAdvancedContext._logger.debug(f"Metadata set: {key}")
                return r[bool].ok(value=True)
            except (TypeError, ValueError) as e:
                return r[bool].fail(f"Metadata value not JSON serializable: {e}")

        def snapshot(
            self,
            correlation_id: str = "",
            trace_id: str = "",
            span_id: str = "",
        ) -> m.Observability.ContextSnapshot:
            """Create snapshot of current context.

            Args:
                correlation_id: Correlation ID (from Phase 3)
                trace_id: Trace ID (from Phase 3)
                span_id: Span ID (from Phase 3)

            Returns:
                ContextSnapshot - Context snapshot for later restoration

            """
            return m.Observability.ContextSnapshot(
                correlation_id=correlation_id,
                trace_id=trace_id,
                span_id=span_id,
                baggage=dict(self.baggage),
                metadata=dict(self.metadata),
            )

    @staticmethod
    def active_context() -> FlextObservabilityAdvancedContext.Context:
        """Return the global advanced context instance.

        Returns:
            Context - Global advanced context

        """
        if FlextObservabilityAdvancedContext._context_instance is None:
            FlextObservabilityAdvancedContext._context_instance = (
                FlextObservabilityAdvancedContext.Context()
            )
        return FlextObservabilityAdvancedContext._context_instance

    @staticmethod
    def resolve_metadata(key: str) -> t.Scalar | None:
        """Convenience function: resolve metadata.

        Args:
            key: Metadata key

        Returns:
            JSONValue - Metadata value or None

        """
        ctx = FlextObservabilityAdvancedContext.active_context()
        return ctx.resolve_metadata(key)

    @staticmethod
    def update_metadata(key: str, value: t.Scalar) -> r[bool]:
        """Convenience function: update metadata.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            r[bool] - Ok if successful

        """
        ctx = FlextObservabilityAdvancedContext.active_context()
        return ctx.update_metadata(key, value)


__all__ = ["FlextObservabilityAdvancedContext"]
