"""Test utilities for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_observability import FlextObservabilityUtilities
from flext_tests import FlextTestsUtilities


class TestsFlextObservabilityUtilities(
    FlextTestsUtilities, FlextObservabilityUtilities
):
    """Test utilities for flext-observability."""


u = TestsFlextObservabilityUtilities
__all__: list[str] = ["TestsFlextObservabilityUtilities", "u"]
