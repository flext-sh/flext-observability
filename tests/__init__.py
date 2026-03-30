# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import (
        constants,
        integration,
        models,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.constants import (
        FlextObservabilityTestConstants,
        FlextObservabilityTestConstants as c,
    )
    from tests.integration import test_phase_11_integration
    from tests.integration.test_phase_11_integration import ErrorEvent
    from tests.models import (
        FlextObservabilityTestModels,
        FlextObservabilityTestModels as m,
    )
    from tests.protocols import (
        FlextObservabilityTestProtocols,
        FlextObservabilityTestProtocols as p,
    )
    from tests.typings import (
        FlextObservabilityTestTypes,
        FlextObservabilityTestTypes as t,
    )
    from tests.unit import test_constants, test_factory, test_init
    from tests.unit.test_constants import TestFlextObservabilityConstants
    from tests.unit.test_factory import TestFlextObservabilityMasterFactoryReal
    from tests.unit.test_init import (
        TestInitCoverage,
        flext_alert,
        flext_health_check,
        flext_metric,
        flext_trace,
        get_global_factory,
        reset_global_factory,
    )
    from tests.utilities import (
        FlextObservabilityTestUtilities,
        FlextObservabilityTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "ErrorEvent": ["tests.integration.test_phase_11_integration", "ErrorEvent"],
    "FlextObservabilityTestConstants": [
        "tests.constants",
        "FlextObservabilityTestConstants",
    ],
    "FlextObservabilityTestModels": ["tests.models", "FlextObservabilityTestModels"],
    "FlextObservabilityTestProtocols": [
        "tests.protocols",
        "FlextObservabilityTestProtocols",
    ],
    "FlextObservabilityTestTypes": ["tests.typings", "FlextObservabilityTestTypes"],
    "FlextObservabilityTestUtilities": [
        "tests.utilities",
        "FlextObservabilityTestUtilities",
    ],
    "TestFlextObservabilityConstants": [
        "tests.unit.test_constants",
        "TestFlextObservabilityConstants",
    ],
    "TestFlextObservabilityMasterFactoryReal": [
        "tests.unit.test_factory",
        "TestFlextObservabilityMasterFactoryReal",
    ],
    "TestInitCoverage": ["tests.unit.test_init", "TestInitCoverage"],
    "c": ["tests.constants", "FlextObservabilityTestConstants"],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "flext_alert": ["tests.unit.test_init", "flext_alert"],
    "flext_health_check": ["tests.unit.test_init", "flext_health_check"],
    "flext_metric": ["tests.unit.test_init", "flext_metric"],
    "flext_trace": ["tests.unit.test_init", "flext_trace"],
    "get_global_factory": ["tests.unit.test_init", "get_global_factory"],
    "h": ["flext_tests", "h"],
    "integration": ["tests.integration", ""],
    "m": ["tests.models", "FlextObservabilityTestModels"],
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextObservabilityTestProtocols"],
    "protocols": ["tests.protocols", ""],
    "r": ["flext_tests", "r"],
    "reset_global_factory": ["tests.unit.test_init", "reset_global_factory"],
    "s": ["flext_tests", "s"],
    "t": ["tests.typings", "FlextObservabilityTestTypes"],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_factory": ["tests.unit.test_factory", ""],
    "test_init": ["tests.unit.test_init", ""],
    "test_phase_11_integration": ["tests.integration.test_phase_11_integration", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextObservabilityTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "ErrorEvent",
    "FlextObservabilityTestConstants",
    "FlextObservabilityTestModels",
    "FlextObservabilityTestProtocols",
    "FlextObservabilityTestTypes",
    "FlextObservabilityTestUtilities",
    "TestFlextObservabilityConstants",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "c",
    "constants",
    "d",
    "e",
    "flext_alert",
    "flext_health_check",
    "flext_metric",
    "flext_trace",
    "get_global_factory",
    "h",
    "integration",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "reset_global_factory",
    "s",
    "t",
    "test_constants",
    "test_factory",
    "test_init",
    "test_phase_11_integration",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
