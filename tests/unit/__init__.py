# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.unit.test_constants import (
        TestFlextObservabilityConstants,
        TestFlextObservabilityConstants as c,
    )
    from tests.unit.test_factory import TestFlextObservabilityMasterFactoryReal
    from tests.unit.test_init import TestInitCoverage

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextObservabilityConstants": (
        "tests.unit.test_constants",
        "TestFlextObservabilityConstants",
    ),
    "TestFlextObservabilityMasterFactoryReal": (
        "tests.unit.test_factory",
        "TestFlextObservabilityMasterFactoryReal",
    ),
    "TestInitCoverage": ("tests.unit.test_init", "TestInitCoverage"),
    "c": ("tests.unit.test_constants", "TestFlextObservabilityConstants"),
}

__all__ = [
    "TestFlextObservabilityConstants",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "c",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
