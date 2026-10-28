# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Observability Utilities - Centralized domain utilities.

Unified utilities facade inheriting core FLEXT utilities.
Provides namespace classes for performance and sampling operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import u as flext_cli_u

from flext_observability._utilities import (
    FlextObservabilityUtilitiesBase,
    FlextObservabilityUtilitiesDomains,
)


class FlextObservabilityUtilities(flext_cli_u, FlextObservabilityUtilitiesBase):
    """Centralized utilities for FLEXT Observability.

    Inherits CLI FLEXT utilities, providing additional namespace classes
    for observability domain operations.
    """

    class Observability(
        FlextObservabilityUtilitiesDomains,
        FlextObservabilityUtilitiesBase,
    ):
        """Observability-specific project utilities."""


u = FlextObservabilityUtilities
__all__: list[str] = ["FlextObservabilityUtilities", "u"]
