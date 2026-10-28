"""Runtime settings for flext-observability tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_observability import FlextObservabilitySettings


class TestsFlextObservabilitySettings(FlextObservabilitySettings, FlextTestsSettings):
    """Observability settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextObservabilitySettings"]
