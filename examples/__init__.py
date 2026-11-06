# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextObservabilityConstants, c
    from examples.models import ExamplesFlextObservabilityModels, m
    from examples.protocols import ExamplesFlextObservabilityProtocols, p
    from examples.typings import ExamplesFlextObservabilityTypes, t
    from examples.utilities import ExamplesFlextObservabilityUtilities, u
    from flext_observability import (
        config,
        d,
        e,
        h,
        main,
        observability,
        r,
        s,
        settings,
        x,
    )


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
        "d": "flext_observability",
        "e": "flext_observability",
        "h": "flext_observability",
        "m": ".models",
        "main": "flext_observability",
        "observability": "flext_observability",
        "p": ".protocols",
        "r": "flext_observability",
        "s": "flext_observability",
        "settings": "flext_observability",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_observability",
    },
    public_exports=__all__,
)
