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

import json
from dataclasses import dataclass, field

from flext_core import FlextLogger, FlextResult

# Type for JSON-serializable values (no Any allowed)
# Using PEP 695 type statement for recursive type (Python 3.12+)
type JSONValue = (
    str | int | float | bool | list[JSONValue] | dict[str, JSONValue] | None
)


@dataclass
class ContextSnapshot:
    """Snapshot of current observability context."""

    correlation_id: str
    trace_id: str
    span_id: str
    baggage: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, JSONValue] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__("time").time())

    def to_dict(
        self,
    ) -> dict[str, str | float | dict[str, str] | dict[str, JSONValue]]:
        """Convert snapshot to dictionary.

        Returns:
            dict - Snapshot as dictionary

        """
        return {
            "correlation_id": self.correlation_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "baggage": self.baggage,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        """Convert snapshot to JSON.

        Returns:
            str - Snapshot as JSON string

        """
        try:
            return json.dumps(self.to_dict())
        except (TypeError, ValueError):
            return "{}"


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
            self._metadata: dict[str, JSONValue] = {}
            self._baggage: dict[str, str] = {}
            self._request_id: str = ""
            self._parent_context: ContextSnapshot | None = None

        def set_metadata(self, key: str, value: JSONValue) -> FlextResult[bool]:
            """Set request-local metadata.

            Args:
                key: Metadata key
                value: Metadata value (must be JSON serializable)

            Returns:
                FlextResult[bool] - Ok if successful

            Behavior:
                - Stores in request-local storage
                - Value must be JSON serializable
                - Useful for user IDs, request IDs, etc.

            """
            try:
                # Validate JSON serializability
                json.dumps(value)
                self._metadata[key] = value

                FlextObservabilityAdvancedContext._logger.debug(f"Metadata set: {key}")
                return FlextResult[bool].ok(value=True)

            except (TypeError, ValueError) as e:
                return FlextResult[bool].fail(
                    f"Metadata value not JSON serializable: {e}",
                )

        def get_metadata(self, key: str) -> JSONValue | None:
            """Get request-local metadata.

            Args:
                key: Metadata key

            Returns:
                JSONValue - Metadata value or None

            """
            return self._metadata.get(key)

        def set_baggage(self, key: str, value: str) -> FlextResult[bool]:
            """Set baggage item (W3C Baggage API).

            Args:
                key: Baggage key
                value: Baggage value (string)

            Returns:
                FlextResult[bool] - Ok if successful

            """
            try:
                self._baggage[key] = value
                FlextObservabilityAdvancedContext._logger.debug(f"Baggage set: {key}")
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Failed to set baggage: {e}")

        def get_baggage(self, key: str) -> str | None:
            """Get baggage item.

            Args:
                key: Baggage key

            Returns:
                str - Baggage value or None

            """
            return self._baggage.get(key)

        def get_all_metadata(self) -> dict[str, JSONValue]:
            """Get all request-local metadata.

            Returns:
                dict - All metadata

            """
            return self._metadata.copy()

        def get_all_baggage(self) -> dict[str, str]:
            """Get all baggage items.

            Returns:
                dict - All baggage

            """
            return self._baggage.copy()

        def snapshot(
            self,
            correlation_id: str = "",
            trace_id: str = "",
            span_id: str = "",
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
                baggage=self.get_all_baggage(),
                metadata=self.get_all_metadata(),
            )

        def restore(self, snapshot: ContextSnapshot) -> FlextResult[bool]:
            """Restore context from snapshot.

            Args:
                snapshot: Context snapshot to restore

            Returns:
                FlextResult[bool] - Ok if successful

            Behavior:
                - Restores all metadata and baggage
                - Useful for async callbacks, background tasks

            """
            try:
                self._metadata = snapshot.metadata.copy()
                self._baggage = snapshot.baggage.copy()

                FlextObservabilityAdvancedContext._logger.debug(
                    "Context restored from snapshot",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Failed to restore context: {e}")

        def clear(self) -> FlextResult[bool]:
            """Clear all request-local context.

            Returns:
                FlextResult[bool] - Ok always

            """
            try:
                self._metadata.clear()
                self._baggage.clear()
                self._request_id = ""

                FlextObservabilityAdvancedContext._logger.debug("Context cleared")
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Failed to clear context: {e}")

        def merge(
            self,
            other: FlextObservabilityAdvancedContext.Context,
        ) -> FlextResult[bool]:
            """Merge another context into this one.

            Args:
                other: Other context to merge

            Returns:
                FlextResult[bool] - Ok if successful

            """
            try:
                self._metadata.update(other.get_all_metadata())
                self._baggage.update(other.get_all_baggage())

                FlextObservabilityAdvancedContext._logger.debug("Context merged")
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Failed to merge context: {e}")

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
    def set_metadata(key: str, value: JSONValue) -> FlextResult[bool]:
        """Convenience function: set metadata.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            FlextResult[bool] - Ok if successful

        """
        ctx = FlextObservabilityAdvancedContext.get_context()
        return ctx.set_metadata(key, value)

    @staticmethod
    def get_metadata(key: str) -> JSONValue | None:
        """Convenience function: get metadata.

        Args:
            key: Metadata key

        Returns:
            Any - Metadata value or None

        """
        ctx = FlextObservabilityAdvancedContext.get_context()
        return ctx.get_metadata(key)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "ContextSnapshot",
    "FlextObservabilityAdvancedContext",
]
