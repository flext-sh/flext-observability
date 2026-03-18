"""Test protocol definitions for flext-observability.

Provides TestsFlextObservabilityProtocols, combining p with
FlextObservabilityProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_observability import FlextObservabilityProtocols


class TestsFlextObservabilityProtocols(p, FlextObservabilityProtocols):
    """Test protocols combining p and FlextObservabilityProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Observability.* (from FlextObservabilityProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends p.Tests with Observability-specific protocols.
        """

        class Observability:
            """Observability-specific test protocols."""


__all__ = ["TestsFlextObservabilityProtocols", "p"]

p = TestsFlextObservabilityProtocols
