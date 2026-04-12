"""FLEXT Observability Health Domain Models.

Provides focused health monitoring models following the namespace class pattern.
Contains health check entities, configurations, and factory methods for health operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class FlextObservabilityHealth:
    """Health monitoring mixin for FlextObservability MRO composition.

    Health check factory method is defined on the facade (api.py).
    This mixin provides health-related utilities and extensions.
    """


__all__: list[str] = ["FlextObservabilityHealth"]
