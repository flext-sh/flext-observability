# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

    from tests import constants, models, protocols, typings, utilities
    from tests.constants import *
    from tests.integration import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "ErrorEvent": "tests.integration.test_phase_11_integration",
    "FlextObservabilityTestConstants": "tests.constants",
    "FlextObservabilityTestModels": "tests.models",
    "FlextObservabilityTestProtocols": "tests.protocols",
    "FlextObservabilityTestTypes": "tests.typings",
    "FlextObservabilityTestUtilities": "tests.utilities",
    "TestFlextObservabilityConstants": "tests.unit.test_constants",
    "TestFlextObservabilityMasterFactoryReal": "tests.unit.test_factory",
    "TestInitCoverage": "tests.unit.test_init",
    "c": ["tests.constants", "FlextObservabilityTestConstants"],
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "flext_alert": "tests.unit.test_init",
    "flext_health_check": "tests.unit.test_init",
    "flext_metric": "tests.unit.test_init",
    "flext_trace": "tests.unit.test_init",
    "get_global_factory": "tests.unit.test_init",
    "h": "flext_tests",
    "integration": "tests.integration",
    "m": ["tests.models", "FlextObservabilityTestModels"],
    "models": "tests.models",
    "p": ["tests.protocols", "FlextObservabilityTestProtocols"],
    "protocols": "tests.protocols",
    "r": "flext_tests",
    "reset_global_factory": "tests.unit.test_init",
    "s": "flext_tests",
    "t": ["tests.typings", "FlextObservabilityTestTypes"],
    "test_constants": "tests.unit.test_constants",
    "test_factory": "tests.unit.test_factory",
    "test_init": "tests.unit.test_init",
    "test_phase_11_integration": "tests.integration.test_phase_11_integration",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextObservabilityTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
