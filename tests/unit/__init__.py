# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
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

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestFlextObservabilityConstants": [
        "tests.unit.test_constants",
        "TestFlextObservabilityConstants",
    ],
    "TestFlextObservabilityMasterFactoryReal": [
        "tests.unit.test_factory",
        "TestFlextObservabilityMasterFactoryReal",
    ],
    "TestInitCoverage": ["tests.unit.test_init", "TestInitCoverage"],
    "flext_alert": ["tests.unit.test_init", "flext_alert"],
    "flext_health_check": ["tests.unit.test_init", "flext_health_check"],
    "flext_metric": ["tests.unit.test_init", "flext_metric"],
    "flext_trace": ["tests.unit.test_init", "flext_trace"],
    "get_global_factory": ["tests.unit.test_init", "get_global_factory"],
    "reset_global_factory": ["tests.unit.test_init", "reset_global_factory"],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_factory": ["tests.unit.test_factory", ""],
    "test_init": ["tests.unit.test_init", ""],
}

_EXPORTS: Sequence[str] = [
    "TestFlextObservabilityConstants",
    "TestFlextObservabilityMasterFactoryReal",
    "TestInitCoverage",
    "flext_alert",
    "flext_health_check",
    "flext_metric",
    "flext_trace",
    "get_global_factory",
    "reset_global_factory",
    "test_constants",
    "test_factory",
    "test_init",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
