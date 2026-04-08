"""Shared service foundation for flext-observability components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with s from flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from typing import override

from flext_core import FlextSettings, s
from flext_observability import FlextObservabilitySettings, t


class FlextObservabilityServiceBase(s[t.Dict], ABC):
    """Base class for flext-observability services with typed configuration access."""

    @property
    @override
    def settings(self) -> FlextObservabilitySettings:
        """Return the typed observability settings namespace."""
        return FlextSettings.get_global().get_namespace(
            "observability", FlextObservabilitySettings
        )


__all__: t.StrSequence = ["FlextObservabilityServiceBase", "s"]
