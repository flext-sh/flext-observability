# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
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
    from tests.integration import ErrorEvent, test_phase_11_integration
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
    from tests.unit import (
        TestFlextObservabilityConstants,
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
    from tests.utilities import (
        FlextObservabilityTestUtilities,
        FlextObservabilityTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
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
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "integration": "tests.integration",
        "m": ("tests.models", "FlextObservabilityTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextObservabilityTestProtocols"),
        "protocols": "tests.protocols",
        "r": "flext_tests",
        "s": "flext_tests",
        "t": ("tests.typings", "FlextObservabilityTestTypes"),
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextObservabilityTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
