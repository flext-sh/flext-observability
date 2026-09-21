"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import m

from ._models.base import FlextObservabilityModelsBase
from ._models.domains import FlextObservabilityModelsDomains


class FlextObservabilityModels(m, FlextObservabilityModelsBase):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class Observability(FlextObservabilityModelsBase, FlextObservabilityModelsDomains):
        """Observability domain models namespace."""


m = FlextObservabilityModels

__all__: list[str] = ["FlextObservabilityModels", "m"]
