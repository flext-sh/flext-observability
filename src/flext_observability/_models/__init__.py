# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._models.base import FlextObservabilityModelsBase
    from flext_observability._models.domains import FlextObservabilityModelsDomains


__all__: tuple[str, ...] = (
    "FlextObservabilityModelsBase",
    "FlextObservabilityModelsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityModelsBase": ".base",
        "FlextObservabilityModelsDomains": ".domains",
    }),
    public_exports=__all__,
)
