"""Service base for flext-observability tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_observability import m
from tests.settings import TestsFlextObservabilitySettings


class TestsFlextObservabilityServiceBase(tests_s):
    """Observability test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextObservabilitySettings:
        """Return the typed Observability+Tests settings singleton."""
        return TestsFlextObservabilitySettings.fetch_global()

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextObservabilitySettings)


s = TestsFlextObservabilityServiceBase

__all__: list[str] = ["TestsFlextObservabilityServiceBase", "s"]
