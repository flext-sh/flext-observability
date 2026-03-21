# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from . import unit as unit
    from .constants import (
        TestsFlextObservabilityConstants,
        TestsFlextObservabilityConstants as c,
    )
    from .models import (
        TestsFlextObservabilityModels,
        TestsFlextObservabilityModels as m,
        tm,
    )
    from .protocols import (
        TestsFlextObservabilityProtocols,
        TestsFlextObservabilityProtocols as p,
    )
    from .typings import TestsFlextObservabilityTypes, TestsFlextObservabilityTypes as t
    from .unit import (
        TestFlextObservabilityConstants,
        TestFlextObservabilityMasterFactoryReal,
        TestInitCoverage,
    )
    from .utilities import (
        TestsFlextObservabilityUtilities,
        TestsFlextObservabilityUtilities as u,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextObservabilityConstants": (
        "tests.unit",
        "TestFlextObservabilityConstants",
    ),
    "TestFlextObservabilityMasterFactoryReal": (
        "tests.unit",
        "TestFlextObservabilityMasterFactoryReal",
    ),
    "TestInitCoverage": ("tests.unit", "TestInitCoverage"),
    "TestsFlextObservabilityConstants": (
        "tests.constants",
        "TestsFlextObservabilityConstants",
    ),
    "TestsFlextObservabilityModels": ("tests.models", "TestsFlextObservabilityModels"),
    "TestsFlextObservabilityProtocols": (
        "tests.protocols",
        "TestsFlextObservabilityProtocols",
    ),
    "TestsFlextObservabilityTypes": ("tests.typings", "TestsFlextObservabilityTypes"),
    "TestsFlextObservabilityUtilities": (
        "tests.utilities",
        "TestsFlextObservabilityUtilities",
    ),
    "c": ("tests.constants", "TestsFlextObservabilityConstants"),
    "m": ("tests.models", "TestsFlextObservabilityModels"),
    "p": ("tests.protocols", "TestsFlextObservabilityProtocols"),
    "t": ("tests.typings", "TestsFlextObservabilityTypes"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextObservabilityUtilities"),
    "unit": ("tests.unit", ""),
}

__all__ = [
    "TestFlextObservabilityConstants",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "TestsFlextObservabilityConstants",
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "TestsFlextObservabilityTypes",
    "TestsFlextObservabilityUtilities",
    "c",
    "m",
    "p",
    "t",
    "tm",
    "u",
    "unit",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
