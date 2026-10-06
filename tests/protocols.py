"""Test protocols for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_observability import FlextObservabilityProtocols


class TestsFlextObservabilityProtocols(
    FlextTestsProtocols,
    FlextObservabilityProtocols,
):
    """Test protocols for flext-observability."""

    class TestsFlextObservability(
        FlextTestsProtocols.Tests,
        FlextObservabilityProtocols.Observability,
    ):
        """Canonical namespace for test protocols."""


p = TestsFlextObservabilityProtocols
__all__: list[str] = ["TestsFlextObservabilityProtocols", "p"]
