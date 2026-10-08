"""FlextObservabilityConfig — frozen config singleton for flext-observability.

Reference: ADR-005 §7. Model-less: business rules live in ``config/*.yaml``
under the ``Observability:`` key and are exposed through the open
``config.Observability`` namespace (``extra="allow"``), with no per-domain
model. Access is ``config.Observability.<domain>[<key>...]``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_cli import FlextCliConfig, m

from flext_core import FlextSettings
from flext_observability._models._observability_namespace import (
    FlextObservabilityNamespace,
)


class FlextObservabilityConfig(FlextSettings, FlextCliConfig):
    """Observability config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); unlike never-instantiated
    namespace holders, this class IS instantiated by ``fetch_global``, so the
    instance-inert holder contract does not apply and pydantic settings
    construction machinery stays intact.
    """

    Observability: Annotated[
        FlextObservabilityNamespace,
        m.Field(
            description=(
                "Open namespace exposing ``config/*.yaml`` under ``Observability``."
            ),
        ),
    ] = FlextObservabilityNamespace()


config: FlextObservabilityConfig = FlextObservabilityConfig.fetch_global()
"""Pre-instantiated frozen config singleton —
``from flext_observability import config``."""

__all__: list[str] = ["FlextObservabilityConfig", "config"]
