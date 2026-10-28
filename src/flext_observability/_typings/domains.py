"""Observability domain type aliases owned by the private typings family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_cli import t

from flext_observability import c


class FlextObservabilityTypingsDomains:
    """Observability domain type aliases."""

    type DomainLabels = Mapping[str, t.Scalar]
    type HealthMetricsDict = t.JsonMapping
    type ErrorSeverity = c.Observability.ErrorSeverity


__all__: list[str] = ["FlextObservabilityTypingsDomains"]
