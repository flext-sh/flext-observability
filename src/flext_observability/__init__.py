# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext observability package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_observability.api import *
    from flext_observability.base import *
    from flext_observability.constants import *
    from flext_observability.models import *
    from flext_observability.protocols import *
    from flext_observability.services import *
    from flext_observability.settings import *
    from flext_observability.typings import *
    from flext_observability.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_observability.services",),
    {
        "FlextObservability": "flext_observability.api",
        "FlextObservabilityConstants": "flext_observability.constants",
        "FlextObservabilityMasterFactory": "flext_observability.api",
        "FlextObservabilityModels": "flext_observability.models",
        "FlextObservabilityProtocols": "flext_observability.protocols",
        "FlextObservabilityServiceBase": "flext_observability.base",
        "FlextObservabilitySettings": "flext_observability.settings",
        "FlextObservabilityTypes": "flext_observability.typings",
        "FlextObservabilityUtilities": "flext_observability.utilities",
        "api": "flext_observability.api",
        "base": "flext_observability.base",
        "c": ("flext_observability.constants", "FlextObservabilityConstants"),
        "constants": "flext_observability.constants",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": ("flext_observability.models", "FlextObservabilityModels"),
        "models": "flext_observability.models",
        "p": ("flext_observability.protocols", "FlextObservabilityProtocols"),
        "protocols": "flext_observability.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "services": "flext_observability.services",
        "settings": "flext_observability.settings",
        "t": ("flext_observability.typings", "FlextObservabilityTypes"),
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityUtilities"),
        "utilities": "flext_observability.utilities",
        "x": "flext_core",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
