"""Test constants for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_observability import FlextObservabilityConstants


class FlextObservabilityTestConstants(FlextTestsConstants, FlextObservabilityConstants):
    """Test constants for flext-observability."""

    class Observability(FlextObservabilityConstants.Observability):
        """Observability domain test constants."""

        class Tests:
            """Test-specific constants."""


c = FlextObservabilityTestConstants
__all__ = ["FlextObservabilityTestConstants", "c"]
