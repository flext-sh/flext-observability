# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_observability.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_observability.api import (
        FlextObservability as FlextObservability,
        observability as observability,
    )
    from flext_observability.constants import (
        FlextObservabilityConstants as FlextObservabilityConstants,
        c as c,
    )
    from flext_observability.models import (
        FlextObservabilityModels as FlextObservabilityModels,
        m as m,
    )
    from flext_observability.protocols import (
        FlextObservabilityProtocols as FlextObservabilityProtocols,
        p as p,
    )
    from flext_observability.settings import (
        FlextObservabilitySettings as FlextObservabilitySettings,
    )
    from flext_observability.typings import (
        FlextObservabilityTypes as FlextObservabilityTypes,
        t as t,
    )
    from flext_observability.utilities import (
        FlextObservabilityUtilities as FlextObservabilityUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextObservability",
            "observability",
        ),
        ".constants": (
            "FlextObservabilityConstants",
            "c",
        ),
        ".models": (
            "FlextObservabilityModels",
            "m",
        ),
        ".protocols": (
            "FlextObservabilityProtocols",
            "p",
        ),
        ".settings": ("FlextObservabilitySettings",),
        ".typings": (
            "FlextObservabilityTypes",
            "t",
        ),
        ".utilities": (
            "FlextObservabilityUtilities",
            "u",
        ),
        "flext_core": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityConstants",
    "FlextObservabilityModels",
    "FlextObservabilityProtocols",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "observability",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
