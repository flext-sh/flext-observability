"""Test constants for flext-observability."""

from __future__ import annotations

from flext_tests import c as tests_c

from flext_observability import c as obs_c


class TestsFlextObservabilityConstants(tests_c, obs_c):
    """Test constants for flext-observability."""

    class TestsFlextObservability(tests_c.Tests, obs_c.Observability):
        """Canonical namespace for test constants."""


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
