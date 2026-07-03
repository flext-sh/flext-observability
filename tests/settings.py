"""Runtime settings for flext-observability tests."""

from __future__ import annotations

from flext_tests.settings import FlextTestsSettings

from flext_observability import FlextObservabilitySettings


class TestsFlextObservabilitySettings(
    FlextObservabilitySettings,
    FlextTestsSettings,
):
    """Observability settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextObservabilitySettings"]
