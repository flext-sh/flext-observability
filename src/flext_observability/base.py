"""Shared service foundation for flext-observability components.

Provides typed access to the registered ``observability`` settings namespace while
preserving flext-core service runtime behavior.
"""

from __future__ import annotations

from abc import ABC

from flext_core import s

from . import FlextObservabilitySettings, m, p, t


class FlextObservabilityServiceBase[
    TDomainResult: t.JsonPayload | t.SequenceOf[t.JsonPayload]
](s[TDomainResult], ABC):
    """Base class for flext-observability services with typed API settings access."""

    def __init__(
        self,
        *,
        settings_type: type | None = None,
        runtime_settings: p.Settings | None = None,
        settings_overrides: t.ScalarMapping | None = None,
        initial_context: p.Context | None = None,
    ) -> None:
        """Bootstrap observability services with one concrete runtime settings contract."""
        super().__init__(
            settings_type=settings_type or FlextObservabilitySettings,
            runtime_settings=runtime_settings,
            settings_overrides=settings_overrides,
            initial_context=initial_context,
        )

    @classmethod
    def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        """Return runtime bootstrap options for observability services."""
        return m.RuntimeBootstrapOptions(settings_type=FlextObservabilitySettings)


s = FlextObservabilityServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextObservabilityServiceBase", "s"]
