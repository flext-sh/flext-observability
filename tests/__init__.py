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
    from flext_tests import td as td, tf as tf, tk as tk, tv as tv

    from flext_observability import d as d, e as e, h as h, r as r, x as x
    from tests.base import (
        TestsFlextObservabilityServiceBase as TestsFlextObservabilityServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextObservabilityConstants as TestsFlextObservabilityConstants,
        c as c,
    )
    from tests.models import (
        TestsFlextObservabilityModels as TestsFlextObservabilityModels,
        m as m,
    )
    from tests.protocols import (
        TestsFlextObservabilityProtocols as TestsFlextObservabilityProtocols,
        p as p,
    )
    from tests.settings import (
        TestsFlextObservabilitySettings as TestsFlextObservabilitySettings,
    )
    from tests.typings import (
        TestsFlextObservabilityTypes as TestsFlextObservabilityTypes,
        t as t,
    )
    from tests.unit.test_constants import (
        TestsFlextObservabilityConstantsUnit as TestsFlextObservabilityConstantsUnit,
    )
    from tests.unit.test_factory import (
        TestsFlextObservabilityFactory as TestsFlextObservabilityFactory,
    )
    from tests.unit.test_init import (
        TestsFlextObservabilityInit as TestsFlextObservabilityInit,
    )
    from tests.utilities import (
        TestsFlextObservabilityUtilities as TestsFlextObservabilityUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextObservabilityServiceBase",
                "s",
            ),
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
            ".settings": ("TestsFlextObservabilitySettings",),
            ".typings": (
                "TestsFlextObservabilityTypes",
                "t",
            ),
            ".unit.test_constants": ("TestsFlextObservabilityConstantsUnit",),
            ".unit.test_factory": ("TestsFlextObservabilityFactory",),
            ".unit.test_init": ("TestsFlextObservabilityInit",),
            ".utilities": (
                "TestsFlextObservabilityUtilities",
                "u",
            ),
            "flext_observability": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextObservabilityConstants",
    "TestsFlextObservabilityConstantsUnit",
    "TestsFlextObservabilityFactory",
    "TestsFlextObservabilityInit",
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "TestsFlextObservabilityServiceBase",
    "TestsFlextObservabilitySettings",
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
    "tv",
    "u",
    "x",
]
