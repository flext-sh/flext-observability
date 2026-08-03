"""FlextObservabilityConfig — frozen config singleton for flext-observability (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Observability:`` key and
are exposed through the open ``config.Observability`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Observability.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliConfig, m


class _ObservabilityNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextObservabilityConfig(FlextCliConfig):
    """Observability config auto-loaded model-less from ``config/*.yaml``."""

    Observability: _ObservabilityNamespace = _ObservabilityNamespace()


config: FlextObservabilityConfig = FlextObservabilityConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_observability import config``."""

__all__: list[str] = ["FlextObservabilityConfig", "config"]
