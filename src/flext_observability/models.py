# AUTO-GENERATED FILE — Regenerate with: make gen
"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import m as flext_cli_m

from flext_observability._models import (
    FlextObservabilityModelsBase,
    FlextObservabilityModelsDomains,
)


class FlextObservabilityModels(flext_cli_m, FlextObservabilityModelsBase):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class Observability(FlextObservabilityModelsBase, FlextObservabilityModelsDomains):
        """Observability domain models namespace."""


m = FlextObservabilityModels
__all__: list[str] = ["FlextObservabilityModels", "m"]
