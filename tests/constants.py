"""Test constants for flext-observability."""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_observability import c


class TestsFlextObservabilityConstants(
    FlextTestsConstants,
    c,
):
    class Tests(FlextTestsConstants.Tests):
        """Test-specific constants."""


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
