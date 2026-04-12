"""Test constants for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_observability import FlextObservabilityConstants


class TestsFlextObservabilityConstants(
    FlextTestsConstants, FlextObservabilityConstants
):
    """Test constants for flext-observability."""

    class Observability(FlextObservabilityConstants.Observability):
        """Observability domain test constants."""

        class Tests:
            """Test-specific constants."""


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
