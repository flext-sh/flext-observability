# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextObservabilityConstants, c
    from examples.models import ExamplesFlextObservabilityModels, m
    from examples.protocols import ExamplesFlextObservabilityProtocols, p
    from examples.typings import ExamplesFlextObservabilityTypes, t
    from examples.utilities import ExamplesFlextObservabilityUtilities, u
    from flext_core import d, e, h, r, s, x


__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ExamplesFlextObservabilityConstants": ".constants",
        "ExamplesFlextObservabilityModels": ".models",
        "ExamplesFlextObservabilityProtocols": ".protocols",
        "ExamplesFlextObservabilityTypes": ".typings",
        "ExamplesFlextObservabilityUtilities": ".utilities",
        "c": ".constants",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": ".models",
        "p": ".protocols",
        "r": "flext_core",
        "s": "flext_core",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)
