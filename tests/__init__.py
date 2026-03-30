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

    from tests import (
        constants,
        integration,
        models,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.constants import *
    from tests.integration import test_phase_11_integration
    from tests.integration.test_phase_11_integration import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import test_constants, test_factory, test_init
    from tests.unit.test_constants import *
    from tests.unit.test_factory import *
    from tests.unit.test_init import *
    from tests.utilities import *

from tests.integration import _LAZY_IMPORTS as _INTEGRATION_LAZY
from tests.unit import _LAZY_IMPORTS as _UNIT_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_INTEGRATION_LAZY,
    **_UNIT_LAZY,
    "FlextObservabilityTestConstants": "tests.constants",
    "FlextObservabilityTestModels": "tests.models",
    "FlextObservabilityTestProtocols": "tests.protocols",
    "FlextObservabilityTestTypes": "tests.typings",
    "FlextObservabilityTestUtilities": "tests.utilities",
    "c": ["tests.constants", "FlextObservabilityTestConstants"],
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "h": "flext_tests",
    "integration": "tests.integration",
    "m": ["tests.models", "FlextObservabilityTestModels"],
    "models": "tests.models",
    "p": ["tests.protocols", "FlextObservabilityTestProtocols"],
    "protocols": "tests.protocols",
    "r": "flext_tests",
    "s": "flext_tests",
    "t": ["tests.typings", "FlextObservabilityTestTypes"],
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextObservabilityTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
