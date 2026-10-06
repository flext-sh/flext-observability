"""Test constants for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_observability import FlextObservabilityConstants


class TestsFlextObservabilityConstants(FlextTestsConstants):
    """Test constants for flext-observability."""

    class Observability(FlextObservabilityConstants.Observability):
        """Canonical observability constants namespace for tests."""


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
