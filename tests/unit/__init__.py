# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from tests.unit.test_constants import *
    from tests.unit.test_factory import *
    from tests.unit.test_init import *

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
