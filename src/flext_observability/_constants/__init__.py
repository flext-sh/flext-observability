# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._constants.base import FlextObservabilityConstantsBase
    from flext_observability._constants.domains import (
        FlextObservabilityConstantsDomains,
    )


__all__: tuple[str, ...] = (
    "FlextObservabilityConstantsBase",
    "FlextObservabilityConstantsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityConstantsBase": ".base",
        "FlextObservabilityConstantsDomains": ".domains",
    }),
    public_exports=__all__,
)
