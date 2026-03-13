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

from collections.abc import Mapping

from flext_core import FlextLogger, r, t
from pydantic import BaseModel, Field, TypeAdapter


class ContextSnapshot(BaseModel):
    """Snapshot of observability context for restoration in async operations."""

    correlation_id: str = Field(default="")
    trace_id: str = Field(default="")
    span_id: str = Field(default="")
    baggage: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, t.Scalar] = Field(default_factory=dict)


class FlextObservabilityAdvancedContext:
    """Advanced context management for rich metadata propagation.

    Extends basic context with request-local storage and baggage support.

    Usage:
        ```python
        from flext_observability import FlextObservabilityAdvancedContext

        ctx = FlextObservabilityAdvancedContext.get_context()

        # Store request-local data
        ctx.set_metadata("user_id", "user-123")
        ctx.set_metadata("api_key", "secret-key")

        # Get context snapshot
        snapshot = ctx.snapshot()

        # Restore context
        ctx.restore(snapshot)
        ```

    Nested Classes:
        Context: Request-local context management
    """

    _logger = FlextLogger.get_logger(__name__)
    _context_instance: FlextObservabilityAdvancedContext.Context | None = None

    class Context:
        """Request-local context for storing metadata."""

        def __init__(self) -> None:
            """Initialize advanced context."""
            self._metadata: dict[str, t.Scalar] = {}
            self._baggage: dict[str, str] = {}
            self._request_id: str = ""
            self._parent_context: ContextSnapshot | None = None

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

        def get_all_baggage(self) -> Mapping[str, str]:
            """Get all baggage items.

            Returns:
                dict - All baggage

            """
            return self._baggage.copy()

        def get_all_metadata(self) -> Mapping[str, t.Scalar]:
            """Get all request-local metadata.

            Returns:
                dict - All metadata

            """
            return self._metadata.copy()

        def get_baggage(self, key: str) -> str | None:
            """Get baggage item.

            Args:
                key: Baggage key

            Returns:
                str - Baggage value or None

            """
            return self._baggage.get(key)

        def get_metadata(self, key: str) -> t.Scalar | None:
            """Get request-local metadata.

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
                self._metadata.update(other.get_all_metadata())
                self._baggage.update(other.get_all_baggage())
                FlextObservabilityAdvancedContext._logger.debug("Context merged")
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to merge context: {e}")

        def restore(self, snapshot: ContextSnapshot) -> r[bool]:
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
                self._metadata = snapshot.metadata.copy()
                self._baggage = snapshot.baggage.copy()
                FlextObservabilityAdvancedContext._logger.debug(
                    "Context restored from snapshot"
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Failed to restore context: {e}")

        def set_baggage(self, key: str, value: str) -> r[bool]:
            """Set baggage item (W3C Baggage API).

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

        def set_metadata(self, key: str, value: t.Scalar) -> r[bool]:
            """Set request-local metadata.

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
                TypeAdapter(t.Scalar).validate_python(value)
                self._metadata[key] = value
                FlextObservabilityAdvancedContext._logger.debug(f"Metadata set: {key}")
                return r[bool].ok(value=True)
            except (TypeError, ValueError) as e:
                return r[bool].fail(f"Metadata value not JSON serializable: {e}")

        def snapshot(
            self, correlation_id: str = "", trace_id: str = "", span_id: str = ""
        ) -> ContextSnapshot:
            """Create snapshot of current context.

            Args:
                correlation_id: Correlation ID (from Phase 3)
                trace_id: Trace ID (from Phase 3)
                span_id: Span ID (from Phase 3)

            Returns:
                ContextSnapshot - Context snapshot for later restoration

            """
            return ContextSnapshot(
                correlation_id=correlation_id,
                trace_id=trace_id,
                span_id=span_id,
                baggage=dict(self.get_all_baggage()),
                metadata=dict(self.get_all_metadata()),
            )

    @staticmethod
    def get_context() -> FlextObservabilityAdvancedContext.Context:
        """Get global advanced context instance (singleton).

        Returns:
            Context - Global advanced context

        """
        if FlextObservabilityAdvancedContext._context_instance is None:
            FlextObservabilityAdvancedContext._context_instance = (
                FlextObservabilityAdvancedContext.Context()
            )
        return FlextObservabilityAdvancedContext._context_instance

    @staticmethod
    def get_metadata(key: str) -> t.Scalar | None:
        """Convenience function: get metadata.

        Args:
            key: Metadata key

        Returns:
            JSONValue - Metadata value or None

        """
        ctx = FlextObservabilityAdvancedContext.get_context()
        return ctx.get_metadata(key)

    @staticmethod
    def set_metadata(key: str, value: t.Scalar) -> r[bool]:
        """Convenience function: set metadata.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            r[bool] - Ok if successful

        """
        ctx = FlextObservabilityAdvancedContext.get_context()
        return ctx.set_metadata(key, value)


__all__ = ["ContextSnapshot", "FlextObservabilityAdvancedContext"]
