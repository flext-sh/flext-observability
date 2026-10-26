# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Observability Types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import t

from flext_observability._typings import (
    FlextObservabilityTypingsBase,
    FlextObservabilityTypingsDomains,
)


class FlextObservabilityTypes(t, FlextObservabilityTypingsBase):
    """Observability-specific type definitions extending t via MRO."""

    class Observability(
        FlextObservabilityTypingsBase,
        FlextObservabilityTypingsDomains,
    ):
        """Observability domain namespace (flat members per AGENTS.md §149)."""


t = FlextObservabilityTypes
__all__: list[str] = ["FlextObservabilityTypes", "t"]
