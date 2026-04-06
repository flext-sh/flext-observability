# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import observability_settings, pytest_plugins

    constants = _tests_constants
    import tests.integration as _tests_integration
    from tests.constants import (
        FlextObservabilityTestConstants,
        FlextObservabilityTestConstants as c,
    )

    integration = _tests_integration
    import tests.models as _tests_models
    from tests.integration import ErrorEvent, test_phase_11_integration

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import (
        FlextObservabilityTestModels,
        FlextObservabilityTestModels as m,
    )

    protocols = _tests_protocols
    import tests.typings as _tests_typings
    from tests.protocols import (
        FlextObservabilityTestProtocols,
        FlextObservabilityTestProtocols as p,
    )

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import (
        FlextObservabilityTestTypes,
        FlextObservabilityTestTypes as t,
    )

    unit = _tests_unit
    import tests.utilities as _tests_utilities
    from tests.unit import (
        Testc,
        TestFlextObservabilityMasterFactoryReal,
        TestInitCoverage,
        flext_alert,
        flext_health_check,
        flext_metric,
        flext_trace,
        get_global_factory,
        reset_global_factory,
        test_constants,
        test_factory,
        test_init,
    )

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextObservabilityTestUtilities,
        FlextObservabilityTestUtilities as u,
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
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "integration": "tests.integration",
        "m": ("tests.models", "FlextObservabilityTestModels"),
        "models": "tests.models",
        "observability_settings": "tests.conftest",
        "p": ("tests.protocols", "FlextObservabilityTestProtocols"),
        "protocols": "tests.protocols",
        "pytest_plugins": "tests.conftest",
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
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "conftest",
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
    "observability_settings",
    "p",
    "protocols",
    "pytest_plugins",
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
