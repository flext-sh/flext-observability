# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests import (
        constants as constants,
        integration as integration,
        models as models,
        protocols as protocols,
        typings as typings,
        unit as unit,
        utilities as utilities,
    )
    from tests.constants import (
        FlextObservabilityTestConstants as FlextObservabilityTestConstants,
        FlextObservabilityTestConstants as c,
    )
    from tests.integration import test_phase_11_integration as test_phase_11_integration
    from tests.integration.test_phase_11_integration import ErrorEvent as ErrorEvent
    from tests.models import (
        FlextObservabilityTestModels as FlextObservabilityTestModels,
        FlextObservabilityTestModels as m,
    )
    from tests.protocols import (
        FlextObservabilityTestProtocols as FlextObservabilityTestProtocols,
        FlextObservabilityTestProtocols as p,
    )
    from tests.typings import (
        FlextObservabilityTestTypes as FlextObservabilityTestTypes,
        FlextObservabilityTestTypes as t,
    )
    from tests.unit import (
        test_constants as test_constants,
        test_factory as test_factory,
        test_init as test_init,
    )
    from tests.unit.test_constants import (
        TestFlextObservabilityConstants as TestFlextObservabilityConstants,
    )
    from tests.unit.test_factory import (
        TestFlextObservabilityMasterFactoryReal as TestFlextObservabilityMasterFactoryReal,
    )
    from tests.unit.test_init import (
        TestInitCoverage as TestInitCoverage,
        flext_alert as flext_alert,
        flext_health_check as flext_health_check,
        flext_metric as flext_metric,
        flext_trace as flext_trace,
        get_global_factory as get_global_factory,
        reset_global_factory as reset_global_factory,
    )
    from tests.utilities import (
        FlextObservabilityTestUtilities as FlextObservabilityTestUtilities,
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

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
