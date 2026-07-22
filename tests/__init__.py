# AUTO-GENERATED FILE — canonical lazy tests facade. Regenerate with: make gen
"""Test package facade exposing the project test aliases lazily."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from tests.base import (
        TestsFlextObservabilityServiceBase as TestsFlextObservabilityServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextObservabilityConstants as TestsFlextObservabilityConstants,
        c as c,
    )
    from tests.models import (
        TestsFlextObservabilityModels as TestsFlextObservabilityModels,
        m as m,
    )
    from tests.protocols import (
        TestsFlextObservabilityProtocols as TestsFlextObservabilityProtocols,
        p,
    )
    from tests.typings import (
        TestsFlextObservabilityTypes as TestsFlextObservabilityTypes,
        t as t,
    )
    from tests.utilities import (
        TestsFlextObservabilityUtilities as TestsFlextObservabilityUtilities,
        u,
    )

_LAZY_IMPORTS = build_lazy_import_map({
    ".constants": ("TestsFlextObservabilityConstants", "c"),
    ".typings": ("TestsFlextObservabilityTypes", "t"),
    ".protocols": ("TestsFlextObservabilityProtocols", "p"),
    ".models": ("TestsFlextObservabilityModels", "m"),
    ".utilities": ("TestsFlextObservabilityUtilities", "u"),
    ".base": ("TestsFlextObservabilityServiceBase", "s"),
})

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
