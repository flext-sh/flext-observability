"""Test protocols for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p as tests_p

from flext_observability import p as obs_p


class TestsFlextObservabilityProtocols(tests_p):
    """Test protocols for flext-observability."""

    class TestsFlextObservability(tests_p.Tests, obs_p.Observability):
        """Canonical namespace for test protocols."""


p = TestsFlextObservabilityProtocols
__all__: list[str] = ["TestsFlextObservabilityProtocols", "p"]
