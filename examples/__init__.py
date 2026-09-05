# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_core import (
        FlextObservabilityConstants,
        FlextObservabilityConstants as c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        t,
        u,
        x,
    )

    from .constants import ExamplesFlextObservabilityConstants
    from .models import ExamplesFlextObservabilityModels
    from .protocols import ExamplesFlextObservabilityProtocols
    from .typings import ExamplesFlextObservabilityTypes
    from .utilities import ExamplesFlextObservabilityUtilities
__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "FlextObservabilityConstants",
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
            ".constants": ("ExamplesFlextObservabilityConstants",),
            ".models": ("ExamplesFlextObservabilityModels",),
            ".protocols": ("ExamplesFlextObservabilityProtocols",),
            ".typings": ("ExamplesFlextObservabilityTypes",),
            ".utilities": ("ExamplesFlextObservabilityUtilities",),
            "flext_core": (
                "FlextObservabilityConstants",
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
