# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from tests.integration import test_phase_11_integration
    from tests.integration.test_phase_11_integration import ErrorEvent

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "ErrorEvent": "tests.integration.test_phase_11_integration",
    "test_phase_11_integration": "tests.integration.test_phase_11_integration",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
