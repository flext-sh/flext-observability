# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_observability.tests.unit.test_constants import (
        TestsFlextObservabilityConstantsUnit as TestsFlextObservabilityConstantsUnit,
    )
    from flext_observability.tests.unit.test_factory import (
        TestsFlextObservabilityFactory as TestsFlextObservabilityFactory,
    )
    from flext_observability.tests.unit.test_init import (
        TestsFlextObservabilityInit as TestsFlextObservabilityInit,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_constants": ("TestsFlextObservabilityConstantsUnit",),
        ".test_factory": ("TestsFlextObservabilityFactory",),
        ".test_init": ("TestsFlextObservabilityInit",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
