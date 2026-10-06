"""Test types for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_observability import FlextObservabilityTypes


class TestsFlextObservabilityTypes(FlextTestsTypes, FlextObservabilityTypes):
    """Test types for flext-observability."""

    class TestsFlextObservability(
        FlextTestsTypes.Tests,
        FlextObservabilityTypes.Observability,
    ):
        """Canonical namespace for test types."""


t = TestsFlextObservabilityTypes
__all__: list[str] = ["TestsFlextObservabilityTypes", "t"]
