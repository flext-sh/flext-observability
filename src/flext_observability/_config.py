"""FlextObservabilityConfig — frozen, validated config singleton.

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call (model-less, ``extra=allow`` at the FlextCliConfig base).
The flat YAML is then validated into the pure-Pydantic ``_models.config``
shapes and exposed as typed domain objects under ``config.Observability``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import ClassVar

from flext_cli import FlextCliConfig
from flext_observability._models.config import FlextObservabilityConfigModels


class FlextObservabilityConfig(FlextCliConfig):
    """Observability config auto-loaded from ``config/*.yaml``."""

    CONFIG_DIR: ClassVar[str] = str(
        Path(__file__).resolve().parents[2] / "config",
    )

    @cached_property
    def Observability(self) -> FlextObservabilityConfigModels.Observability:
        """Validated ``Observability`` business-rule config namespace."""
        root = FlextObservabilityConfigModels.Root.model_validate(
            dict(self.model_extra or {}),
        )
        return root.Observability


config: FlextObservabilityConfig = FlextObservabilityConfig.fetch_global()
"""Pre-instantiated frozen config singleton."""

__all__: list[str] = ["FlextObservabilityConfig", "config"]
