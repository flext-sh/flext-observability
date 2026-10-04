# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_observability._protocols.base import FlextObservabilityProtocolsBase
    from flext_observability._protocols.domains import (
        FlextObservabilityProtocolsDomains,
    )


__all__: tuple[str, ...] = (
    "FlextObservabilityProtocolsBase",
    "FlextObservabilityProtocolsDomains",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservabilityProtocolsBase": ".base",
        "FlextObservabilityProtocolsDomains": ".domains",
    }),
    public_exports=__all__,
)
