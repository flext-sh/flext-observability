# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Observability Tests - Test infrastructure and utilities.

Provides TestsFlextObservability classes extending FlextTests and FlextObservability
for comprehensive testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from tests.constants import TestsFlextObservabilityConstants
    from tests.models import TestsFlextObservabilityModels, m, tm
    from tests.protocols import TestsFlextObservabilityProtocols, p
    from tests.typings import (
        TestsFlextObservabilityTypes,
        TestsFlextObservabilityTypes as t,
    )
    from tests.unit.test_constants import (
        TestFlextObservabilityConstants,
        TestFlextObservabilityConstants as c,
    )
    from tests.unit.test_factory import TestFlextObservabilityMasterFactoryReal
    from tests.unit.test_init import TestInitCoverage
    from tests.utilities import (
        TestsFlextObservabilityUtilities,
        TestsFlextObservabilityUtilities as u,
    )

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
    "c": ("tests.unit.test_constants", "TestFlextObservabilityConstants"),
    "m": ("tests.models", "m"),
    "p": ("tests.protocols", "p"),
    "t": ("tests.typings", "TestsFlextObservabilityTypes"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextObservabilityUtilities"),
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
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
