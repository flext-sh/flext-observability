"""Test utilities for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_observability import FlextObservabilityUtilities


class FlextObservabilityTestUtilities(FlextTestsUtilities, FlextObservabilityUtilities):
    """Test utilities for flext-observability."""


u = FlextObservabilityTestUtilities
__all__ = ["FlextObservabilityTestUtilities", "u"]
