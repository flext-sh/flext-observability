"""Observability domain type aliases owned by the private typings family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t

from flext_observability import c


class FlextObservabilityTypingsDomains:
    """Observability domain type aliases."""

    type DomainLabels = t.ScalarMapping
    type HealthMetricsDict = t.JsonMapping
    type ErrorSeverity = c.Observability.ErrorSeverity


__all__: list[str] = ["FlextObservabilityTypingsDomains"]
