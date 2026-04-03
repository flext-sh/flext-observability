# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from tests.constants import (
    FlextObservabilityTestConstants,
    FlextObservabilityTestConstants as c,
)
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
from tests.unit.test_constants import Testc
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

if _t.TYPE_CHECKING:
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.integration.test_phase_11_integration as _tests_integration_test_phase_11_integration

    test_phase_11_integration = _tests_integration_test_phase_11_integration
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_factory as _tests_unit_test_factory

    test_factory = _tests_unit_test_factory
    import tests.unit.test_init as _tests_unit_test_init

    test_init = _tests_unit_test_init
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        ErrorEvent,
        FlextObservabilityTestConstants,
        FlextObservabilityTestModels,
        FlextObservabilityTestProtocols,
        FlextObservabilityTestTypes,
        FlextObservabilityTestUtilities,
        TestFlextObservabilityMasterFactoryReal,
        TestInitCoverage,
        Testc,
        c,
        constants,
        d,
        e,
        flext_alert,
        flext_health_check,
        flext_metric,
        flext_trace,
        get_global_factory,
        h,
        integration,
        m,
        models,
        p,
        protocols,
        r,
        reset_global_factory,
        s,
        t,
        test_constants,
        test_factory,
        test_init,
        test_phase_11_integration,
        typings,
        u,
        unit,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "tests.integration",
        "tests.unit",
    ),
    {
        "FlextObservabilityTestConstants": "tests.constants",
        "FlextObservabilityTestModels": "tests.models",
        "FlextObservabilityTestProtocols": "tests.protocols",
        "FlextObservabilityTestTypes": "tests.typings",
        "FlextObservabilityTestUtilities": "tests.utilities",
        "c": ("tests.constants", "FlextObservabilityTestConstants"),
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "integration": "tests.integration",
        "m": ("tests.models", "FlextObservabilityTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextObservabilityTestProtocols"),
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("tests.typings", "FlextObservabilityTestTypes"),
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextObservabilityTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "ErrorEvent",
    "FlextObservabilityTestConstants",
    "FlextObservabilityTestModels",
    "FlextObservabilityTestProtocols",
    "FlextObservabilityTestTypes",
    "FlextObservabilityTestUtilities",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "Testc",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
