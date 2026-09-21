"""FLEXT Observability Utilities - Centralized domain utilities.

Unified utilities facade inheriting core FLEXT utilities.
Provides namespace classes for performance and sampling operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u

from ._utilities.base import FlextObservabilityUtilitiesBase
from ._utilities.domains import FlextObservabilityUtilitiesDomains


class FlextObservabilityUtilities(u, FlextObservabilityUtilitiesBase):
    """Centralized utilities for FLEXT Observability.

    Inherits CLI FLEXT utilities, providing additional namespace classes
    for observability domain operations.
    """

    class Observability(
        FlextObservabilityUtilitiesBase, FlextObservabilityUtilitiesDomains
    ):
        """Observability-specific project utilities."""


u = FlextObservabilityUtilities

__all__: list[str] = ["FlextObservabilityUtilities", "u"]
