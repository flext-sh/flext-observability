"""Test type aliases for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_observability import t


class TestsFlextObservabilityTypes(FlextTestsTypes, t):
    """Test type aliases for flext-observability."""

    class Tests(FlextTestsTypes.Tests):
        """Test-specific types."""


t = TestsFlextObservabilityTypes
__all__: list[str] = ["TestsFlextObservabilityTypes", "t"]
