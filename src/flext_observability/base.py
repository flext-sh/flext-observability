"""Shared service foundation for flext-observability components.

Provides typed access to the registered ``observability`` settings namespace while
preserving flext-core service runtime behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from abc import ABC
from collections.abc import MutableSequence

from flext_core import FlextService

from flext_observability import FlextObservabilitySettings, m, p


class FlextObservabilityServiceBase[TDomainResult](FlextService[TDomainResult], ABC):
    """Base class for flext-observability services with typed API settings access."""

    @classmethod
    def runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        """Return runtime bootstrap options for observability services."""
        return m.RuntimeBootstrapOptions(settings_type=FlextObservabilitySettings)


s = FlextObservabilityServiceBase

__all__: MutableSequence[str] = ["FlextObservabilityServiceBase", "s"]
