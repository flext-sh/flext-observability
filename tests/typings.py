"""Test type aliases for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_observability import FlextObservabilityTypes


class FlextObservabilityTestTypes(FlextTestsTypes, FlextObservabilityTypes):
    """Test type aliases for flext-observability."""

    class Observability(FlextObservabilityTypes.Observability):
        """Observability domain test type aliases."""

        class Tests:
            """Test-specific type aliases."""


t = FlextObservabilityTestTypes
__all__ = ["FlextObservabilityTestTypes", "t"]
