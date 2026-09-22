# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli, main

    from flext_core import (
        config,
        core,
        d,
        e,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        s,
        settings,
        x,
    )
    from flext_observability import observability

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
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "normalize_lazy_imports",
    "observability",
    "p",
    "r",
    "s",
    "settings",
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
            "flext_cli": ("cli", "main"),
            "flext_core": (
                "config",
                "core",
                "d",
                "e",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "s",
                "settings",
                "x",
            ),
            "flext_observability": ("observability",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
