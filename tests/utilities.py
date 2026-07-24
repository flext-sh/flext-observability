"""Test utilities for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_observability import u


class TestsFlextObservabilityUtilities(FlextTestsUtilities, u):
    """Test utilities for flext-observability."""

    class Tests(FlextTestsUtilities.Tests):
        """Test-specific utilities."""


u = TestsFlextObservabilityUtilities
__all__: list[str] = ["TestsFlextObservabilityUtilities", "u"]
