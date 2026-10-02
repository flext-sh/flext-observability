# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x
    from tests import integration, unit
    from tests.base import TestsFlextObservabilityServiceBase, s
    from tests.constants import TestsFlextObservabilityConstants, c
    from tests.models import TestsFlextObservabilityModels, m
    from tests.protocols import TestsFlextObservabilityProtocols, p
    from tests.settings import TestsFlextObservabilitySettings
    from tests.typings import TestsFlextObservabilityTypes, t
    from tests.utilities import TestsFlextObservabilityUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextObservabilityConstants",
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "TestsFlextObservabilityServiceBase",
    "TestsFlextObservabilitySettings",
    "TestsFlextObservabilityTypes",
    "TestsFlextObservabilityUtilities",
    "api",
    "c",
    "d",
    "e",
    "h",
    "integration",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextObservabilityServiceBase", "s"),
            ".constants": ("TestsFlextObservabilityConstants", "c"),
            ".integration": ("integration",),
            ".models": ("TestsFlextObservabilityModels", "m"),
            ".protocols": ("TestsFlextObservabilityProtocols", "p"),
            ".settings": ("TestsFlextObservabilitySettings",),
            ".typings": ("TestsFlextObservabilityTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextObservabilityUtilities", "u"),
            "flext_tests": ("api", "d", "e", "h", "r", "td", "tf", "tk", "tm", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
