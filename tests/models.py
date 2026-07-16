"""Test models for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_observability import m


class TestsFlextObservabilityModels(FlextTestsModels, m):
    """Test models for flext-observability."""

    class Tests(FlextTestsModels.Tests):
        """Test-specific models."""


m = TestsFlextObservabilityModels
__all__: list[str] = ["TestsFlextObservabilityModels", "m"]
