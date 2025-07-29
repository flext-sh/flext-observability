"""FlextStructured - Structured logging specific to observability.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Extends flext-core logging with observability-specific structured features.
"""

from __future__ import annotations

from contextvars import ContextVar

from flext_core import FlextResult, get_logger

# ============================================================================
# OBSERVABILITY-SPECIFIC STRUCTURED LOGGING
# ============================================================================

# Context for correlation IDs and observability metadata
_flext_observability_context: ContextVar[dict[str, object] | None] = ContextVar(
    "flext_observability_context",
    default=None,
)


class FlextStructuredLogger:
    """Observability-specific structured logger extending flext-core."""

    def __init__(self, name: str) -> None:
        """Initialize with flext-core logger."""
        self._core_logger = get_logger(name)
        self._bound_data: dict[str, object] = {}

    def flext_observability_info(
        self, message: str, **observability_data: object,
    ) -> FlextResult[None]:
        """Log info with observability context."""
        try:
            context = _flext_observability_context.get() or {}
            all_data = {**context, **self._bound_data, **observability_data}

            if all_data:
                extras = " | ".join(f"{k}={v}" for k, v in all_data.items())
                formatted_message = f"{message} | {extras}"
            else:
                formatted_message = message

            self._core_logger.info(formatted_message)
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Structured logging failed: {e}")

    def flext_observability_error(
        self, message: str, **observability_data: object,
    ) -> FlextResult[None]:
        """Log error with observability context."""
        try:
            context = _flext_observability_context.get() or {}
            all_data = {**context, **self._bound_data, **observability_data}

            if all_data:
                extras = " | ".join(f"{k}={v}" for k, v in all_data.items())
                formatted_message = f"{message} | {extras}"
            else:
                formatted_message = message

            self._core_logger.error(formatted_message)
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Structured logging failed: {e}")

    def flext_bind_observability(
        self, **data: object,
    ) -> FlextStructuredLogger:
        """Bind observability-specific data to logger."""
        new_logger = FlextStructuredLogger(self._core_logger.__class__.__name__)
        new_logger._core_logger = self._core_logger
        new_logger._bound_data = {**self._bound_data, **data}
        return new_logger


def flext_set_correlation_id(correlation_id: str) -> FlextResult[None]:
    """Set correlation ID for observability context."""
    try:
        context = _flext_observability_context.get() or {}.copy()
        context["correlation_id"] = correlation_id
        _flext_observability_context.set(context)
        return FlextResult.ok(None)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to set correlation ID: {e}")


def flext_get_correlation_id() -> FlextResult[str]:
    """Get current correlation ID."""
    try:
        context = _flext_observability_context.get() or {}
        correlation_id = context.get("correlation_id", "")
        correlation_id_str = str(correlation_id) if correlation_id else ""
        return FlextResult.ok(correlation_id_str)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to get correlation ID: {e}")


def flext_get_structured_logger(name: str) -> FlextStructuredLogger:
    """Get observability-specific structured logger."""
    return FlextStructuredLogger(name)


__all__ = [
    "FlextStructuredLogger",
    "flext_get_correlation_id",
    "flext_get_structured_logger",
    "flext_set_correlation_id",
]
