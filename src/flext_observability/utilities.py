"""FLEXT Observability Utilities - Tier 0 Foundation Module.

Utility functions and classes for observability operations.
This module contains no service dependencies - pure utility functions only.

For services (with FlextContainer, FlextLogger dependencies), use:
    from flext_observability.services import FlextObservabilityServices

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextUtilities


class FlextObservabilityUtilities(FlextUtilities):
    """Observability utility functions.

    Extends FlextUtilities with observability-specific helpers.
    This is a Tier 0 module - no services dependencies allowed.

    For service operations (container, logger, config), use:
        from flext_observability.services import FlextObservabilityServices
    """

    class Observability:
        """Observability domain namespace."""


__all__ = ["FlextObservabilityUtilities"]
