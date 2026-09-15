"""Test utilities for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u as tests_u

from flext_observability import u as obs_u


class TestsFlextObservabilityUtilities(tests_u):
    """Test utilities for flext-observability."""

    class TestsFlextObservability(tests_u.Tests, obs_u.Observability):
        """Canonical namespace for test utilities."""


u = TestsFlextObservabilityUtilities
__all__: list[str] = ["TestsFlextObservabilityUtilities", "u"]
