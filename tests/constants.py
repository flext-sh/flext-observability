"""Test constants for flext-observability."""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_observability import FlextObservabilityConstants


class TestsFlextObservabilityConstants(
    FlextTestsConstants, FlextObservabilityConstants
):
    class Observability(FlextObservabilityConstants.Observability):
        class Tests: ...


c = TestsFlextObservabilityConstants
__all__: list[str] = ["TestsFlextObservabilityConstants", "c"]
