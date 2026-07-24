"""Test protocols for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_observability import p


class TestsFlextObservabilityProtocols(FlextTestsProtocols, p):
    """Test protocols for flext-observability."""

    class Tests(FlextTestsProtocols.Tests):
        """Test-specific protocols."""


p = TestsFlextObservabilityProtocols
__all__: list[str] = ["TestsFlextObservabilityProtocols", "p"]
