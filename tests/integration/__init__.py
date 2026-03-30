# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.integration import test_phase_11_integration as test_phase_11_integration
    from tests.integration.test_phase_11_integration import ErrorEvent as ErrorEvent

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "ErrorEvent": ["tests.integration.test_phase_11_integration", "ErrorEvent"],
    "test_phase_11_integration": ["tests.integration.test_phase_11_integration", ""],
}

_EXPORTS: Sequence[str] = [
    "ErrorEvent",
    "test_phase_11_integration",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
