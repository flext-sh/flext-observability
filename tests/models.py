"""Test models for flext-observability tests.

Provides TestsFlextObservabilityModels, extending FlextTestsModels with
flext-observability-specific models using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsModels (flext_tests) - Provides .Tests.* namespace
- FlextObservabilityModels (production) - Provides observability domain models

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.models import FlextTestsModels

from flext_observability.models import FlextObservabilityModels


class TestsFlextObservabilityModels(FlextTestsModels, FlextObservabilityModels):
    """Models for flext-observability tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsModels - for test infrastructure (.Tests.*)
    2. FlextObservabilityModels - for domain models (GenericObservabilityEntry, etc.)

    Access patterns:
    - tm.Tests.* (generic test models from FlextTestsModels)
    - tm.GenericObservabilityEntry (observability entry model)
    - tm.GenericObservabilityConfig (observability config model)
    - tm.Metrics.* (metrics domain models)
    - m.* (production models via alternative alias)

    Rules:
    - NEVER duplicate models from FlextTestsModels or FlextObservabilityModels
    - Only flext-observability-specific test fixtures allowed
    - All generic test models come from FlextTestsModels
    - All production models come from FlextObservabilityModels
    """

    # class Tests:
        """Project-specific test fixtures namespace.

        Provides test fixtures for flext-observability testing.
        Extends the base FlextTestsModels.Tests namespace.
        """

        class Observability:
            """Observability-specific test fixtures."""


# Short aliases per FLEXT convention
tm = TestsFlextObservabilityModels  # Primary test models alias
m = TestsFlextObservabilityModels  # Alternative alias for production model access

__all__ = [
    "TestsFlextObservabilityModels",
    "m",
    "tm",
]
