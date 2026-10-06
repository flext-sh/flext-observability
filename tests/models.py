"""Test models for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_observability import FlextObservabilityModels


class TestsFlextObservabilityModels(FlextTestsModels, FlextObservabilityModels):
    """Test models for flext-observability."""

    class TestsFlextObservability(
        FlextTestsModels.Tests,
        FlextObservabilityModels.Observability,
    ):
        """Canonical namespace for test models."""


m = TestsFlextObservabilityModels
__all__: list[str] = ["TestsFlextObservabilityModels", "m"]
