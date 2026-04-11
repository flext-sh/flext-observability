# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import (
        d,
        e,
        h,
        r,
        reset_settings,
        s,
        settings,
        settings_factory,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

    from tests.constants import TestsFlextObservabilityConstants, c
    from tests.models import TestsFlextObservabilityModels, m
    from tests.protocols import TestsFlextObservabilityProtocols, p
    from tests.typings import TestsFlextObservabilityTypes, t
    from tests.utilities import TestsFlextObservabilityUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextObservabilityConstants",
                "c",
            ),
            ".models": (
                "TestsFlextObservabilityModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextObservabilityProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextObservabilityTypes",
                "t",
            ),
            ".utilities": (
                "TestsFlextObservabilityUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "reset_settings",
                "s",
                "settings",
                "settings_factory",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestsFlextObservabilityConstants",
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "TestsFlextObservabilityTypes",
    "TestsFlextObservabilityUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "reset_settings",
    "s",
    "settings",
    "settings_factory",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
