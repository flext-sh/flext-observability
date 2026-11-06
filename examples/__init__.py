# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, s, x

    from examples.constants import ExamplesFlextObservabilityConstants, c
    from examples.models import ExamplesFlextObservabilityModels, m
    from examples.protocols import ExamplesFlextObservabilityProtocols, p
    from examples.typings import ExamplesFlextObservabilityTypes, t
    from examples.utilities import ExamplesFlextObservabilityUtilities, u
    from flext_observability import config, main, observability, settings


__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "observability",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "ExamplesFlextObservabilityConstants": ".constants",
        "ExamplesFlextObservabilityModels": ".models",
        "ExamplesFlextObservabilityProtocols": ".protocols",
        "ExamplesFlextObservabilityTypes": ".typings",
        "ExamplesFlextObservabilityUtilities": ".utilities",
        "c": ".constants",
        "config": "flext_observability",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": ".models",
        "main": "flext_observability",
        "observability": "flext_observability",
        "p": ".protocols",
        "r": "flext_core",
        "s": "flext_core",
        "settings": "flext_observability",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    },
    public_exports=__all__,
)
