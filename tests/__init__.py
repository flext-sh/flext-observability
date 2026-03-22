# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from . import unit as unit
    from .constants import (
        FlextObservabilityTestConstants,
        FlextObservabilityTestConstants as c,
    )
    from .models import FlextObservabilityTestModels, FlextObservabilityTestModels as m
    from .protocols import (
        FlextObservabilityTestProtocols,
        FlextObservabilityTestProtocols as p,
    )
    from .typings import FlextObservabilityTestTypes, FlextObservabilityTestTypes as t
    from .unit.test_constants import TestFlextObservabilityConstants
    from .unit.test_factory import TestFlextObservabilityMasterFactoryReal
    from .unit.test_init import TestInitCoverage
    from .utilities import (
        FlextObservabilityTestUtilities,
        FlextObservabilityTestUtilities as u,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextObservabilityTestConstants": (
        "tests.constants",
        "FlextObservabilityTestConstants",
    ),
    "FlextObservabilityTestModels": ("tests.models", "FlextObservabilityTestModels"),
    "FlextObservabilityTestProtocols": (
        "tests.protocols",
        "FlextObservabilityTestProtocols",
    ),
    "FlextObservabilityTestTypes": ("tests.typings", "FlextObservabilityTestTypes"),
    "FlextObservabilityTestUtilities": (
        "tests.utilities",
        "FlextObservabilityTestUtilities",
    ),
    "TestFlextObservabilityConstants": (
        "tests.unit.test_constants",
        "TestFlextObservabilityConstants",
    ),
    "TestFlextObservabilityMasterFactoryReal": (
        "tests.unit.test_factory",
        "TestFlextObservabilityMasterFactoryReal",
    ),
    "TestInitCoverage": ("tests.unit.test_init", "TestInitCoverage"),
    "c": ("tests.constants", "FlextObservabilityTestConstants"),
    "d": ("flext_tests", "d"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "m": ("tests.models", "FlextObservabilityTestModels"),
    "p": ("tests.protocols", "FlextObservabilityTestProtocols"),
    "r": ("flext_tests", "r"),
    "s": ("flext_tests", "s"),
    "t": ("tests.typings", "FlextObservabilityTestTypes"),
    "u": ("tests.utilities", "FlextObservabilityTestUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "FlextObservabilityTestConstants",
    "FlextObservabilityTestModels",
    "FlextObservabilityTestProtocols",
    "FlextObservabilityTestTypes",
    "FlextObservabilityTestUtilities",
    "TestFlextObservabilityConstants",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
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
    "unit",
    "x",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
