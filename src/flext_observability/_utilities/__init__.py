# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._utilities.base import FlextObservabilityUtilitiesBase
    from flext_observability._utilities.domains import (
        FlextObservabilityUtilitiesDomains,
    )


__all__: tuple[str, ...] = (
    "FlextObservabilityUtilitiesBase",
    "FlextObservabilityUtilitiesDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityUtilitiesBase": ".base",
        "FlextObservabilityUtilitiesDomains": ".domains",
    }),
    public_exports=__all__,
)
