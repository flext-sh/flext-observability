"""Test constants for flext-observability."""

from __future__ import annotations

from flext_tests import FlextTestsConstants, c as tests_c

from flext_observability import c as obs_c


class TestsFlextObservabilityConstants(FlextTestsConstants):
    """Test constants for flext-observability."""

    class Observability(obs_c.Observability):
        """Re-exported observability constants namespace."""

    class TestsFlextObservability(tests_c.Tests, obs_c.Observability):
        """Canonical namespace for test constants."""


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
