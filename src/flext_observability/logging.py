"""FLEXT Observability Logging Domain Models.

Provides focused logging models following the namespace class pattern.
Contains log entities, configurations, and factory methods for logging operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels


class FlextObservabilityLogging(FlextModels):
    """Focused logging models for observability operations extending FlextModels.

    Provides complete logging entities, configurations, and operations
    for structured logging, log management, and log analysis within the FLEXT ecosystem.
    """


__all__ = ["FlextObservabilityLogging"]
