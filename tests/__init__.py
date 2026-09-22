# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_tests import (
        api,
        config,
        core,
        d,
        e,
        from_json,
        h,
        install_local_packages,
        lazy_attribute,
        load_infra_report,
        r,
        services,
        settings,
        td,
        tf,
        tk,
        tm,
        to_json,
        to_jsonable_python,
        tv,
        x,
    )

    from flext_observability import main, observability

    from . import integration, unit
    from .base import (
        TestsFlextObservabilityServiceBase,
        TestsFlextObservabilityServiceBase as s,
    )
    from .constants import (
        TestsFlextObservabilityConstants,
        TestsFlextObservabilityConstants as c,
    )
    from .models import (
        TestsFlextObservabilityModels,
        TestsFlextObservabilityModels as m,
    )
    from .protocols import (
        TestsFlextObservabilityProtocols,
        TestsFlextObservabilityProtocols as p,
    )
    from .settings import TestsFlextObservabilitySettings
    from .typings import TestsFlextObservabilityTypes, TestsFlextObservabilityTypes as t
    from .utilities import (
        TestsFlextObservabilityUtilities,
        TestsFlextObservabilityUtilities as u,
    )
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
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "install_local_packages",
    "integration",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "observability",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "to_json",
    "to_jsonable_python",
    "tv",
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
            "flext_cli": ("cli",),
            "flext_observability": ("main", "observability"),
            "flext_tests": (
                "api",
                "config",
                "core",
                "d",
                "e",
                "from_json",
                "h",
                "install_local_packages",
                "lazy_attribute",
                "load_infra_report",
                "r",
                "services",
                "settings",
                "td",
                "tf",
                "tk",
                "tm",
                "to_json",
                "to_jsonable_python",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
