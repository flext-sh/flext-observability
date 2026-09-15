"""FLEXT Observability Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import t as _t

from ._typings import FlextObservabilityTypingsBase


class FlextObservabilityTypes(_t, FlextObservabilityTypingsBase):
    """Observability-specific type definitions extending t via MRO."""

    class Observability:
        """Observability domain namespace (flat members per AGENTS.md §149)."""

        type DomainLabels = _t.ScalarMapping
        type HealthMetricsDict = _m.JsonMapping


t = FlextObservabilityTypes

__all__: list[str] = ["FlextObservabilityTypes", "t"]
