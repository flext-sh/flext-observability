# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_factory as _tests_unit_test_factory
    from tests.unit.test_constants import Testc

    test_factory = _tests_unit_test_factory
    import tests.unit.test_init as _tests_unit_test_init
    from tests.unit.test_factory import TestFlextObservabilityMasterFactoryReal

    test_init = _tests_unit_test_init
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from tests.unit.test_init import (
        TestInitCoverage,
        flext_alert,
        flext_health_check,
        flext_metric,
        flext_trace,
        get_global_factory,
        reset_global_factory,
    )
_LAZY_IMPORTS = {
    "TestFlextObservabilityMasterFactoryReal": "tests.unit.test_factory",
    "TestInitCoverage": "tests.unit.test_init",
    "Testc": "tests.unit.test_constants",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "flext_alert": "tests.unit.test_init",
    "flext_health_check": "tests.unit.test_init",
    "flext_metric": "tests.unit.test_init",
    "flext_trace": "tests.unit.test_init",
    "get_global_factory": "tests.unit.test_init",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "reset_global_factory": "tests.unit.test_init",
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_constants": "tests.unit.test_constants",
    "test_factory": "tests.unit.test_factory",
    "test_init": "tests.unit.test_init",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "Testc",
    "c",
    "d",
    "e",
    "flext_alert",
    "flext_health_check",
    "flext_metric",
    "flext_trace",
    "get_global_factory",
    "h",
    "m",
    "p",
    "r",
    "reset_global_factory",
    "s",
    "t",
    "test_constants",
    "test_factory",
    "test_init",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
