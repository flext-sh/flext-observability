# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        config,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        s,
        settings,
        x,
    )

    from examples.constants import ExamplesFlextObservabilityConstants, c
    from examples.models import ExamplesFlextObservabilityModels, m
    from examples.protocols import ExamplesFlextObservabilityProtocols, p
    from examples.typings import ExamplesFlextObservabilityTypes, t
    from examples.utilities import ExamplesFlextObservabilityUtilities, u
    from flext_observability import cli, main, observability


__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "observability",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
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
        "build_lazy_import_map": "flext_core",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_core",
        "cli": "flext_observability",
        "config": "flext_core",
        "core": "flext_core",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "install_lazy_exports": "flext_core",
        "lazy": "flext_core",
        "lazy_getattr": "flext_core",
        "lazy_member": "flext_core",
        "m": ".models",
        "main": "flext_observability",
        "merge_lazy_imports": "flext_core",
        "normalize_lazy_imports": "flext_core",
        "observability": "flext_observability",
        "p": ".protocols",
        "r": "flext_core",
        "resolve_lazy_members": "flext_core",
        "s": "flext_core",
        "settings": "flext_core",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)
