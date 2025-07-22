"""Logging Infrastructure - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Complex import paths are deprecated.

❌ OLD: from flext_observability.infrastructure.logging import get_logger
✅ NEW: from flext_observability import get_logger

This module provides logging infrastructure with structured logging,
context management, and OpenTelemetry integration.
"""

from __future__ import annotations

import warnings
from typing import Any

# Import real implementations from compatibility layer
from flext_observability._compatibility import (
    LoggingConfig,
    StructuredLogger,
    bind_context,
    clear_context,
    get_logger,
    setup_logging,
    with_context,
)

# Re-export with local names for backward compatibility
__all__ = [
    "LoggingConfig",
    "StructuredLogger",
    "bind_context",
    "clear_context",
    "get_logger",
    "setup_logging",
    "with_context",
]

# Deprecation warning for complex path access
warnings.warn(
    "🚨 DEPRECATED COMPLEX PATH: Importing from 'flext_observability.infrastructure.logging' is deprecated.\n"
    "✅ SIMPLE SOLUTION: from flext_observability import get_logger, setup_logging\n"
    "💡 ALL logging functions are now available at root level for better productivity!\n"
    "📖 Complex paths will be removed in version 0.8.0.\n"
    "📚 Migration guide: https://docs.flext.dev/observability/simple-imports",
    DeprecationWarning,
    stacklevel=2,
)


def __getattr__(name: str) -> Any:
    """Handle attribute access with deprecation warnings."""
    if name in __all__:
        warnings.warn(
            f"🚨 DEPRECATED ACCESS: Using 'flext_observability.infrastructure.logging.{name}' is deprecated.\n"
            f"✅ SIMPLE SOLUTION: from flext_observability import {name}\n"
            f"💡 Direct root-level imports are much simpler and more productive!\n"
            f"📖 This access pattern will be removed in version 0.8.0.",
            DeprecationWarning,
            stacklevel=2,
        )

    # Return the actual implementation
    globals_dict = globals()
    if name in globals_dict:
        return globals_dict[name]

    msg = f"module 'flext_observability.infrastructure.logging' has no attribute '{name}'"
    raise AttributeError(msg)
