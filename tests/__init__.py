"""FLEXT Observability Tests - Test infrastructure and utilities.

Provides TestsFlextObservability classes extending FlextTests and FlextObservability
for comprehensive testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.models import (
        TestsFlextObservabilityModels,
        TestsFlextObservabilityModels as m,
        tm,
    )
    from tests.protocols import (
        TestsFlextObservabilityProtocols,
        TestsFlextObservabilityProtocols as p,
    )
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestsFlextObservabilityModels": ("tests.models", "TestsFlextObservabilityModels"),
    "TestsFlextObservabilityProtocols": (
        "tests.protocols",
        "TestsFlextObservabilityProtocols",
    ),
    "m": ("tests.models", "TestsFlextObservabilityModels"),
    "p": ("tests.protocols", "TestsFlextObservabilityProtocols"),
    "tm": ("tests.models", "tm"),
}
__all__ = [
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "m",
    "p",
    "tm",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
