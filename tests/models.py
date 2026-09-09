"""Test models for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_observability import FlextObservabilityModels


class TestsFlextObservabilityModels(FlextTestsModels, FlextObservabilityModels):
    """Test models for flext-observability."""


m = TestsFlextObservabilityModels
__all__: list[str] = ["TestsFlextObservabilityModels", "m"]
