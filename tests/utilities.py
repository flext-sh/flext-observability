"""Module skeleton for TestsFlextObservabilityUtilities.

Test utilities for flextobservability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u as _base_u
from flext_tests._utilities.matchers import FlextTestsMatchersUtilities

from flext_observability.utilities import FlextObservabilityUtilities


class TestsFlextObservabilityUtilities(FlextObservabilityUtilities):
    """Test utilities for flextobservability."""

    class Tests(FlextTestsMatchersUtilities.Tests, _base_u.Tests):
        """Merged Tests namespace with Matchers from FlextTestsMatchersUtilities."""


u = TestsFlextObservabilityUtilities
__all__ = ["TestsFlextObservabilityUtilities", "u"]
