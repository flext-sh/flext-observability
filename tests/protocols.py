"""Test protocol definitions for flext-observability.

Provides TestsFlextObservabilityProtocols, combining FlextTestsProtocols with
FlextObservabilityProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_observability import FlextObservabilityProtocols


class TestsFlextObservabilityProtocols(
    FlextTestsProtocols,
    FlextObservabilityProtocols,
):
    """Test protocols combining FlextTestsProtocols and FlextObservabilityProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Observability.* (from FlextObservabilityProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with Observability-specific protocols.
        """

        class Observability:
            """Observability-specific test protocols."""


# Runtime aliases
p = TestsFlextObservabilityProtocols
p = TestsFlextObservabilityProtocols

__all__ = ["TestsFlextObservabilityProtocols", "p"]
