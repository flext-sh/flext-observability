"""Observability domain type aliases owned by the private typings family."""

from __future__ import annotations

from flext_cli import t


class FlextObservabilityTypingsDomains:
    """Observability domain type aliases."""

    type DomainLabels = t.ScalarMapping
    type HealthMetricsDict = t.JsonMapping


__all__: list[str] = ["FlextObservabilityTypingsDomains"]
