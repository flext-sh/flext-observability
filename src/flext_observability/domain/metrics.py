"""Metrics Domain - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Complex import paths are deprecated.

❌ OLD: from flext_observability.domain.metrics import Metric
✅ NEW: from flext_observability import Metric

This module provides metrics domain entities, value objects,
and business logic for metric collection and processing.
"""

from __future__ import annotations

import warnings
from typing import Any

# NO FALLBACKS - SEMPRE usar implementações originais conforme instrução
from flext_observability.domain import (
    Metric,
    MetricType,
    MetricValue,
    ThresholdValue,
)

# Deprecation warning for complex path access
warnings.warn(
    "🚨 DEPRECATED COMPLEX PATH: Importing from 'flext_observability.domain.metrics' is deprecated.\n"
    "✅ SIMPLE SOLUTION: from flext_observability import Metric, MetricType, MetricValue\n"
    "💡 ALL metric types are now available at root level for better productivity!\n"
    "📖 Complex paths will be removed in version 0.8.0.\n"
    "📚 Migration guide: https://docs.flext.dev/observability/simple-imports",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export for backward compatibility
__all__ = [
    "Metric",
    "MetricType",
    "MetricValue",
    "ThresholdValue",
]


def __getattr__(name: str) -> Any:
    """Handle attribute access with deprecation warnings."""
    if name in __all__:
        warnings.warn(
            f"🚨 DEPRECATED ACCESS: Using 'flext_observability.domain.metrics.{name}' is deprecated.\n"
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

    msg = f"module 'flext_observability.domain.metrics' has no attribute '{name}'"
    raise AttributeError(msg)
