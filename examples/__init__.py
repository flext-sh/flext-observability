# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextObservabilityConstants", "c"),
            ".models": ("ExamplesFlextObservabilityModels", "m"),
            ".protocols": ("ExamplesFlextObservabilityProtocols", "p"),
            ".typings": ("ExamplesFlextObservabilityTypes", "t"),
            ".utilities": ("ExamplesFlextObservabilityUtilities", "u"),
            "flext_core": ("d", "e", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
