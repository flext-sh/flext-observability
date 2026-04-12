"""Test configuration for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from flext_observability import FlextObservabilitySettings


@pytest.fixture
def observability_settings(
    settings_factory: Callable[..., FlextObservabilitySettings],
) -> FlextObservabilitySettings:
    """Provide clean FlextObservabilitySettings for tests."""
    return settings_factory(FlextObservabilitySettings)
