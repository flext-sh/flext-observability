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
    from flext_tests import td, tf, tk, tm, tv

    from flext_observability import d, e, h, r, s, x
    from tests.constants import TestsFlextObservabilityConstants, c
    from tests.models import TestsFlextObservabilityModels, m
    from tests.protocols import TestsFlextObservabilityProtocols, p
    from tests.typings import TestsFlextObservabilityTypes, t
    from tests.unit.test_constants import Testc
    from tests.unit.test_factory import TestFlextObservabilityMasterFactoryReal
    from tests.unit.test_init import TestInitCoverage
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
            ".unit.test_constants": ("Testc",),
            ".unit.test_factory": ("TestFlextObservabilityMasterFactoryReal",),
            ".unit.test_init": ("TestInitCoverage",),
            ".utilities": (
                "TestsFlextObservabilityUtilities",
                "u",
            ),
            "flext_observability": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
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

__all__: list[str] = [
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "Testc",
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
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
