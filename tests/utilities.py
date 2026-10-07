"""Test utilities for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_observability import FlextObservabilityUtilities


class TestsFlextObservabilityUtilities(
    FlextTestsUtilities,
    FlextObservabilityUtilities,
):
    """Test utilities for flext-observability."""

    class TestsFlextObservability(
        FlextTestsUtilities.Tests,
        FlextObservabilityUtilities.Observability,
    ):
        """Canonical namespace for test utilities."""


u = TestsFlextObservabilityUtilities
__all__: list[str] = ["TestsFlextObservabilityUtilities", "u"]
