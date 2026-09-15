"""Test type aliases for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import t as tests_t

from flext_observability import t as obs_t


class TestsFlextObservabilityTypes(tests_t):
    """Test type aliases for flext-observability."""

    class TestsFlextObservability(tests_t.Tests, obs_t.Observability):
        """Canonical namespace for test type aliases."""


t = TestsFlextObservabilityTypes
__all__: list[str] = ["TestsFlextObservabilityTypes", "t"]
