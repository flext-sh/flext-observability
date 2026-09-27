"""Test models for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels, m as tests_m

from flext_observability import m as obs_m


class TestsFlextObservabilityModels(FlextTestsModels):
    """Test models for flext-observability."""

    class TestsFlextObservability(tests_m.Tests, obs_m.Observability):
        """Canonical namespace for test models."""


m = TestsFlextObservabilityModels
__all__: list[str] = ["TestsFlextObservabilityModels", "m"]
