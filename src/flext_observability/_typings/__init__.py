# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._typings.base import FlextObservabilityTypingsBase
    from flext_observability._typings.domains import FlextObservabilityTypingsDomains


__all__: tuple[str, ...] = (
    "FlextObservabilityTypingsBase",
    "FlextObservabilityTypingsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityTypingsBase": ".base",
        "FlextObservabilityTypingsDomains": ".domains",
    }),
    public_exports=__all__,
)
