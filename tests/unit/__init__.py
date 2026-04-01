# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestFlextObservabilityConstants": "tests.unit.test_constants",
    "TestFlextObservabilityMasterFactoryReal": "tests.unit.test_factory",
    "TestInitCoverage": "tests.unit.test_init",
    "flext_alert": "tests.unit.test_init",
    "flext_health_check": "tests.unit.test_init",
    "flext_metric": "tests.unit.test_init",
    "flext_trace": "tests.unit.test_init",
    "get_global_factory": "tests.unit.test_init",
    "reset_global_factory": "tests.unit.test_init",
    "test_constants": "tests.unit.test_constants",
    "test_factory": "tests.unit.test_factory",
    "test_init": "tests.unit.test_init",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
