"""FLEXT Observability Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import t


class FlextObservabilityTypes(t):
    """Observability-specific type definitions extending t via MRO."""

    class Observability:
        """Observability domain namespace (flat members per AGENTS.md §149)."""

        type DomainLabels = t.ScalarMapping
        type HealthMetricsDict = t.JsonMapping


t = FlextObservabilityTypes

__all__: list[str] = ["FlextObservabilityTypes", "t"]
