# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_core import c as _c, d, e, h, r, s, x

    from .constants import (
        ExamplesFlextObservabilityConstants,
        ExamplesFlextObservabilityConstants as c,
    )
    from .models import (
        ExamplesFlextObservabilityModels,
        ExamplesFlextObservabilityModels as m,
    )
    from .protocols import (
        ExamplesFlextObservabilityProtocols,
        ExamplesFlextObservabilityProtocols as p,
    )
    from .typings import (
        ExamplesFlextObservabilityTypes,
        ExamplesFlextObservabilityTypes as t,
    )
    from .utilities import (
        ExamplesFlextObservabilityUtilities,
        ExamplesFlextObservabilityUtilities as u,
    )
__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "_c",
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
        alias_groups=MappingProxyType({"flext_core": (("_c", "c"),)}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
